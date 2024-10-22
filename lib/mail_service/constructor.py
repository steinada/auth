from config import EMAIL_ADDRESS, API_HOST, API_PORT, APP_NAME


class MailConstructor:

    @staticmethod
    async def reset_password_link_mail(mail: str, token: str):
        letter = f"""\
        From: {EMAIL_ADDRESS}
        To: {mail}
        Subject: Сброс пароля на платформе {APP_NAME}!
        Content-Type: text/plain; charset="UTF-8";

        Здравствуйте!\n
        Для сброса пароля перейдите по ссылке http://{API_HOST}:{API_PORT}/auth/reset-password-token/{token}"""

        letter = letter.encode("UTF-8")
        return letter

    @staticmethod
    async def verify_mail_code(code: str, mail: str):
        letter = f"""\
                From: {EMAIL_ADDRESS}
                To: {mail}
                Subject: Подтвердите почту на сервисе {APP_NAME}!
                Content-Type: text/plain; charset="UTF-8";

                Здравствуйте!\n
                Введите код {code} для активации почты на сервисе {APP_NAME}"""

        letter = letter.encode("UTF-8")
        return letter
