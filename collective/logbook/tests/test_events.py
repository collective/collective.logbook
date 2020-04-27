# -*- coding: utf-8 -*-

import sys
import unittest

from Acquisition import ImplicitAcquisitionWrapper
from Acquisition import aq_acquire
from collective.logbook.interfaces import ILogBookStorage
from collective.logbook.tests.base import LogBookFunctionalTestCase
from plone import api


class TestEvents(LogBookFunctionalTestCase):
    """ Test the event handlers

    Implementation note: Since the `events.handleTraceback` calls
    `transaction.commit` these tests must belong to the functional test layer,
    even if no test browser stuff is used. If these tests were in the
    integration layer some isolation issues would arise.
    """

    def test_error_is_logged(self):
        prefix = 'test0_'
        self.assertEqual(len(self._get_errors_by_prefix(prefix)), 0)
        self._simulate_error(prefix + '0')
        self.assertEqual(len(self._get_errors_by_prefix(prefix)), 1)
        self._simulate_error(prefix + '1')
        self.assertEqual(len(self._get_errors_by_prefix(prefix)), 2)

    def test_error_is_logged_with_acquisition_wrapped_context(self):
        # Note: this is a regression test for issue #11:
        # Error in unknown conditions: TypeError:
        #   Can't pickle objects in acquisition wrappers

        folder = api.content.create(
            container=self.portal, type='Folder', title='Folder 0')
        aq_wrapped_folder = ImplicitAcquisitionWrapper(folder, self.portal)

        prefix = 'test1_'
        self.assertEqual(len(self._get_errors_by_prefix(prefix)), 0)
        self._simulate_error(prefix + '0')
        self.assertEqual(len(self._get_errors_by_prefix(prefix)), 1)
        self._simulate_error(prefix + '1', context=aq_wrapped_folder)
        self.assertEqual(len(self._get_errors_by_prefix(prefix)), 2)

    def test_error_is_logged_when_acessing_view_method_directly(self):
        # Note: this is a regression test for issue #19: "Cannot handle traceback when error occurs
        # when accessing a method of a view".

        view = self.portal.unrestrictedTraverse('@@plone_portal_state')
        aq_wrapped_view = ImplicitAcquisitionWrapper(view, self.portal)
        prefix = 'test1_'
        self.assertEqual(len(self._get_errors_by_prefix(prefix)), 0)
        self._simulate_error(prefix + '0')
        self.assertEqual(len(self._get_errors_by_prefix(prefix)), 1)

        # Simulate the failure mode by setting the error context as the view itself.
        self._simulate_error(prefix + '1', context=aq_wrapped_view)
        self.assertEqual(len(self._get_errors_by_prefix(prefix)), 2)

    def _simulate_error(self, msg='Dummy error', context=None):
        try:
            raise RuntimeError(msg)
        except RuntimeError:
            # Acquire the error_log object the same way Zope does. See module: Zope2.App.startup
            error_log = aq_acquire(self.portal, '__error_log__', containment=1)
            error_log.raising(sys.exc_info())

    def _get_errors_by_prefix(self, prefix):
        storage = ILogBookStorage(self.portal)
        return [
            (k, v)
            for (k, v)
            in storage.get_all_errors()
            if (v.get('value') or '').startswith(prefix)
        ]


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestEvents))
    return suite
