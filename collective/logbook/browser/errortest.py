# -*- coding: utf-8 -*-

import random

ERRORS = [ValueError, KeyError, RuntimeError, ImportError, AttributeError, AssertionError, IndexError, IOError]


class ErrorTestView(object):
    """Raise a test error for collective.logbook
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        raise RuntimeError("collective.logbook test error")


class RandomErrorTestView(object):
    """Raise a random error for collective.logbook
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        raise random.choice(ERRORS)("collective.logbook test error")
