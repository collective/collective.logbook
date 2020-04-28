# -*- coding: utf-8 -*-

import unittest
import robotsuite
from plone.testing import layered

from collective.logbook.tests.base import ROBOT_TESTING


def test_suite():
    suite = unittest.TestSuite()
    # Disabling for Travis due to this failure (see .travis.yml):
    # The command "sh -e /etc/init.d/xvfb start" failed and exited with 127 during .
    # suite.addTests([
    #     layered(robotsuite.RobotTestSuite('robot_tests.txt'),
    #             layer=ROBOT_TESTING),
    # ])
    return suite
