import ssl
from django.core.mail.backends.smtp import EmailBackend

class UnsafeEmailBackend(EmailBackend):
    """
    SMTP backend that ignores certificate verification.
    Use only for testing / when cert mismatch exists.
    """
    def _get_connection(self):
        connection = super()._get_connection()
        if self.use_ssl:
            # Create an SSL context that ignores verification
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            connection.context = context
        return connection
