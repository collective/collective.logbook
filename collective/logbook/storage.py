# -*- coding: utf-8 -*-

from BTrees.OOBTree import OOBTree
from collective.logbook.config import INDEX_KEY
from collective.logbook.config import LOGGER
from collective.logbook.config import REFERENCE_ERRORS
from collective.logbook.config import STORAGE_KEY
from collective.logbook.events import NotifyTraceback
from collective.logbook.interfaces import ILogBookStorage
from collective.logbook.utils import filtered_error_tail
from zope import event
from zope.annotation.interfaces import IAnnotations
from zope.interface import implementer


@implementer(ILogBookStorage)
class LogBookStorage(object):
    """ A LogBookStorage implementation based on Annotation Storage which is
    capable to handle same errors as references.
    """

    def __init__(self, portal):
        self.portal = portal

    @property
    def _storage(self):
        """ annotation storage bound to the portal

        ERRORS = {111: error_object,
                  222: error_object,
                 }
        """
        annotations = IAnnotations(self.portal)
        # create the logbook storage
        if annotations.get(STORAGE_KEY) is None:
            annotations[STORAGE_KEY] = OOBTree()
        return annotations[STORAGE_KEY]

    @property
    def _index(self):
        """ annotation storage bound to the portal

        REFINDEX = {333: 111,
                    444: 222,
                   }
        """
        annotations = IAnnotations(self.portal)
        # create the error reference storage
        if annotations.get(INDEX_KEY) is None:
            annotations[INDEX_KEY] = OOBTree()
        return annotations[INDEX_KEY]

    @property
    def error_count(self):
        """ count error entries
        """
        return len(self._storage)

    @property
    def reference_count(self):
        """ count referenced entries
        """
        return len(self._index)

    def save_error(self, error):
        """ see ILogBookStorage
        """
        if REFERENCE_ERRORS == 0:
            return self._handle_save(error)
        else:
            return self._handle_reference_enabled_save(error)

    def delete_error(self, err_id):
        """ see ILogBookStorage
        """
        try:
            del self._storage[err_id]
            self._cleanup_index()
            return True
        except KeyError:
            return False

    def get_error(self, err_id):
        """ see ILogBookStorage
        """
        # storages
        storage = self._storage
        index = self._index

        if err_id in storage:
            return storage.get(err_id)
        elif err_id in index:
            reference = index.get(err_id)
            if type(reference) == str:
                return storage.get(reference)
            return storage.get(reference.get('referencedError'))
        else:
            return False

    def get_all_errors(self):
        """ see ILogBookStorage
        """
        return self._storage.items()

    def get_counter(self, err_id):
        """ see ILogBookStorage
        """
        return len(self.get_referenced_errordata(err_id))

    def get_referenced_errordata(self, err_id):
        """ see ILogBookStorage
        """
        out = []
        for k, v in self._index.items():
            if type(v) == str:
                # stay backward compatible with simple ref storage
                refId = v
            else:
                refId = v.get('referencedError', None)

            if refId == err_id:
                out.append(v)
        return out

    def delete_all_errors(self):
        """ see ILogBookStorage
        """
        annotations = IAnnotations(self.portal)
        if annotations.get(STORAGE_KEY):
            del annotations[STORAGE_KEY]

        if annotations.get(INDEX_KEY):
            del annotations[INDEX_KEY]

    def delete_all_references(self):
        """ see ILogBookStorage
        """
        annotations = IAnnotations(self.portal)
        if annotations.get(INDEX_KEY):
            del annotations[INDEX_KEY]

    def _handle_save(self, error):
        """ save error to storage
        """
        err_id = error.get('id', None)
        if err_id is None:
            return False
        # save each error under its id
        self._storage[err_id] = error
        # notify new error
        event.notify(NotifyTraceback(error))
        return True

    def _handle_reference_enabled_save(self, error):
        """ check if this error is already logged in the storage.

        Therefore we check the last lines of the traceback and see if this is
        already in the storage
        """
        err_id = error.get('id', None)
        if err_id is None:
            return False

        # this is a kind of signature of the error
        tail = filtered_error_tail(error)

        # check all errors in the storage
        for existing_id, existing_error in self._storage.items():
            error_tail = filtered_error_tail(existing_error)

            # error signature is the same
            if error_tail == tail:
                info = dict(referencedError=existing_id,
                            time=error.get('time'),
                            userid=error.get('userid') or 'anon')
                self._index[err_id] = info
                return True

        # save it
        return self._handle_save(error)

    def _cleanup_index(self):
        """ clean the index
        """
        existing = [k for k in self._storage]

        orphane_keys = []
        for k, v in self._index.items():
            if v not in existing:
                LOGGER.info('+ Found orphaned Index %s' % k)
                orphane_keys.append(k)

        if len(orphane_keys):
            for k in orphane_keys:
                LOGGER.info('- Erasing orphaned Index %s' % k)
                del self._index[k]
