# -*- coding: utf-8 -*-

import unittest

from collective.logbook.tests.base import LogBookTestCase


class TestSetup(LogBookTestCase):
    """ Test Setup
    """

    def afterSetUp(self):
        self.setRoles(('Manager', ))

    def testViewAvailable(self):
        self.assertTrue(self.portal.restrictedTraverse('@@logbook'))


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite
