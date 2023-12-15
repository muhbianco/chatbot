import smtplib
import os
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
        self.msg = MIMEMultipart()

    def send_email(self, sent_to, sent_subject, sent_body, files = None):
        self.msg["From"] = self.sent_from
        self.msg["To"] = COMMASPACE.join(sent_to)
        self.msg["Data"] = formatdate(localtime=True)
        self.msg["Subject"] = sent_subject

        self.msg.attach(MIMEText(sent_body))

        for file in files:
            with open(file, "rb") as fil:
                part = MIMEApplication(
                    fil.read(),
                    Name=basename(file)
                )
            part["Content-Disposition"] = "attachment; filename=%s" % basename(file)
            self.msg.attach(part)

        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(self.gmail_user, self.gmail_app_password)
            server.sendmail(self.sent_from, sent_to, self.msg.as_string())
            server.close()

            print('Email sent!')
        except Exception as exception:
            print("Error: %s!\n\n" % exception)