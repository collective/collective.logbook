# -*- coding: utf-8 -*-

from zope import interface
from zope import schema

from plone.z3cform import layout

from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper

from collective.logbook.utils import log
from collective.logbook.utils import check_email
from collective.logbook.monkey import install_monkey
from collective.logbook.monkey import uninstall_monkey
from collective.logbook import logbookMessageFactory as _


class ILogbookSchema(interface.Interface):
    """Schema for the Logbook Control Panel Form
    """

    logbook_enabled = schema.Bool(title=_(u'Enable Logbook logging'),
                                  description=_(u''),
                                  default=True,
                                  required=True)

    logbook_large_site = schema.Bool(title=_(u'Enable large site'),
                                     description=_(u'If you have a large site, the number '
                                                   'of errors might increase quickly. This will change '
                                                   'some functionalities so that logbook remains usable.'),
                                     default=False,
                                     required=True)

    logbook_log_mails = schema.Tuple(title=_(u'Notify Email'),
                                     description=_(u'Notify these Email Adresses '
                                                   'when a new error occurs'),
                                     unique=True,
                                     default=(),
                                     value_type=schema.TextLine(constraint=check_email, ),
                                     required=False)

    logbook_webhook_urls = schema.Tuple(title=_(u'Webhook Urls'),
                                        description=_(u'HTTP POST these URLs '
                                                      'when a new error occurs. One URL per line.'),
                                        unique=True,
                                        default=(),
                                        value_type=schema.TextLine(),
                                        required=False)


class LogbookControlPanelForm(RegistryEditForm):
    schema = ILogbookSchema
    schema_prefix = "logbook"
    label = _(u"Logbook settings")
    description = _(u"Logbook settings.")
    form_name = _(u"Logbook settings")

    # def updateFields(self):
    #     super(LogbookControlPanelForm, self).updateFields()
    #     log("LogbookControlPanelForm::updateFields")

    # def update(self):
    #     super(LogbookControlPanelForm, self).update()
    #     log("LogbookControlPanelForm::update")

    def applyChanges(self, data):
        super(LogbookControlPanelForm, self).applyChanges(data)
        log("LogbookControlPanelForm::applyChanges:data=%r" % data)

        logbook_enabled = data.get("logbook_enabled")
        if logbook_enabled:
            install_monkey()
        else:
            uninstall_monkey()


LogbookControlPanelView = layout.wrap_form(
    LogbookControlPanelForm, ControlPanelFormWrapper)
