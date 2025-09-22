from django.db import models

# Create your models here.
from django.db import models
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

