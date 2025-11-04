from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    matric_number = models.CharField(max_length=30, unique=True)
    department = models.CharField(max_length=100, blank=True)
    level = models.CharField(max_length=10, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.png')
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.matric_number})"
    

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"


from django.conf import settings
from django.db import models

class StudentProfile(models.Model):
    LEVEL_CHOICES = [
        ("100L", "100 Level"),
        ("200L", "200 Level"),
        ("300L", "300 Level"),
        ("400L", "400 Level"),
        ("500L", "500 Level"),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    matric_number = models.CharField(max_length=30, unique=True)
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.png')

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.matric_number})"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"




