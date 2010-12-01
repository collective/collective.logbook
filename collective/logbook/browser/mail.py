from collective.logbook.config import PROP_KEY_LOG_MAILS
from collective.logbook.utils import send


class MailView(object):

    def __call__(self, event):
        error = event.error
        portal = self.context
        app = portal.getParentNode()
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
            request=error.get("req_html"),
            )

        message = super(MailView, self).__call__()
        send(portal, message, subject, recipients)
