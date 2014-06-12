# -*- coding: utf-8 -*-

import unittest

from zope import interface

from collective.logbook.tests.base import LogBookTestCase
from collective.logbook.storage import LogBookStorage
from collective.logbook.interfaces import ILogBookStorage

# errors
MockError1 = dict(id=111, tb_text="Traceback1")
MockError2 = dict(id=222, tb_text="Traceback2")
MockError3 = dict(id=333, tb_text="Traceback3")

# errors which occured twice (same traceback)
MockError11 = dict(id=444, tb_text="Traceback1")
MockError22 = dict(id=555, tb_text="Traceback2")
MockError33 = dict(id=666, tb_text="Traceback3")


class TestStorage(LogBookTestCase):
    """ Test View Class
    """

    def afterSetUp(self):
        self.setRoles(('Manager', ))

    def test_storage_adapter_registered(self):
        self.failUnless(ILogBookStorage(self.portal))

    def test_adapter_implements_interface(self):
        adapter = ILogBookStorage(self.portal)
        self.failUnless(ILogBookStorage.providedBy(adapter))

    def test_adapter_class_fulfills_interface_contract(self):
        self.failUnless(interface.verify.verifyClass(ILogBookStorage, LogBookStorage))

    def test_save_error(self):
        adapter = ILogBookStorage(self.portal)
        self.failUnless(adapter.save_error(MockError1))

    def test_delete_error(self):
        adapter = ILogBookStorage(self.portal)
        adapter.save_error(MockError1)
        self.assertEqual(adapter.error_count, 1)
        self.failUnless(adapter.delete_error(MockError1.get("id")))
        self.assertEqual(adapter.error_count, 0)

    def test_get_error(self):
        adapter = ILogBookStorage(self.portal)
        adapter.save_error(MockError1)
        self.failUnless(adapter.get_error(MockError1.get("id")))

    def test_get_all_errors(self):
        adapter = ILogBookStorage(self.portal)
        adapter.save_error(MockError1)
        adapter.save_error(MockError2)
        adapter.save_error(MockError3)
        errors = adapter.get_all_errors()
        self.assertEqual(len(errors), 3)

    def test_delete_all_errors(self):
        adapter = ILogBookStorage(self.portal)
        adapter.save_error(MockError1)
        adapter.save_error(MockError2)
        adapter.save_error(MockError3)
        self.assertEqual(adapter.error_count, 3)
        adapter.delete_all_errors()
        self.assertEqual(adapter.error_count, 0)

    def test_referenced_errors(self):
        adapter = ILogBookStorage(self.portal)
        # these errors occured once
        adapter.save_error(MockError1)
        adapter.save_error(MockError2)
        adapter.save_error(MockError3)
        # 3 unique errors and 0 referenced errors
        self.assertEqual(adapter.error_count, 3)
        self.assertEqual(adapter.reference_count, 0)
        # now we have some already occured errors
        adapter.save_error(MockError11)
        adapter.save_error(MockError22)
        adapter.save_error(MockError33)
        self.assertEqual(adapter.error_count, 3)
        self.assertEqual(adapter.reference_count, 3)

    def test_delete_reference(self):
        adapter = ILogBookStorage(self.portal)
        # 3 unique, 1 referenced error
        adapter.save_error(MockError1)
        adapter.save_error(MockError2)
        adapter.save_error(MockError3)
        adapter.save_error(MockError11)

        # check
        self.assertEqual(adapter.error_count, 3)
        self.assertEqual(adapter.reference_count, 1)

        # delete referenced error
        self.failUnless(adapter.delete_error(MockError1.get("id")))

        # check
        self.assertEqual(adapter.error_count, 2)
        self.assertEqual(adapter.reference_count, 0)

    def test_delete_all_references(self):
        adapter = ILogBookStorage(self.portal)

        # 3 unique, 3 referenced errors
        adapter.save_error(MockError1)
        adapter.save_error(MockError2)
        adapter.save_error(MockError3)
        adapter.save_error(MockError11)
        adapter.save_error(MockError22)
        adapter.save_error(MockError33)

        # check
        self.assertEqual(adapter.error_count, 3)
        self.assertEqual(adapter.reference_count, 3)

        # delete all referenced error
        adapter.delete_all_references()

        # check
        self.assertEqual(adapter.error_count, 3)
        self.assertEqual(adapter.reference_count, 0)

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestStorage))
    return suite

# vim: set ft=python ts=4 sw=4 expandtab :
