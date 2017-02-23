# -*- coding: utf-8 -*-

from zope.i18nmessageid import MessageFactory

from collective.logbook import monkey

logbookMessageFactory = MessageFactory('collective.logbook')


def initialize(context):
    """Initializer called when used as a Zope 2 product.
    """
    # Note: Component Registry is not ready at this stage, so we can not query
    #       the Plone registry to see if logbook logging is enabled or not.
    #
    #       => Install the monkeypatch always. The patched raising event will
    #          check later the Plone registry and will uninstall the monkey
    #          patch if logging is disabled (see monkey.py).
    monkey.install_monkey()
