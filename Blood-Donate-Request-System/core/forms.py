from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import DonorProfile, BloodRequest

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]

class DonorForm(forms.ModelForm):
    class Meta:
        model = DonorProfile
        fields = ["blood_group", "phone", "location", "last_donation_date", "availability", "description"]
        widgets = {"last_donation_date": forms.DateInput(attrs={"type": "date"})}

class BloodRequestForm(forms.ModelForm):
    class Meta:
        model = BloodRequest
        fields = ["patient_name", "blood_group", "hospital_name", "location", "required_date",
                  "bags_required", "contact_number", "description", "status"]
        widgets = {"required_date": forms.DateInput(attrs={"type": "date"})}

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
