# -*- coding: utf-8 -*-
#
# File: Install.py
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

__author__ = 'Ramon Bartl <ramon.bartl@inquant.de>'
__docformat__ = 'plaintext'

import logging
from zope.annotation.interfaces import IAnnotations
from Products.CMFCore.utils import getToolByName
from collective.logbook.config import STORAGE_KEY
from collective.logbook.config import INDEX_KEY

logger = logging.getLogger('collective.logbook')

def install(portal):
    setup_tool = getToolByName(portal, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-collective.logbook:default')
    logger.info("*** INSTALL collective.logbook ***")
    return "Ran all import steps."

def uninstall(portal):
    setup_tool = getToolByName(portal, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-collective.logbook:uninstall')
    logger.info("*** UNINSTALL collective.logbook ***")

    # remove storages
    uninstall_storages(portal)

    return "Ran all uninstall steps."

def uninstall_storages(portal):
    annotations = IAnnotations(portal)
    if annotations.get(STORAGE_KEY):
        logger.info("*** UNINSTALL collective.logbook Logstorage ***")
        del annotations[STORAGE_KEY]

    if annotations.get(INDEX_KEY):
        logger.info("*** UNINSTALL collective.logbook Indexstorage ***")
        del annotations[INDEX_KEY]

# vim: set ft=python ts=4 sw=4 expandtab :
