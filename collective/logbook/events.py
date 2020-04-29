# -*- coding: utf-8 -*-

import threading

from six.moves.urllib.parse import splitvalue

import transaction
from Acquisition import aq_base
from Acquisition import aq_parent
from collective.logbook.config import LOGGER
from collective.logbook.interfaces import IErrorRaisedEvent
from collective.logbook.interfaces import INotifyTraceback
from collective.logbook.utils import log
from plone import api
from zope.interface import implementer
from zope.publisher.interfaces import IView

cleanup_lock = threading.Lock()


@implementer(IErrorRaisedEvent)
class ErrorRaisedEvent(object):

    def __init__(self, context, entry_url):
        self.context = context
        self.entry_url = entry_url


@implementer(INotifyTraceback)
class NotifyTraceback(object):

    def __init__(self, error):
        self.error = error
        log('***** Notify new traceback %s' % error.get('id', 0))


def mailHandler(event):
    """ notify this error
    """
    try:
        portal = api.portal.get()
        return portal.restrictedTraverse('@@logbook_mail')(event)
    except Exception as e:
        log('An error occured while notifying recipients: {}'.format(
            str(e)), level='error')


def webhookHandler(event):
    """ Travese to webhook handler and let it deal with the error.
    """
    try:
        portal = api.portal.get()
        portal.restrictedTraverse('@@logbook_webhook')(event)
    except Exception as e:
        log('An error occured while notifying with webhooks: {}'.format(
            str(e)), level='error')


def handleTraceback(event):
    context = event.context
    entry_url = event.entry_url

    if entry_url is None:
        return

    log('handle traceback [%s]' % entry_url)
    try:
        cleanup_lock.acquire()
        # we don't want to produce any errors here, thus, we'll be nice and die
        # silently if an error occurs here
        try:
            transaction.begin()
            # get our logbook view to use the api
            logbook = context.unrestrictedTraverse('@@logbook')
            # get the generated error url from Products.SiteErrorLog
            err_id = splitvalue(entry_url)[1]
            # save error
            logbook.save_error(err_id, context=_getErrorContext(event))
            transaction.get().note('collective.logbook traceback [%s]' %
                                   entry_url)
            transaction.commit()
        finally:
            cleanup_lock.release()
    # only warning
    except Exception as e:
        log('An error occured while handling the traceback', level='warning')
        log('%s' % e, level='warning')
        LOGGER.exception(e)


def _getErrorContext(event):
    error_log = event.context
    error_context = aq_parent(error_log)

    # If the error context is a view then we must get the context of the view.
    # Otherwise an error will occur because views are cannot be persisted.
    if IView.providedBy(error_context):
        error_context = error_context.context

    # The error context will be persisted, so it must be acquisition unwrapped.
    return aq_base(error_context)
