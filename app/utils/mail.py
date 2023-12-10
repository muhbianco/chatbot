import smtplib
import os


class SendEmail:
    def __init__(self):
        self.gmail_user = os.environ["EMAIL_USER"]
        self.gmail_app_password = os.environ["EMAIL_PASS"]
        self.sent_from = self.gmail_user

    def send_email(self, sent_to, sent_subject, sent_body):
        email_text = """\
        From: %s
        To: %s
        Subject: %s

        %s
        """ % (self.sent_from, ", ".join(sent_to), sent_subject, sent_body)

        print("CORPO EMAIL::::", email_text)

        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(self.gmail_user, self.gmail_app_password)
            server.sendmail(self.sent_from, sent_to, email_text.encode('ascii').decode('utf-8'))
            server.close()

            print('Email sent!')
        except Exception as exception:
            print("Error: %s!\n\n" % exception)