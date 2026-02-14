from django.db import models

# Create your models here.


class Participation(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    participation = models.CharField(max_length=50)
    relation = models.CharField(max_length=50, blank=True, null=True)
    message = models.TextField(blank=True, null=True)