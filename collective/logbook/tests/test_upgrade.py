# -*- coding: utf-8 -*-

import unittest

from collective.logbook.browser.controlpanel import ILogbookSchema
from collective.logbook.tests.base import LogBookTestCase

from plone import api

from Products.GenericSetup.upgrade import _upgrade_registry


class TestUpgrade(LogBookTestCase):
    """ Test Upgrade Steps
    """

    def afterSetUp(self):
        self.setRoles(('Manager', ))

    def test_upgrade_from_2_to_3(self):
        registry = api.portal.get_tool('portal_registry')
        prefix = 'logbook.'
        logbook_fields = set((prefix + f) for f in ILogbookSchema)

        # Delete all records from registry.
        for f in logbook_fields:
            del registry.records[f]

        # Run upgrade and see if the records are restored.
        self.assertTrue(self._upgrade_add_on('2', '3'))
        self.assertTrue(logbook_fields.issubset(set(registry.records.keys())))

        # We want it to be idempotent so we check again.
        self.assertTrue(self._upgrade_add_on('2', '3'))
        self.assertTrue(logbook_fields.issubset(set(registry.records.keys())))

    def _upgrade_add_on(
        self,
        source,
        destination,
        add_on_name='collective.logbook',
        profile='default'
    ):
        u"""Run the upgrade steps for an add-on.

        Arguments:
        add_on_name -- Add-on name. Eg.: "my.package".
        profile -- Generic Setup profile. Eg.: "default".
        source -- Source version (string). Eg.: "1".
        destination -- Destination version (string). Eg.: "2".

        Return: boolean which is true if and only if at least one upgrade step
                ran.
        """
        setup = api.portal.get_tool('portal_setup')
        full_profile_id = u'{}:{}'.format(add_on_name, profile)
        ran = False
        groups = _upgrade_registry.getUpgradeStepsForProfile(full_profile_id)
        for step_or_steps in groups.values():
            try:
                steps = sorted([s[1] for s in step_or_steps], key=lambda x: x.sortkey)
            except TypeError:
                steps = [step_or_steps]
            for step in steps:
                if (source in step.source) and (destination in step.dest):
                    step.doStep(setup)
                    ran = True

        return ran


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestUpgrade))
    return suite
