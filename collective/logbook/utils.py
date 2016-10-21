# -*- coding: utf-8 -*-
#
# File: utils.py
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

__author__    = 'Ramon Bartl <ramon.bartl@inquant.de>'
__docformat__ = 'plaintext'

import re

from email.MIMEText import MIMEText
from email.Header import Header
from email.Utils import parseaddr, formataddr
from socket import gaierror

from plone.registry.interfaces import IRegistry
from zope.component import getUtility

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode

from config import LOGGER

REGEX = re.compile(r'0x[0-9a-fA-F]+')


def hexfilter(text):
    """ unify hex numbers
    """
    return REGEX.sub('0x0000000', text)


def filtered_error_tail(error):
    """ last 5 lines of traceback with replaced oid's
    """
    tb_text = error.get('tb_text', '')
    tail = tb_text.splitlines()[-5:]
    filtered_tail = map(hexfilter, tail)
    return filtered_tail

# this is stolen from http://grok.zope.org/documentation/how-to/automatic-form-generation
expr = re.compile(r"^(\w&.%#$&'\*+-/=?^_`{}|~]+!)*[\w&.%#$&'\*+-/=?^_`{}|~]+"
                  r"@(([0-9a-z]([0-9a-z-]*[0-9a-z])?\.)+[a-z]{2,6}|([0-9]{1,3}"
                  r"\.){3}[0-9]{1,3})$", re.IGNORECASE)

check_email = expr.match


def send(portal, message, subject, recipients=[]):
    """Send an email.

    this is taken from Products.eXtremeManagement
    """
    # Weed out any empty strings.
    recipients = [r for r in recipients if r]
    if not recipients:
        LOGGER.warn("No recipients to send the mail to, not sending.")
        return

    charset = portal.getProperty('email_charset', 'ISO-8859-1')
    # Header class is smart enough to try US-ASCII, then the charset we
    # provide, then fall back to UTF-8.
    header_charset = charset

    # We must choose the body charset manually
    for body_charset in 'US-ASCII', charset, 'UTF-8':
        try:
            message = message.encode(body_charset)
        except UnicodeError:
            pass
        else:
            break
        
    # Get the 'From' address.
    registry = getUtility(IRegistry)
    sender_name = registry.get('plone.email_from_name')
    sender_addr = registry.get('plone.email_from_address')

    # We must always pass Unicode strings to Header, otherwise it will
    # use RFC 2047 encoding even on plain ASCII strings.
    sender_name = str(Header(safe_unicode(sender_name), header_charset))
    # Make sure email addresses do not contain non-ASCII characters
    sender_addr = sender_addr.encode('ascii')
    email_from = formataddr((sender_name, sender_addr))

    formatted_recipients = []
    for recipient in recipients:
        # Split real name (which is optional) and email address parts
        recipient_name, recipient_addr = parseaddr(recipient)
        recipient_name = str(Header(safe_unicode(recipient_name),
                                    header_charset))
        recipient_addr = recipient_addr.encode('ascii')
        formatted = formataddr((recipient_name, recipient_addr))
        formatted_recipients.append(formatted)
    email_to = ', '.join(formatted_recipients)

    # Make the subject a nice header
    subject = Header(safe_unicode(subject), header_charset)

    # Create the message ('plain' stands for Content-Type: text/plain)

    # plone4 should use 'text/plain' according to the docs, but this should work for us
    # http://plone.org/documentation/manual/upgrade-guide/version/upgrading-plone-3-x-to-4.0/updating-add-on-products-for-plone-4.0/mailhost.securesend-is-now-deprecated-use-send-instead/
    msg = MIMEText(message, 'html', body_charset)
    msg['From'] = email_from
    msg['To'] = email_to
    msg['Subject'] = subject
    msg = msg.as_string()

    # Finally send it out.
    mailhost = getToolByName(portal, 'MailHost')
    try:
        LOGGER.info("Begin sending email to %r " % formatted_recipients)
        LOGGER.info("Subject: %s " % subject)
        mailhost.send(msg)
    except gaierror, exc:
        LOGGER.error("Failed sending email to %r" % formatted_recipients)
        LOGGER.error("Reason: %s: %r" % (exc.__class__.__name__, str(exc)))
    else:
        LOGGER.info("Succesfully sent email to %r" % formatted_recipients)

# vim: set ft=python ts=4 sw=4 expandtab :
