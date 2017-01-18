# -*- coding: utf-8 -*-

from zope.i18nmessageid import MessageFactory

from collective.logbook import monkey

logbookMessageFactory = MessageFactory('collective.logbook')


def initialize(context):
    """ Initializer called when used as a Zope 2 product. """

    # Install the monkeypatch always, as we can not ask the Plone registry if
    # logbook logging is enabled or not. The patched raising event will check
    # this and uninstall the monkey patch if logging is disabled (see monkey.py).
    monkey.install_monkey()
