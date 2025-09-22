from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import StudentProfile
from .models import ContactMessage

admin.site.register(StudentProfile)





@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at")
    search_fields = ("name", "email", "message")
