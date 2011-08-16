from persistent.dict import PersistentDict
from BTrees.OOBTree import OOBTree

from zope.annotation.interfaces import IAnnotations

from Products.CMFCore.utils import getToolByName

from collective.logbook.interfaces import ILogBookStorage
from collective.logbook.config import STORAGE_KEY
from collective.logbook.config import INDEX_KEY


def migrate_storage(context):
    portal_url = getToolByName(context, 'portal_url')
    portal = portal_url.getPortalObject()
    storage = ILogBookStorage(portal)
    assert isinstance(storage._storage, PersistentDict)
    assert isinstance(storage._index, PersistentDict)
    error_count = storage.error_count
    reference_count = storage.reference_count
    annotations = IAnnotations(portal)
    btree = migrate_PersistentDict(storage._storage)
    annotations[STORAGE_KEY] = btree
    btree = migrate_PersistentDict(storage._index)
    annotations[INDEX_KEY] = btree
    assert isinstance(storage._storage, OOBTree)
    assert isinstance(storage._index, OOBTree)
    assert error_count == storage.error_count
    assert reference_count == storage.reference_count


def migrate_PersistentDict(dict):
    result = OOBTree()
    result.update(dict)
    return result
