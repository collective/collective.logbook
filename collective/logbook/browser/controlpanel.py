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

import Zope2

from zope import interface
from zope import schema
from zope import component
from zope.formlib import form

from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.formlib.schema import SchemaAdapterBase

from Products.CMFPlone.interfaces import IPloneSiteRoot
from plone.app.controlpanel.form import ControlPanelForm

from collective.logbook.config import PROP_KEY
from collective.logbook.monkey import install_monkey
from collective.logbook.monkey import uninstall_monkey
from collective.logbook import logbookMessageFactory as _


class ILogbookSchema(interface.Interface):
    """ Combined schema for the adapter lookup.
    """

    logbook_enabled = schema.Bool(
                        title = _(u'label_logbook_enabled', default = u'Enable Logbook logging'),
                        description = _(u"help_logbook_enabled", default = u'This installs or uninstalls the logbook patch for Products.SiteErrorLog'),
                        default = True,
                        required = True)


class LogbookControlPanelAdapter(SchemaAdapterBase):
    component.adapts(IPloneSiteRoot)
    interface.implements(ILogbookSchema)

    def __init__(self, context):
        super(LogbookControlPanelAdapter, self).__init__(context)
        self.context = getToolByName(self.context, "portal_properties").site_properties

    @apply
    def logbook_enabled():
        app = Zope2.app()
        def get(self):
            return app.getProperty(PROP_KEY)

        def set(self, value):
            if value:
                install_monkey()
            else:
                uninstall_monkey()
            return app.manage_changeProperties(logbook_enabled = value)

        return property(get, set)


class LogbookControlPanel(ControlPanelForm):
    form_fields = form.FormFields(ILogbookSchema)
    label = _(u"Logbook settings")
    description = _(u"Logbook settings.")
    form_name = _(u"Logbook settings")

# vim: set ft=python ts=4 sw=4 expandtab :
