import ssl
from django.core.mail.backends.smtp import EmailBackend


class NoVerifyEmailBackend(EmailBackend):
    """SMTP backend без проверки SSL-сертификата (для Mailcow через внутренний хост)."""

    def open(self):
        if self.connection:
            return False
        connection_params = {
            "local_hostname": None,
            "timeout": self.timeout,
        }
        if self.use_ssl:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            connection_params["context"] = ctx
        try:
            self.connection = self.connection_class(
                self.host, self.port, **connection_params
            )
            if self.use_tls:
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                self.connection.ehlo()
                self.connection.starttls(context=ctx)
                self.connection.ehlo()
            if self.username and self.password:
                self.connection.login(self.username, self.password)
            return True
        except Exception:
            if not self.fail_silently:
                raise
