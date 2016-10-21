from Products.CMFCore.utils import getToolByName
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

from collective.logbook.config import LOGGER

import threading
import urllib
import urllib2


class WebhookView(object):
    """
    Perform web hook HTTP POSTs.

    This view is called from events.py
    """

    def __call__(self, event):
        error = event.error
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        registry = getUtility(IRegistry)
        urls = registry.get('logbook.logbook_webhook_urls')

        if not urls:
            return

        subject = "[collective.logbook] NEW TRACEBACK: '%s'" % (
            error.get("value"))
        date = error.get("time").strftime("%Y-%m-%d %H:%M:%S"),
        traceback = "\n".join(error.get("tb_text").split("\n")[-3:])
        #error_number = error.get("id")
        error_url = error.get("url")
        logbook_url = (
            portal.absolute_url() + "/@@logbook?errornumber=%s" %
            error.get("id"))
        #req_html = error.get("req_html")

        message = "%s\n%s\n%s\n%s\n%s\n" % (
            subject, date, traceback,
            error_url, logbook_url)

        LOGGER.info("Calling webhooks")
        LOGGER.info("Webhook urls:\n%s" % ("\n".join(urls)))

        for url in urls:

            url = url.strip()

            # Emptry url
            if not url:
                continue

            t = UrlThread(url, {'data': message})
            t.start()


class UrlThread(threading.Thread):
    """
    Separate thread doing HTTP POST so we won't block
    """
    def __init__(self, url, data):
        threading.Thread.__init__(self)
        self.url = url
        self.data = data

    def run(self):
        try:
            self.data = urllib.urlencode(self.data)
            r = urllib2.urlopen(self.url, self.data)
            r.read()
        except Exception as e:
            LOGGER.error(e)
            LOGGER.exception(e)
