from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Participation

@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "phone_number", "participation", "relation", "message")
    list_filter = ("first_name","email")
    search_fields = ("email", "last_name", "participation","relation")
