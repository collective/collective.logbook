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

from plone.z3cform import layout

from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.formlib.schema import SchemaAdapterBase

from Products.CMFPlone.interfaces import IPloneSiteRoot
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm

from collective.logbook.utils import check_email
from collective.logbook.monkey import install_monkey
from collective.logbook.monkey import uninstall_monkey
from collective.logbook import logbookMessageFactory as _


class ILogbookSchema(interface.Interface):
    """ Combined schema for the adapter lookup.
    """

    # logbook_enabled = schema.Bool(
    #                     title=_(u'Enable Logbook logging'),
    #                     description=_(u'This installs or uninstalls '
    #                     'the logbook patch for Products.SiteErrorLog.'
    #                     'Please restart your Zope instance after changing it.'),
    #                     default=True,
    #                     required=True)

    logbook_large_site = schema.Bool(
                        title=_(u'Enable large site'),
                        description=_(u'If you have a large site, the number '
                            'of errors might increase quickly. This will change '
                            'some functionalities so that logbook remains usable.'),
                        default=False,
                        required=True)

    logbook_log_mails = schema.Tuple(
                        title=_(u'Notify Email'),
                        description=_(u'Notify these Email Adresses '
                            'when a new error occurs'),
                        unique=True,
                        default=(),
                        value_type=schema.TextLine(
                                     constraint=check_email, ),
                        required=False,
                        )

    logbook_webhook_urls = schema.Tuple(
                        title=_(u'Webhook Urls'),
                        description=_(u'HTTP POST these URLs '
                            'when a new error occurs. One URL per line.'),
                        unique=True,
                        default=(),
                        value_type=schema.TextLine(),
                        required=False,
                        )

    # @apply
    # def logbook_enabled():

    #         if value:
    #             install_monkey()
    #         else:
    #             uninstall_monkey()


class LogbookControlPanelForm(RegistryEditForm):
    schema = ILogbookSchema
    schema_prefix = "logbook"
    label = _(u"Logbook settings")
    description = _(u"Logbook settings.")
    form_name = _(u"Logbook settings")

LogbookControlPanelView = layout.wrap_form(
    LogbookControlPanelForm, ControlPanelFormWrapper)
    
# vim: set ft=python ts=4 sw=4 expandtab :
