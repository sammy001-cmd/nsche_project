from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=100, default="Administrator")
    phone = models.CharField(max_length=20, blank=True, null=True)
    profile_image = models.ImageField(upload_to="admin_profiles/", blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"


# class UpgradeOption(models.Model):
#     name = models.CharField(max_length=200)
#     description = models.TextField()
#     price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
#     active = models.BooleanField(default=True)

#     def __str__(self):
#         return self.name
from django.db import models
from accounts.models import StudentProfile
from events.models import Event

class EventRegistration(models.Model):
    student = models.ForeignKey(
        StudentProfile, 
        on_delete=models.CASCADE, 
        related_name="admin_event_registrations"
    )
    event = models.ForeignKey(
        Event, 
        on_delete=models.CASCADE, 
        related_name="admin_event_registrations"
    )
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.event.title}"
