# -*- coding: utf-8 -*-

from zope.annotation.interfaces import IAnnotations

from Products.CMFCore.utils import getToolByName

from collective.logbook.config import STORAGE_KEY
from collective.logbook.config import INDEX_KEY
from collective.logbook.config import LOGGER
from collective.logbook.monkey import install_monkey
from collective.logbook.monkey import uninstall_monkey


def install(portal):
    setup_tool = getToolByName(portal, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-collective.logbook:default')

    # install monkey
    install_monkey()

    LOGGER.info("*** INSTALLED collective.logbook ***")
    return "Ran all import steps."


def uninstall(portal):
    setup_tool = getToolByName(portal, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-collective.logbook:uninstall')

    # remove monkey
    uninstall_monkey()

    # remove storages
    uninstall_storages(portal)

    LOGGER.info("*** UNINSTALLED collective.logbook ***")
    return "Ran all uninstall steps."


def uninstall_storages(portal):
    annotations = IAnnotations(portal)
    if annotations.get(STORAGE_KEY):
        LOGGER.info("*** UNINSTALL collective.logbook Logstorage ***")
        del annotations[STORAGE_KEY]

    if annotations.get(INDEX_KEY):
        LOGGER.info("*** UNINSTALL collective.logbook Indexstorage ***")
        del annotations[INDEX_KEY]
