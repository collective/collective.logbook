# -*- coding: utf-8 -*-

import urllib
import transaction
from thread import allocate_lock

from zope import interface

from Acquisition import aq_parent

from collective.logbook.utils import log
from collective.logbook.config import LOGGER

from interfaces import IErrorRaisedEvent
from interfaces import INotifyTraceback


cleanup_lock = allocate_lock()


class ErrorRaisedEvent(object):
    interface.implements(IErrorRaisedEvent)

    def __init__(self, context, entry_url):
        self.context = context
        self.entry_url = entry_url


class NotifyTraceback(object):
    interface.implements(INotifyTraceback)

    def __init__(self, error):
        self.error = error
        log("***** Notify new traceback %s" % error.get('id', 0))


def mailHandler(event):
    """ notify this error
    """
    try:
        return event.error['context'].restrictedTraverse(
            '@@logbook_mail')(event)
    except Exception, e:
        log("An error occured while notifying recipients: {}".format(
            str(e)), level="error")


def webhookHandler(event):
    """ Travese to webhook handler and let it deal with the error.
    """
    try:
        return event.error['context'].restrictedTraverse(
            '@@logbook_webhook')(event)
    except Exception, e:
        log("An error occured while notifying with webhooks: {}".format(
            str(e)), level="error")


def handleTraceback(object):
    context = object.context
    entry_url = object.entry_url

    if entry_url is None:
        return

    log("handle traceback [%s]" % entry_url)
    try:
        cleanup_lock.acquire()
        # we don't want to produce any errors here, thus, we'll be nice and die
        # silently if an error occurs here
        try:
            transaction.begin()
            # get our logbook view to use the api
            logbook = context.unrestrictedTraverse('@@logbook')
            # get the generated error url from Products.SiteErrorLog
            err_id = urllib.splitvalue(entry_url)[1]
            # save error
            logbook.save_error(err_id, context=aq_parent(context))
            transaction.get().note('collective.logbook traceback [%s]' %
                                   entry_url)
            transaction.commit()
        finally:
            cleanup_lock.release()
    # only warning
    except Exception, e:
        log("An error occured while handling the traceback", level="warning")
        log("%s" % e, level="warning")
        LOGGER.exception(e)
