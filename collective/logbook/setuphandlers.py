# -*- coding: utf-8 -*-

from collective.logbook.config import INDEX_KEY
from collective.logbook.config import STORAGE_KEY
from zope.annotation.interfaces import IAnnotations

from .config import PACKAGENAME
from .monkey import install_monkey
from .monkey import uninstall_monkey


def import_various(context):
    if context.readDataFile('{}_various.txt'.format(PACKAGENAME)) is None:
        return

    install_monkey()


def uninstall(context):
    if context.readDataFile('{}_uninstall.txt'.format(PACKAGENAME)) is None:
        return

    portal = context.getSite()

    uninstall_monkey()
    _uninstall_storages(portal)


def _uninstall_storages(portal):
    annotations = IAnnotations(portal)
    if annotations.get(STORAGE_KEY):
        del annotations[STORAGE_KEY]

    if annotations.get(INDEX_KEY):
        del annotations[INDEX_KEY]
