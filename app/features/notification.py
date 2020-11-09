#!/usr/bin/python
import smtplib, ssl
import logging

logging.basicConfig(level=logging.INFO, filename='debug.log', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%y-%m-%dT%H:%M:%S%z')

class MailNotification:
    def __init__(
        self,
        SMTPServer,
        SMTPPort,
        SMTPUsername,
        SMTPPassword,
        recipient,
        message
    ):
        self.SMTPServer = SMTPServer
        self.SMTPPort = SMTPPort
        self.SMTPUsername = SMTPUsername
        self.SMTPPassword = SMTPPassword
        self.recipient = recipient
        self.message = message

    def send(self):
        ssl_context = ssl.create_default_context()
        try:
            server = smtplib.SMTP(self.SMTPServer, self.SMTPPort)
            server.starttls(context=ssl_context)
            server.login(self.SMTPUsername, self.SMTPPassword)
            server.sendmail(self.SMTPUsername, self.recipient, self.message)
        except Exception as e:
            logging.debug(f"Unable to send email: {e}")
            return False
