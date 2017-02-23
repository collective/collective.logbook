# -*- coding: utf-8 -*-

from zope.event import notify

from Products.SiteErrorLog.SiteErrorLog import SiteErrorLog

from collective.logbook.utils import log
from collective.logbook.utils import is_patch_applied
from collective.logbook.events import ErrorRaisedEvent
from collective.logbook.utils import is_logbook_enabled
from zope.component.interfaces import ComponentLookupError

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
    # Uninstall the monkey if logbook logging is disabled in the Plone Registry.
    try:
        if not is_logbook_enabled():
            return uninstall_monkey()
    except ComponentLookupError:
        # This error will occur when the Plone registry is not available yet.
        # Example: trying to login as Zope admin in the ZMI and Unauthorized is
        # raised.
        # We cannot uninstall the monley patch unless we are sure logbook it is
        # disabled, otherwise we'll miss errors until logbook is enabled again.
        log(">>> Catched ComponentLookupError: No Plone Site installed?", "ERROR")
        pass

    enty_url = _raising(self, info)
    notify(ErrorRaisedEvent(self, enty_url))
    return enty_url
