#!/usr/bin/python
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
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
        try:
            server = smtplib.SMTP(self.SMTPServer, int(self.SMTPPort))
            server.starttls()
            server.login(self.SMTPUsername, self.SMTPPassword)
            msg = MIMEMultipart()
            msg["From"] = self.SMTPUsername
            msg["To"] = self.recipient
            today = time.strftime("%A %d %B %Y")
            msg["Subject"] = f"News {today}"
            msg.attach(MIMEText(self.message, 'html'))
            server.send_message(msg)
            server.quit()
        except Exception as e:
            logging.warning(f"Error in sending email: {e}")
            return False
