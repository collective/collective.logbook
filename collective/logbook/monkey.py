# -*- coding: utf-8 -*-

from zope.event import notify

from Products.SiteErrorLog.SiteErrorLog import SiteErrorLog

from config import LOGGER
from events import ErrorRaisedEvent

_raising = SiteErrorLog.raising


def install_monkey():
    LOGGER.info(">>> Installing Monkey for Products.SiteErrorLog")
    SiteErrorLog.raising = raising


def uninstall_monkey():
    LOGGER.info(">>> Uninstalling Monkey for Products.SiteErrorLog")
    SiteErrorLog.raising = _raising


def raising(self, info):
    enty_url = _raising(self, info)
    notify(ErrorRaisedEvent(self, enty_url))
    return enty_url
