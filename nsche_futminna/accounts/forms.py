from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import StudentProfile

from .models import ContactMessage

# Validator for matric number
def validate_matric_number(value):
    if not value.lower().endswith("eh"):
        raise forms.ValidationError("Matric number must end with 'EH' or 'eh'.")

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']


class StudentProfileForm(forms.ModelForm):
    matric_number = forms.CharField(validators=[validate_matric_number])

    class Meta:
        model = StudentProfile
        fields = ['matric_number', 'department', 'level', 'phone', 'profile_picture']


class StudentProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['phone', 'department', 'level', 'matric_number', 'profile_picture']



# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
# from .models import StudentProfile

# class UserRegisterForm(UserCreationForm):
#     email = forms.EmailField(required=True)

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']


# class StudentProfileForm(forms.ModelForm):
#     class Meta:
#         model = StudentProfile
#         fields = ['matric_number', 'department', 'level', 'phone', 'profile_picture']


# class StudentProfileUpdateForm(forms.ModelForm):
#     class Meta:
#         model = StudentProfile
#         fields = ['phone', 'department', 'level', 'matric_number', 'profile_picture']



class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "message"]
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)