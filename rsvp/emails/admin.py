# Register your models here.
# emails/admin.py
from django.contrib import admin
from .models import EmailQueue

@admin.register(EmailQueue)
class EmailQueueAdmin(admin.ModelAdmin):
    list_display = ("to_email", "subject", "sent", "retries", "sent_at", "created_at")
    list_filter = ("sent",)
    search_fields = ("to_email", "subject", "error")
