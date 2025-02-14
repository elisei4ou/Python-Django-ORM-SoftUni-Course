from django.db import models


class UserProfile(models.Model):
    username = models.CharField(max_length=65, unique=True)
    first_name = models.CharField(max_length=40, null=True, blank=True)
    last_name = models.CharField(max_length=40, null=True, blank=True)
    email = models.EmailField(unique=True, default="students@softuni.bg")
    bio = models.TextField(max_length=120)
    profile_image_url = models.URLField()
    created_at = models.DateTimeField(auto_now=True)