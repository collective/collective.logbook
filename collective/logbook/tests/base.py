# -*- coding: utf-8 -*-

import pkg_resources

import unittest2 as unittest

from plone.testing import z2
from plone.testing.z2 import Browser

from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing.layers import IntegrationTesting
from plone.app.testing import quickInstallProduct
from zope.configuration import xmlconfig

from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE

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
        xmlconfig.file('configure.zcml', collective.logbook,
                       context=configurationContext)

    def tearDownZope(self, app):
        # Uninstall product
        z2.uninstallProduct(app, 'collective.logbook')

    def setUpPloneSite(self, portal):
        quickInstallProduct(portal, "collective.logbook")


TEST_FIXTURE = TestLayer()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(TEST_FIXTURE,),
    name="collective.logbook:Integration")

ROBOT_TESTING = FunctionalTesting(
    bases=(TEST_FIXTURE, AUTOLOGIN_LIBRARY_FIXTURE, z2.ZSERVER_FIXTURE),
    name="collective.logbook:Robot")


class LogBookTestCase(unittest.TestCase):
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer.get("app")
        self.portal = portal = self.layer.get("portal")
        portal.acl_users.userFolderAddUser('admin', 'secret', ['Manager', ], [])
        setRoles(portal, 'admin', ['Manager'])
        login(portal, 'admin')

        # Disable auto protection for tests
        if HAS_PLONE_PROTECT:
            plone.protect.auto.CSRF_DISABLED = True

    def getBrowser(self, handleErrors=False):
        browser = Browser(self.app)
        if handleErrors:
            browser.handleErrors = True
        return browser

    def getApp(self):
        return self.layer.get("app")

    def getPortal(self):
        return self.layer.get("portal")

    def getRequest(self):
        return self.layer.get("request")
