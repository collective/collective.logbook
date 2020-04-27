# -*- coding: utf-8 -*-

import doctest

import unittest2 as unittest
from collective.logbook.tests.base import LogBookFunctionalTestCase
from Testing import ZopeTestCase as ztc


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        ztc.ZopeDocFileSuite(
            '../../../README.rst',
            test_class=LogBookFunctionalTestCase,
            optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE,
        ),
    ])
    return suite
