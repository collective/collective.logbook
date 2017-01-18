# -*- coding: utf-8 -*-

import re
import types
import logging

from plone import api as ploneapi

from collective.logbook.config import LOGGER
from collective.logbook.config import LOGLEVEL
from collective.logbook.config import HEX_REGEX


def get_portal():
    """Get the portal object

    :returns: Portal object
    :rtype: object
    """
    return ploneapi.portal.getSite()


def get_plone_version():
    """Get the Plone version

    :returns: Plone version
    :rtype: str or list
    """
    return ploneapi.env.plone_version()


def is_plone5():
    """Check for Plone 5 series

    :returns: True if Plone 5
    :rtype: boolean
    """
    version = get_plone_version()
    return version.startswith("5")


def is_patch_applied():
    """Checks if the monkey patch was already applied
    """
    from Products.SiteErrorLog.SiteErrorLog import SiteErrorLog
    from collective.logbook.monkey import raising

    return SiteErrorLog.raising.im_func is raising


def is_logbook_enabled():
    """Checks if logbook logging is enabled
    """
    return ploneapi.portal.get_registry_record("logbook.logbook_enabled")


def is_logbook_large_site_enabled():
    """Checks if logbook logging is enabled
    """
    return ploneapi.portal.get_registry_record("logbook.logbook_large_site")


def get_logbook_log_mails():
    """Returns the emails to notify on new errors
    """
    return ploneapi.portal.get_registry_record('logbook.logbook_log_mails')


def log(msg, level=LOGLEVEL):
    """Log the message
    """
    # get the numeric value of the level. defaults to 0 (NOTSET)
    level = logging._levelNames.get(level.upper(), 0)
    LOGGER.log(level, msg)


def send_email(message, subject, recipients):
    """Send the message to the list of recipients
    """
    log("Sending Email to %r" % recipients)

    # Handle a single recipient address gracefully
    if not is_list(recipients):
        recipients = [recipients]

    # Send email to all of the recipients
    for recipient in recipients:
        try:
            # Note: `plone.api.portal.send_email` takes care about the fetching
            #       the correct sender name and email address
            ploneapi.portal.send_email(
                recipient=recipient,
                subject=subject,
                body=message,
            )
        # Do not create another logbook error during the message sending
        except Exception, exc:
            log("Failed sending email to recipient(s): {} with error: {}".format(
                ",".join(recipients),
                str(exc)), level="error")


def is_list(thing):
    """ checks if an object is a list type

        >>> is_list([])
        True
        >>> is_list(list())
        True
        >>> is_list("[]")
        False
        >>> is_list({})
        False
    """
    return isinstance(thing, types.ListType)


def filtered_error_tail(error):
    """ last 5 lines of traceback with replaced oid's
    """
    tb_text = error.get('tb_text', '')
    tail = tb_text.splitlines()[-5:]
    filtered_tail = map(hexfilter, tail)
    return filtered_tail


def hexfilter(text):
    """ unify hex numbers
    """
    return HEX_REGEX.sub('0x0000000', text)


# this is stolen from http://grok.zope.org/documentation/how-to/automatic-form-generation
email_expr = re.compile(r"^(\w&.%#$&'\*+-/=?^_`{}|~]+!)*[\w&.%#$&'\*+-/=?^_`{}|~]+"
                        r"@(([0-9a-z]([0-9a-z-]*[0-9a-z])?\.)+[a-z]{2,6}|([0-9]{1,3}"
                        r"\.){3}[0-9]{1,3})$", re.IGNORECASE)

check_email = email_expr.match
