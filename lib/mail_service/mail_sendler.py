from . import MailConnector

from config import EMAIL_ADDRESS, EMAIL_PASSWORD


class MailSendler:
    def __init__(self):
        self.connector = MailConnector()
        self.server = self.connector.server

    def __enter__(self):
        self.server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.server.quit()

    def send_mail(self, mail: str, letter: str):
        self.server.sendmail(EMAIL_ADDRESS, mail, letter)
