# -*- coding: utf-8 -*-


from collective.logbook.utils import get_portal
from collective.logbook.utils import send_email
from collective.logbook.utils import get_logbook_log_mails


class MailView(object):
    """
    """

    def __call__(self, event):
        error = event.error
        portal = get_portal()
        emails = get_logbook_log_mails()

        if not emails:
            return

        recipients = [mail for mail in emails if mail]

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
        send_email(message, subject, recipients)
