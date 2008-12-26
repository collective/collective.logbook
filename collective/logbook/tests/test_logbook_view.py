# -*- coding: utf-8 -*-
#
# File: test_views.py
#
# Copyright (c) InQuant GmbH
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

__author__ = 'Ramon Bartl <ramon.bartl@inquant.de>'
__docformat__ = 'plaintext'

import unittest

from zope import interface

from Products.CMFCore.utils import getToolByName

from zff.jc.job.tests.base import ZFFTestCase
from zff.jc.job.interfaces import IXMLRPCView
from zff.jc.job.browser.xmlrpcview import XMLRPCView


class TestSetup(ZFFTestCase):

    def afterSetUp(self):
        self.setRoles(('Manager', ))
        self.types = getToolByName(self.portal, 'portal_types')
        # Fake global allow for job ct
        job_fti = getattr(self.types, 'Job')
        job_fti.global_allow = True
        _ = self.folder.invokeFactory('Job', 'testjob')
        self.testjob = self.folder.get(_)

    def test_view_implements_interface(self):
        view = XMLRPCView(self.portal, None)
        self.failUnless(IXMLRPCView.providedBy(view))

    def test_view_class_fulfills_interface_contract(self):
        self.failUnless(interface.verify.verifyClass(IXMLRPCView, XMLRPCView))

    def test_view_object_fulfills_interface_contract(self):
        view = XMLRPCView(self.portal, None)
        self.failUnless(interface.verify.verifyObject(IXMLRPCView, view))

    def test_view_registered_for_job_ct(self):
        self.failUnless(self.testjob.restrictedTraverse('@@xmlrpc'))

    # Test View Methods
    def test_view_method_add_message(self):
        view = self.testjob.restrictedTraverse('@@xmlrpc')
        self.assertEqual(len(self.testjob.getMessages()), 0)

        view.add_message('MUHAHAHA')
        self.assertEqual(len(self.testjob.getMessages()), 1)

        self.assertEqual(self.testjob.messages, ('MUHAHAHA',))


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite

# vim: set ft=python ts=4 sw=4 expandtab :

