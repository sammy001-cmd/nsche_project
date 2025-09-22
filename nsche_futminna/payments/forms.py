# payments/forms.py
from django import forms
from .models import Payment

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'description']  # student will be assigned in view
# payments/forms.py
from django import forms

STUDENT_TYPE_CHOICES = [
    ("new", "New Student - 1500 NGN"),
    ("returning", "Returning Student - 1000 NGN"),
]

class DuesSelectionForm(forms.Form):
    student_type = forms.ChoiceField(choices=STUDENT_TYPE_CHOICES, widget=forms.RadioSelect)
