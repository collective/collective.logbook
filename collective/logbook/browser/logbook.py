# -*- coding: utf-8 -*-
#
# File: logbook.py
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

import re
import logging

from DateTime import DateTime

from persistent.dict import PersistentDict

from zope.app.component import hooks
from zope.annotation.interfaces import IAnnotations

from Products.statusmessages.interfaces import IStatusMessage
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Acquisition import aq_inner, aq_parent, aq_base
from AccessControl import Unauthorized
from zExceptions import Forbidden

from plone.memoize.instance import memoize, clearafter

KEY = "ERRORS"
INDEX_KEY = "REFINDEX"
REGEX = re.compile(r'0x[0-9a-fA-F]+')

logger = logging.getLogger("collective.logbook")


def hexfilter(text):
    """ unify hex numbers
    """
    return REGEX.sub('0x0000000', text)


class LogBook(BrowserView):
    """ Logbook Form
    """
    template = ViewPageTemplateFile('logbook.pt')

    def __init__(self, context, request):
        super(LogBook, self).__init__(context, request)
        self.context = aq_inner(context)
        self.request = request

    @memoize
    def portal(self):
        """ portal object
        """
        return hooks.getSite()

    @memoize
    def error_log(self):
        """ portal error_log object
        """
        error_log_path = '/'.join(
                ['/'.join(self.portal().getPhysicalPath()), 'error_log'])
        return self.context.restrictedTraverse(error_log_path)

    @property
    def storage(self):
        """ annotation storage bound to the portal

        ERRORS = {111: error_object,
                  222: error_object,
                 }
        """
        annotations = IAnnotations(self.portal())
        # create the error storage
        if annotations.get(KEY) is None:
            annotations[KEY] = PersistentDict()
        return annotations[KEY]

    @property
    def index(self):
        """ annotation storage bound to the portal

        REFINDEX = {333: 111,
                    444: 222,
                   }
        """
        annotations = IAnnotations(self.portal())
        # create the error reference storage
        if annotations.get(INDEX_KEY) is None:
            annotations[INDEX_KEY] = PersistentDict()
        return annotations[INDEX_KEY]

    def error(self, err_id):
        """ get the error object from the zope error_log
        """
        error = self.error_log().getLogEntryById(err_id)
        if error is None:
            return None
        # make human readable time
        error['time'] = DateTime(error['time'])
        return error

    def save_entry(self, err_id):
        """ saves error to the storage
        """
        if self.error(err_id) is None:
            return False
        self.storage[err_id] = self.error(err_id)
        return True

    def save_error_reference(self, new_id, existing_id):
        """ references a new error to an existing error by its id
        """
        self.index[new_id] = existing_id

    def cleanup_index(self):
        """ clean the index
        """
        existing = [k for k in self.storage.keys()]

        orphane_keys = []
        for k, v in self.index.iteritems():
            if v not in existing:
                logger.info("+ Found orphaned Index %s" % k)
                orphane_keys.append(k)

        if len(orphane_keys):
            for k in orphane_keys:
                logger.info("- Erasing orphaned Index %s" % k)
                del self.index[k]

    def delete_entry(self, err_id):
        """ deletes an error entry from the storage
        """
        storage = self.storage
        try:
            del storage[err_id]
            return True
        except:
            return False

    def cleanup_all(self):
        """ delete all storages
        """
        annotations = IAnnotations(self.portal())
        if annotations.get(KEY):
            del annotations[KEY]

        if annotations.get(INDEX_KEY):
            del annotations[INDEX_KEY]

    def cleanup_refs(self):
        """ delete ref storage
        """
        annotations = IAnnotations(self.portal())
        if annotations.get(INDEX_KEY):
            del annotations[INDEX_KEY]

    @property
    def saved_entries(self):
        """ storage entries
        """
        out = []
        storage = self.storage
        if len(storage):
            for id, tb in storage.iteritems():
                out.append(
                        dict(
                            id = id,
                            tb = tb,
                            )
                        )
        return out

    def search_error_in_storage(self, err_id):
        """ search the storage
        """
        # storages
        storage = self.storage
        index = self.index

        # keys
        storage_keys = self.storage.keys()
        index_keys = self.index.keys()

        if err_id in storage_keys:
            return storage.get(err_id)
        elif err_id in index_keys:
            return storage.get(index.get(err_id))
        else:
            return False

    @property
    def error_count(self):
        """ count error entries
        """
        return len(self.storage)

    @property
    def index_count(self):
        """ count index entries
        """
        return len(self.index)

    def error_tail(self, error):
        """ return last 5 lines
        """
        tb_text = error.get('tb_text', '')
        tail = tb_text.splitlines()[-5:]
        return tail

    def filtered_error_tail(self, error):
        """ last 5 lines with replaced hex oids
        """
        tb_text = error.get('tb_text', '')
        tail = tb_text.splitlines()[-5:]
        filtered_tail = map(hexfilter, tail)
        return filtered_tail

    def __call__(self):
        self.request.set('disable_border', True)
        form = self.request.form

        submitted = form.get('form.submitted', None) is not None
        traceback_button = form.get('form.button.traceback', None) is not None
        delete_traceback_button = form.get('form.button.deletetraceback', None) is not None
        delete_refs_button = form.get('form.button.deleterefs', None) is not None
        delete_all_button = form.get('form.button.deleteall', None) is not None

        if submitted:
            if not self.request.get('REQUEST_METHOD','GET') == 'POST':
                raise Forbidden

            if traceback_button:
                err_id = form.get('errornumber', None)
                error = self.search_error_in_storage(err_id)
                self.request.set('entry', error)

            if delete_traceback_button:
                entries = form.get('entries', [])
                for entry in entries:
                    err_id = entry.get('id')
                    if self.delete_entry(err_id):
                        IStatusMessage(self.request).addStatusMessage(u"Traceback %s deleted" % err_id, type='info')
                    else:
                        IStatusMessage(self.request).addStatusMessage(u"could not delete %s" % err_id, type='warning')

                # clean the index after delete
                self.cleanup_index()

            if delete_all_button:
                self.cleanup_all()
                IStatusMessage(self.request).addStatusMessage(u"Deleted all Error Storages", type='info')

            if delete_refs_button:
                self.cleanup_refs()
                IStatusMessage(self.request).addStatusMessage(u"Deleted all referenced Error", type='info')

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

# vim: set ft=python ts=4 sw=4 expandtab :
