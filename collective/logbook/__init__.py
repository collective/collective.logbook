# -*- coding: utf-8 -*-

from zope.i18nmessageid import MessageFactory

from collective.logbook import monkey
from collective.logbook.config import LOGGER

# from plone.registry.interfaces import IRegistry
# from zope.component import getUtility

logbookMessageFactory = MessageFactory('collective.logbook')


def initialize(context):
    """ Initializer called when used as a Zope 2 product. """

    # The registry isn't available at that time, so for
    # now assume it's always enabled.

    # registry = getUtility(IRegistry)
    # enabled = registry.get('logbook.logbook_enabled')
    enabled = True

    if enabled:
        monkey.install_monkey()
        LOGGER.info(">>> logging **enabled**")
    else:
        LOGGER.info(">>> logging **disabled**")
