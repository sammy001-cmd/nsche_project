from django import forms
from .models import AdminProfile
from events.models import Event  

class AdminProfileForm(forms.ModelForm):
    class Meta:
        model = AdminProfile
        fields = ["role", "phone", "profile_image"]


# class UpgradeOptionForm(forms.ModelForm):
#     class Meta:
#         model = UpgradeOption
#         fields = ["name", "description", "price", "active"]
# from django import forms
# from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["title", "description", "date", "time", "location", "image"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "date": forms.DateTimeInput(attrs={"type": "datetime-local", "class": "form-control"}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }


from django import forms
from events.models import Announcement

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ["title", "message", "publish_date", "is_active", "is_pinned"]
        widgets = {
            "publish_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "message": forms.Textarea(attrs={"rows":4}),
        }




