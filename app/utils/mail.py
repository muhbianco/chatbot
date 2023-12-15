import smtplib
import os
import ssl
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate


class SendEmail:
    def __init__(self):
        self.gmail_user = os.environ["EMAIL_USER"]
        self.gmail_app_password = os.environ["EMAIL_PASS"]
        self.sent_from = self.gmail_user

    def send_email(self, sent_to, sent_subject, sent_body, files = None):
        msg = MIMEMultipart()
        msg["From"] = self.sent_from
        msg["To"] = COMMASPACE.join(sent_to)
        msg["Data"] = formatdate(localtime=True)
        msg["Subject"] = sent_subject

        msg.attach(MIMEText(sent_body))

        if files:
            for file in files:
                with open(file, "rb") as fil:
                    part = MIMEApplication(
                        fil.read(),
                        Name=basename(file)
                    )
                part["Content-Disposition"] = "attachment; filename=%s" % basename(file)
                msg.attach(part)

        try:
            context = ssl.create_default_context()
            server = smtplib.SMTP_SSL('smtp.zoho.com', 465, context=context)
            server.ehlo()
            server.login(self.gmail_user, self.gmail_app_password)
            server.sendmail(self.sent_from, sent_to, msg.as_string())
            server.close()

            print('Email sent!')
        except Exception as exception:
            print("Error: %s!\n\n" % exception)