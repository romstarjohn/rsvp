# emails/management/commands/send_pending_emails.py
from django.core.management.base import BaseCommand
from emails.models import EmailQueue
from emails.services import send_email

class Command(BaseCommand):
    help = "Send pending emails from EmailQueue"

    def handle(self, *args, **kwargs):
        pending_emails = EmailQueue.objects.filter(sent=False).order_by("created_at")
        if not pending_emails.exists():
            self.stdout.write("No pending emails found.")
            return

        for email in pending_emails:
            send_email(email)
