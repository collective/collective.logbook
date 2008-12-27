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

import transaction
import logging
import urllib

from zope import interface

from interfaces import IErrorRaisedEvent
from interfaces import INotifyTraceback

logger = logging.getLogger("collective.logbook")


class ErrorRaisedEvent(object):
    interface.implements(IErrorRaisedEvent)

    def __init__(self, context, entry_url):
        self.context = context
        self.entry_url = entry_url


class NotifyTraceback(object):
    interface.implements(INotifyTraceback)

    def __init__(self, error):
        self.error = error
        logger.debug("***** Notify new error %s" % error.get('id', 0))


def handleTraceback(object):
    context = object.context
    entry_url = object.entry_url
    if entry_url is None:
        return
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
    # only warning
    except Exception, e:
        logger.warning("An error occured while handling the traceback")
        logger.warning("%s" % e)

# vim: set ft=python ts=4 sw=4 expandtab :
