# -*- coding: utf-8 -*-

from collective.logbook.config import PACKAGENAME
from collective.logbook.monkey import install_monkey
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_ROLES
from plone.app.testing import setRoles
from plone.app.testing.layers import IntegrationTesting
from plone.testing import z2
from plone.testing.z2 import Browser
import pkg_resources
import unittest

try:
    pkg_resources.get_distribution('plone.protect')
    import plone.protect.auto
except (pkg_resources.DistributionNotFound, ImportError):
    HAS_PLONE_PROTECT = False
else:
    HAS_PLONE_PROTECT = True


class TestLayer(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import collective.logbook
        self.loadZCML(package=collective.logbook)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, '{}:default'.format(PACKAGENAME))


TEST_FIXTURE = TestLayer()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(TEST_FIXTURE,),
    name='{}:Integration'.format(PACKAGENAME))
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(TEST_FIXTURE,),
    name='{}:Functional'.format(PACKAGENAME))

ROBOT_TESTING = FunctionalTesting(
    bases=(TEST_FIXTURE, AUTOLOGIN_LIBRARY_FIXTURE, z2.ZSERVER_FIXTURE),
    name='{}:Robot'.format(PACKAGENAME))


class LogBookTestCase(unittest.TestCase):
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer.get('app')
        self.portal = self.layer.get('portal')
        setRoles(self.portal, TEST_USER_ID, TEST_USER_ROLES + ['Manager'])

        # Disable auto protection for tests
        if HAS_PLONE_PROTECT:
            plone.protect.auto.CSRF_DISABLED = True

        install_monkey()

    def getBrowser(self, handleErrors=False):
        browser = Browser(self.app)
        if handleErrors:
            browser.handleErrors = True
        return browser

    def getApp(self):
        return self.layer.get('app')

    def getPortal(self):
        return self.layer.get('portal')

    def getRequest(self):
        return self.layer.get('request')


class LogBookFunctionalTestCase(LogBookTestCase):
    layer = FUNCTIONAL_TESTING
