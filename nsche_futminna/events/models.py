from django.db import models

from django.conf import settings
from accounts.models import StudentProfile

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to="events/", blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class EventRegistration(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('student', 'event')  # no double registration

class Resource(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='resources/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



class Announcement(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    publish_date = models.DateTimeField(null=True, blank=True, help_text="Optional: set a publish date")
    is_active = models.BooleanField(default=True, help_text="Uncheck to hide announcement")
    is_pinned = models.BooleanField(default=False, help_text="Pinned announcements appear first")

    class Meta:
        ordering = ["-is_pinned", "-created_at"]

    def __str__(self):
        return self.title
