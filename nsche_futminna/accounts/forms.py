from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import StudentProfile

from .models import ContactMessage
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import re

def validate_nigerian_phone(value):
    pattern = r'^(?:\+234|0)[789][01]\d{8}$'  # Matches +2348012345678 or 08012345678
    if not re.match(pattern, value):
        raise forms.ValidationError("Enter a valid Nigerian phone number (e.g., +2348012345678 or 08012345678).")

# def validate_matric_number(value):
#     import re
#     pattern = r'^\d{6}(?:/)?EH$' 
#     if not re.match(pattern, value.upper()):
#         raise forms.ValidationError("Enter your full correct matric number.")

# Validator for matric number
def validate_matric_number(value):
    if not value.lower().endswith("eh"):
        raise forms.ValidationError("Enter your full correct matric number.")

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']


from django.core.exceptions import ValidationError

def validate_image_format(image):
    valid_extensions = ['.jpg', '.jpeg', '.png']
    import os
    ext = os.path.splitext(image.name)[1].lower()
    if ext not in valid_extensions:
        raise ValidationError("Only .jpg, .jpeg, and .png files are allowed.")


class StudentProfileForm(forms.ModelForm):
    matric_number = forms.CharField(validators=[validate_matric_number])
    phone = forms.CharField(validators=[validate_nigerian_phone])
    profile_picture = forms.ImageField(validators=[validate_image_format], required=False)

    class Meta:
        model = StudentProfile
        fields = ['matric_number', 'level', 'phone', 'profile_picture']


class StudentProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['phone', 'level', 'matric_number', 'profile_picture']



class StudentLoginForm(forms.Form):
    username = forms.CharField(label="Matric Number", max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        # Convert input to uppercase to match registration
        return self.cleaned_data['username'].upper()





class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "message"]
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)





# forms.py
from django import forms
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site

class CustomPasswordResetForm(PasswordResetForm):
    """
    Sends plain-text password reset emails only.
    Ignores HTML templates and avoids template rendering issues.
    """

    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):
        # Grab user and request from context
        user = context.get("user")
        request = context.get("request")
        uid = context.get("uid")
        token = context.get("token")

        # Build password reset URL
        domain = get_current_site(request).domain if request else "127.0.0.1:8000"
        protocol = "https" if request and request.is_secure() else "http"
        reset_url = f"{protocol}://{domain}{reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})}"

        # Compose plain-text message
        text_body = (
            f"Hi {user.get_full_name() or user.username},\n\n"
            f"You requested a password reset. Use the link below to reset your password:\n\n"
            f"{reset_url}\n\n"
            "If you did not request this, ignore this email.\n\n"
            "Thanks,\nNSChE FUTMINNA Team"
        )

        # Subject
        subject = "NSChE FUTMINNA Password Reset"

        # From email fallback
        from_email = from_email or settings.DEFAULT_FROM_EMAIL

        # Send plain-text email
        msg = EmailMultiAlternatives(subject, text_body, from_email, [to_email])
        msg.send(fail_silently=False)



    





