# -*- coding: utf-8 -*-

from DateTime import DateTime
from Acquisition import aq_inner
from zExceptions import Forbidden

from zope import interface

from plone import api as ploneapi
from plone.memoize.instance import memoize

from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.logbook.interfaces import ILogBook
from collective.logbook.interfaces import ILogBookStorage
from collective.logbook import logbookMessageFactory as _
from collective.logbook.utils import is_logbook_large_site_enabled


class LogBook(BrowserView):
    """ Logbook Form
    """
    interface.implements(ILogBook)

    template = ViewPageTemplateFile('logbook.pt')

    def __init__(self, context, request):
        super(LogBook, self).__init__(context, request)
        self.context = aq_inner(context)
        self.request = request
        self.portal = ploneapi.portal.get()
        self.storage = ILogBookStorage(self.portal)

    def is_large_site_enabled(self):
        return is_logbook_large_site_enabled()

    def show_all_tracebacks(self):
        if self.has_errors():
            if 'form.button.showall' in self.request.form:
                return True
            elif not self.is_large_site_enabled():
                return True
        return False

    @property
    def error_count(self):
        """ number of logged errors
        """
        return self.storage.error_count

    @property
    def reference_count(self):
        """ number of referenced logged errors
        """
        return self.storage.reference_count

    @memoize
    def error_log(self):
        """ zope error log object
        """
        error_log_path = '/'.join(
            ['/'.join(self.portal.getPhysicalPath()), 'error_log'])
        return self.portal.restrictedTraverse(error_log_path)

    def error(self, err_id):
        """ see ILogBook
        """
        error = self.error_log().getLogEntryById(err_id)
        if error is None:
            return None
        # make human readable time
        error['time'] = DateTime(error['time'])
        return error

    def save_error(self, err_id, context=None):
        """ save error to the storage
        """
        error = self.error(err_id)
        if context is not None:
            error['context'] = context
        return self.storage.save_error(error)

    def delete_error(self, err_id):
        """ delete error from storage by id
        """
        return self.storage.delete_error(err_id)

    def delete_all_errors(self):
        """ delete all errors
        """
        return self.storage.delete_all_errors()

    def delete_all_references(self):
        """ delete all referenced errors
        """
        return self.storage.delete_all_references()

    def has_errors(self):
        """ checks for existing errors
        """
        return self.storage.error_count

    @property
    def saved_errors(self):
        """ saved errors in the storage
        """
        errors = self.storage.get_all_errors()
        out = []
        for id, tb in errors:
            refs = self.storage.get_referenced_errordata(id)
            out.append(
                dict(
                    id=id,
                    tb=tb,
                    counter=len(refs),
                    refs=refs
                )
            )
        return sorted(out, key=lambda x: x["counter"], reverse=True)

    def search_error(self, err_id):
        """ search an error by id
        """
        return self.storage.get_error(err_id)

    def __call__(self):
        self.request.set('disable_border', True)
        form = self.request.form

        submitted = form.get('form.submitted', None) is not None
        traceback_button = form.get('form.button.traceback', None) is not None
        delete_traceback_button = form.get('form.button.deletetraceback', None) is not None
        delete_refs_button = form.get('form.button.deleterefs', None) is not None
        delete_all_button = form.get('form.button.deleteall', None) is not None

        if submitted:
            if not self.request.get('REQUEST_METHOD', 'GET') == 'POST':
                raise Forbidden

            if traceback_button:
                err_id = form.get('errornumber', None)
                error = self.search_error(err_id)
                if not error:
                    IStatusMessage(self.request).addStatusMessage(_(u"Could not find error"), type='warning')
                self.request.set('entry', error)

            if delete_traceback_button:
                entries = form.get('entries', [])
                for entry in entries:
                    err_id = entry.get('id')
                    if self.delete_error(err_id):
                        IStatusMessage(self.request).addStatusMessage(_(u"Traceback %s deleted") % err_id, type='info')
                    else:
                        IStatusMessage(self.request).addStatusMessage(_(u"could not delete %s") % err_id, type='warning')

            if delete_all_button:
                self.delete_all_errors()
                IStatusMessage(self.request).addStatusMessage(_(u"Deleted all Errors"), type='info')

            if delete_refs_button:
                self.delete_all_references()
                IStatusMessage(self.request).addStatusMessage(_(u"Deleted all referenced Error"), type='info')

        return self.template()


class LogBookAtomFeed(LogBook):
    """ Logbook Atom Feed
    """
    template = ViewPageTemplateFile('logbook_atom.pt')

    def __init__(self, context, request):
        super(LogBookAtomFeed, self).__init__(context, request)
        self.context = aq_inner(context)
        self.request = request

    def __call__(self):
        return self.template()


class LogBookRSSFeed(LogBook):
    """ Logbook RSS Feed
    """
    template = ViewPageTemplateFile('logbook_rss.pt')

    def __init__(self, context, request):
        super(LogBookRSSFeed, self).__init__(context, request)
        self.context = aq_inner(context)
        self.request = request

    def __call__(self):
        return self.template()
