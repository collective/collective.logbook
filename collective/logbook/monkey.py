# -*- coding: utf-8 -*-
#
# File: monkey.py
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

# vim: set ft=python ts=4 sw=4 expandtab :
