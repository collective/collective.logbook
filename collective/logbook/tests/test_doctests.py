# -*- coding: utf-8 -*-

import doctest

import unittest2 as unittest

from Testing import ZopeTestCase as ztc

from collective.logbook.tests.base import LogBookTestCase


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        ztc.ZopeDocFileSuite(
            '../../../README.rst',
            test_class=LogBookTestCase,
            optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE,
        ),
    ])
    return suite
