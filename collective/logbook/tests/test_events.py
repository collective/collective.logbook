# -*- coding: utf-8 -*-

from plone import api
import sys
import unittest

from collective.logbook.interfaces import ILogBookStorage
from collective.logbook.tests.base import LogBookFunctionalTestCase


class TestEvents(LogBookFunctionalTestCase):
    """ Test the event handlers

    Implementation note: Since the `events.handleTraceback` calls `transaction.commit` these tests
    must belong to the functional test layer, even if no test browser stuff is used. If these
    tests were in the integration layer some isolation issues would arise.
    """

    def test_error_is_logged(self):
        prefix = 'test0_'
        self.assertEqual(len(self._get_errors_by_prefix(prefix)), 0)
        self._simulate_error(prefix + '0')
        self.assertEqual(len(self._get_errors_by_prefix(prefix)), 1)
        self._simulate_error(prefix + '1')
        self.assertEqual(len(self._get_errors_by_prefix(prefix)), 2)

    def test_error_is_logged_with_acquisition_wrapped_context(self):
        # Note: this is a regression test for a bug that occurs when the context of the error
        # is inside an acquisition wrapper.

        folder = api.content.create(container=self.portal, type='Folder', title='Folder 0')

        prefix = 'test1_'
        self.assertEqual(len(self._get_errors_by_prefix(prefix)), 0)
        self._simulate_error(prefix + '0')
        self.assertEqual(len(self._get_errors_by_prefix(prefix)), 1)
        self._simulate_error(prefix + '1', context=folder)
        self.assertEqual(len(self._get_errors_by_prefix(prefix)), 2)

    def _simulate_error(self, msg='Dummy error', context=None):
        try:
            raise RuntimeError(msg)
        except RuntimeError:
            context = context if (context is not None) else self.portal
            error_log = context.unrestrictedTraverse('error_log')
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
