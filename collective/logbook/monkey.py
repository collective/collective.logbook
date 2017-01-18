# -*- coding: utf-8 -*-

from zope.event import notify

from Products.SiteErrorLog.SiteErrorLog import SiteErrorLog

from collective.logbook.utils import log
from collective.logbook.utils import is_patch_applied
from collective.logbook.events import ErrorRaisedEvent
from collective.logbook.utils import is_logbook_enabled

_raising = SiteErrorLog.raising


def install_monkey():
    if not is_patch_applied():
        log(">>> Installing Monkey Patch for Products.SiteErrorLog")
        SiteErrorLog.raising = raising
    else:
        log(">>> Monkey Patch for Products.SiteErrorLog already applied")


def uninstall_monkey():
    if is_patch_applied():
        log(">>> Uninstalling Monkey for Products.SiteErrorLog")
        SiteErrorLog.raising = _raising
    else:
        log(">>> Monkey Patch for Products.SiteErrorLog already deactivated")


def raising(self, info):
    # Uninstall the monkey if logbook logging is disabled to avoid any kind of
    # performance issues when this package is installed only to avoid any kind
    # of performance issues when logging is disabled.
    if not is_logbook_enabled():
        return uninstall_monkey()
    enty_url = _raising(self, info)
    notify(ErrorRaisedEvent(self, enty_url))
    return enty_url
