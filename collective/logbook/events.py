# -*- coding: utf-8 -*-
#
# File: events.py
#
# Copyright (c) InQuant GmbH
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

__author__    = 'Ramon Bartl <ramon.bartl@inquant.de>'
__docformat__ = 'plaintext'

import urllib
import transaction
from thread import allocate_lock

import Zope2

from zope import interface
from zope.app.component import hooks

from config import LOGGER
from config import PROP_KEY_LOG_MAILS
from utils import send

from interfaces import IErrorRaisedEvent
from interfaces import INotifyTraceback


cleanup_lock = allocate_lock()

MAIL_TEMPLATE = """
A new error occured on %(date)s

%(traceback)s

This error is saved under the number %(error_number)s

The error occured here %(error_url)s

Please check the logbook entry %(logbook_url)s
"""


class ErrorRaisedEvent(object):
    interface.implements(IErrorRaisedEvent)

    def __init__(self, context, entry_url):
        self.context = context
        self.entry_url = entry_url


class NotifyTraceback(object):
    interface.implements(INotifyTraceback)

    def __init__(self, error):
        self.error = error
        LOGGER.info("***** Notify new traceback %s" % error.get('id', 0))


def mailHandler(event):
    """ notify this error
    """
    app = Zope2.app()
    error = event.error
    portal = hooks.getSite()
    emails = app.getProperty(PROP_KEY_LOG_MAILS)

    recipients = [mail for mail in emails]
    subject = "[collective.logbook] NEW TRACEBACK: '%s'" % error.get("value")
    data = dict(
            date = error.get("time").strftime("%Y-%m-%d %H:%M:%S"),
            traceback = error.get("tb_text"),
            error_number = error.get("id"),
            error_url = error.get("url"),
            logbook_url = portal.absolute_url() + "/@@logbook?errornumber=%s" % error.get("id"),
            )

    try:
        message = MAIL_TEMPLATE % data
        send(portal, message, subject, recipients)
    except:
        LOGGER.info("An error occured while notifying recipients")



def handleTraceback(object):
    context = object.context
    entry_url = object.entry_url

    if entry_url is None:
        return

    LOGGER.info("handle traceback [%s]" % entry_url)

    try:
        cleanup_lock.acquire()
        # we don't want to produce any errors here, thus, we'll be nice and die
        # silently if an error occurs here
        try:
            # get our logbook view to use the api
            logbook = context.unrestrictedTraverse('@@logbook')
            # get the generated error url from Products.SiteErrorLog
            err_id = urllib.splitvalue(entry_url)[1]
            # save error
            logbook.save_error(err_id)
            transaction.commit()
        finally:
            cleanup_lock.release()
    # only warning
    except Exception, e:
        LOGGER.warning("An error occured while handling the traceback")
        LOGGER.warning("%s" % e)

# vim: set ft=python ts=4 sw=4 expandtab :
