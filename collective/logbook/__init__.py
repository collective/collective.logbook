# -*- coding: utf-8 -*-
#
# File: __init__.py
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

from zope.i18nmessageid import MessageFactory

from collective.logbook import monkey
from collective.logbook.config import LOGGER

#from plone.registry.interfaces import IRegistry
#from zope.component import getUtility

logbookMessageFactory = MessageFactory('collective.logbook')


def initialize(context):
    """ Initializer called when used as a Zope 2 product. """

    # The registry isn't available at that time, so for
    # now assume it's always enabled.
    
    #registry = getUtility(IRegistry)
    #enabled = registry.get('logbook.logbook_enabled')
    enabled = True

    if enabled:
        monkey.install_monkey()
        LOGGER.info(">>> logging **enabled**")
    else:
        LOGGER.info(">>> logging **disabled**")

# vim: set ft=python ts=4 sw=4 expandtab :
