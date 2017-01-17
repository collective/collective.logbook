# -*- coding: utf-8 -*-

from zope.event import notify

from Products.SiteErrorLog.SiteErrorLog import SiteErrorLog

from config import LOGGER
from events import ErrorRaisedEvent


_raising = SiteErrorLog.raising


def install_monkey():
    from collective.logbook.config import PATCH_APPLIED

    if not PATCH_APPLIED:
        LOGGER.info(">>> Installing Monkey Patch for Products.SiteErrorLog")
        SiteErrorLog.raising = raising
        PATCH_APPLIED = True
    else:
        LOGGER.info(">>> Monkey Patch for Products.SiteErrorLog already applied")


def uninstall_monkey():
    from collective.logbook.config import PATCH_APPLIED

    if PATCH_APPLIED:
        LOGGER.info(">>> Uninstalling Monkey for Products.SiteErrorLog")
        SiteErrorLog.raising = _raising
        PATCH_APPLIED = False
    else:
        LOGGER.info(">>> Monkey Patch for Products.SiteErrorLog already already deactivated")


def raising(self, info):
    enty_url = _raising(self, info)
    notify(ErrorRaisedEvent(self, enty_url))
    return enty_url
