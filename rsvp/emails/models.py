from django.db import models

# Create your models here.
# emails/models.py
from django.db import models

class EmailQueue(models.Model):
    to_email = models.EmailField()
    subject = models.CharField(max_length=255)
    body = models.TextField()
    is_html = models.BooleanField(default=True)
    sent = models.BooleanField(default=False)
    error = models.TextField(blank=True, null=True)
    retries = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.to_email} | {'Sent' if self.sent else 'Pending'}"
