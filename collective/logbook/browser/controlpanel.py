# -*- coding: utf-8 -*-
#
# File: controlpanel.py
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

from zope import interface
from zope import schema
from zope import component
from zope.formlib import form
from zope.app.component import hooks

from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.formlib.schema import SchemaAdapterBase

from Products.CMFPlone.interfaces import IPloneSiteRoot
from plone.app.controlpanel.form import ControlPanelForm

from collective.logbook.utils import check_email
from collective.logbook.monkey import install_monkey
from collective.logbook.monkey import uninstall_monkey
from collective.logbook import logbookMessageFactory as _

from collective.logbook.config import PROP_KEY_LOG_ENABLED
from collective.logbook.config import PROP_KEY_LOG_MAILS


class ILogbookSchema(interface.Interface):
    """ Combined schema for the adapter lookup.
    """

    logbook_enabled = schema.Bool(
                        title = _(u'Enable Logbook logging'),
                        description = _(u'This installs or uninstalls the logbook patch for Products.SiteErrorLog'),
                        default = True,
                        required = True)

    logbook_log_mails = schema.Tuple(
                        title = _(u'Notify Email'),
                        description = _(u'Notify these Email Adresses when a new error occurs'),
                        unique = True,
                        default = (),
                        value_type = schema.TextLine(
                                     constraint = check_email, ),
                        )


class LogbookControlPanelAdapter(SchemaAdapterBase):
    component.adapts(IPloneSiteRoot)
    interface.implements(ILogbookSchema)

    def __init__(self, context):
        super(LogbookControlPanelAdapter, self).__init__(context)
        self.context = getToolByName(self.context, "portal_properties").site_properties
        self.portal = hooks.getSite()
        self.app = self.portal.getParentNode()

    @apply
    def logbook_enabled():

        def get(self):
            return self.app.getProperty(PROP_KEY_LOG_ENABLED)

        def set(self, value):

            if value:
                install_monkey()
            else:
                uninstall_monkey()

            return self.app.manage_changeProperties(logbook_enabled = value)

        return property(get, set)

    @apply
    def logbook_log_mails():

        def get(self):
            return self.app.getProperty(PROP_KEY_LOG_MAILS) or ()

        def set(self, value):
            self.app.manage_changeProperties(logbook_log_mails = value)

        return property(get, set)


class LogbookControlPanel(ControlPanelForm):
    form_fields = form.FormFields(ILogbookSchema)
    label = _(u"Logbook settings")
    description = _(u"Logbook settings.")
    form_name = _(u"Logbook settings")

# vim: set ft=python ts=4 sw=4 expandtab :
