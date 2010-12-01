from Products.CMFCore.utils import getToolByName

from collective.logbook.config import PROP_KEY_LOG_MAILS
from collective.logbook.utils import send


class MailView(object):

    def __call__(self, event):
        error = event.error
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        app = portal.getPhysicalRoot()
        emails = app.getProperty(PROP_KEY_LOG_MAILS)

        if not emails:
            return

        recipients = [mail for mail in emails]
        subject = "[collective.logbook] NEW TRACEBACK: '%s'" % (
            error.get("value"))
        self.__dict__.update(
            date=error.get("time").strftime("%Y-%m-%d %H:%M:%S"),
            traceback=error.get("tb_text"),
            error_number=error.get("id"),
            error_url=error.get("url"),
            logbook_url=(
                portal.absolute_url() + "/@@logbook?errornumber=%s" %
                error.get("id")),
            req_html=error.get("req_html"),
            )

        message = self.index()
        send(portal, message, subject, recipients)
