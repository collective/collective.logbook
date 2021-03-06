# -*- coding: utf-8 -*-

import unittest

from collective.logbook.browser.logbook import LogBook
from collective.logbook.interfaces import ILogBook
from collective.logbook.tests.base import LogBookTestCase
from zope.interface import verify


class TestViews(LogBookTestCase):
    """ Test View Class
    """

    def afterSetUp(self):
        self.setRoles(('Manager', ))

    def test_view_implements_interface(self):
        view = LogBook(self.portal, None)
        self.assertTrue(ILogBook.providedBy(view))

    def test_view_class_fulfills_interface_contract(self):
        self.assertTrue(verify.verifyClass(ILogBook, LogBook))


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestViews))
    return suite
