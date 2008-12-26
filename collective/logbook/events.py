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
from zope import event

from interfaces import IErrorRaisedEvent
from interfaces import INotofyTraceback

logger = logging.getLogger("inquant.error")


class ErrorRaisedEvent(object):
    interface.implements(IErrorRaisedEvent)

    def __init__(self, context, entry_url):
        self.context = context
        self.entry_url = entry_url


class NotifyTraceback(object):
    interface.implements(INotofyTraceback)

    def __init__(self, error):
        self.error = error
        logger.debug("***** Notify new error %s" % error.get('id', 0))


def handleTraceback(object):
    context = object.context
    entry_url = object.entry_url
    if entry_url is None:
        return
    try:
        # get our error view to use the api
        error_form = context.unrestrictedTraverse('@@error')
        # get the generated error url from Products.SiteErrorLog
        err_id = urllib.splitvalue(entry_url)[1]
        # get the error object from error_log
        error = error_form.error(err_id)
        # get a error signature (last 5 lines of traceback)
        error_tail = error_form.filtered_error_tail(error)

        # check for existing entries in our annotation storage
        for entry in error_form.saved_entries:
            entry_id = entry.get('id')
            # get signature of existing entries
            tail = error_form.filtered_error_tail(entry.get('tb'))

            if tail == error_tail:
                logger.debug("***** Traceback '%s' already logged" % tail[-1:])
                error_form.save_error_reference(err_id, entry_id)
                transaction.commit()
                return

        # notify new error
        event.notify(NotifyTraceback(error))
        logger.debug("***** New Traceback logged with err_id=%s" % err_id)
        error_form.save_entry(err_id)
        transaction.commit()
    except Exception, e:
        logger.warning("An error occured while handling the traceback")
        logger.warning("%s" % e)

# vim: set ft=python ts=4 sw=4 expandtab :
