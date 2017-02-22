# -*- coding: utf-8 -*-

from persistent.dict import PersistentDict
from BTrees.OOBTree import OOBTree

from zope.annotation.interfaces import IAnnotations

from Products.CMFCore.utils import getToolByName

from collective.logbook.interfaces import ILogBookStorage
from collective.logbook.config import STORAGE_KEY
from collective.logbook.config import INDEX_KEY

from plone import api


PACKAGE_NAME = 'collective.logbook'


def generic_setup_profile_id(package_name, profile='default'):
    return 'profile-{package_name}:{profile}'.format(
        package_name=package_name,
        profile=profile
    )


def run_import_step(profile_id, import_step):
    u"""Run an import step.

    Arguments:
    profile_id -- Profile ID. Eg.: "profile-my.package:default"
    import_step -- Import step IP. Eg.: "actions".
    """
    setup = api.portal.get_tool('portal_setup')
    setup.runImportStepFromProfile(profile_id, import_step)


def run_registry_import_step(context):
    profile_id = generic_setup_profile_id(
        package_name=PACKAGE_NAME,
        profile='default'
    )
    run_import_step(profile_id=profile_id, import_step='plone.app.registry')


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
