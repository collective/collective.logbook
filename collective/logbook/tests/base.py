# -*- coding: utf-8 -*-

import unittest2 as unittest

from plone.testing.z2 import Browser

from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing.layers import IntegrationTesting
from plone.app.testing import quickInstallProduct
from zope.configuration import xmlconfig


class TestLayer(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import collective.logbook
        xmlconfig.file('configure.zcml', collective.logbook,
                       context=configurationContext)

    def setUpPloneSite(self, portal):
        quickInstallProduct(portal, "collective.logbook")


TEST_FIXTURE = TestLayer()
INTEGRATION_TESTING = IntegrationTesting(bases=(TEST_FIXTURE,),
                                         name="collective.logbook:Integration")


class LogBookTestCase(unittest.TestCase):
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer.get("app")
        self.portal = portal = self.layer.get("portal")
        portal.acl_users.userFolderAddUser('admin', 'secret', ['Manager', ], [])
        setRoles(portal, 'admin', ['Manager'])
        login(portal, 'admin')

    def getBrowser(self, handleErrors=False):
        browser = Browser(self.app)
        if handleErrors:
            browser.handleErrors = True
        return browser
