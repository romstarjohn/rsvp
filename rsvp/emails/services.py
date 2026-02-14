# emails/services.py
import logging
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from .models import EmailQueue

logger = logging.getLogger("rsvp.custom")

def send_email(email_obj: EmailQueue):
    try:
        msg = EmailMultiAlternatives(
            subject=email_obj.subject,
            body=email_obj.body if not email_obj.is_html else "",
            to=[email_obj.to_email],
        )
        if email_obj.is_html:
            msg.attach_alternative(email_obj.body, "text/html")
        msg.send()
        email_obj.sent = True
        email_obj.sent_at = timezone.now()
        email_obj.error = ""
        email_obj.save()
        logger.info(f"Email sent successfully to {email_obj.to_email}")
        return True
    except Exception as e:
        email_obj.sent = False
        email_obj.error = str(e)
        email_obj.retries += 1
        email_obj.save()
        logger.error(f"Failed to send email to {email_obj.to_email}: {str(e)}")
        return False
