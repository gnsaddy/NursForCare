from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, ServiceBooking


class ExtendedUserCreationForm(UserCreationForm):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        "class": "form-control rounded-pill",
        "placeholder": "Enter username"
    }))

    email = forms.EmailField(required=True, label="Email", max_length=100, widget=forms.EmailInput(attrs={
        'class': 'form-control rounded-pill',
        'placeholder': 'Email Id'
    }))

    first_name = forms.CharField(label="First Name", max_length=100, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control rounded-pill',
        'placeholder': 'First Name'
    }))

    last_name = forms.CharField(label="Last Name", max_length=100, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control rounded-pill',
        'placeholder': 'Last Name'
    }))

    password1 = forms.CharField(max_length=50, label='Password', widget=forms.PasswordInput(attrs={
        "class": "form-control rounded-pill",
        "placeholder": "Enter password"
    }))
    password2 = forms.CharField(max_length=50, label='Confirm password', widget=forms.PasswordInput(attrs={
        "class": "form-control rounded-pill",
        "placeholder": "Confirm password"
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']


class UserProfileForm(forms.ModelForm):
    mobile = forms.CharField(label="Mobile", max_length=100, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control rounded-pill',
        'placeholder': 'Mobile Number'
    }))

    class Meta:
        model = UserProfile
        fields = ('mobile',)


class ServiceBookingForm(forms.ModelForm):
    patient = forms.CharField(label="Patient Name", max_length=100, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control ',
        'placeholder': 'Patient Name'
    }))

    mobile = forms.CharField(label="Mobile", max_length=12, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control ',
        'placeholder': 'Mobile Number'
    }))

    address = forms.CharField(label="Address", max_length=500, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control ',
        'placeholder': 'Address'
    }))

    pin = forms.CharField(label="Pincode", max_length=10, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Pin-code (Zip)'
    }))

    class Meta:
        model = ServiceBooking
        fields = ['patient', 'mobile', 'service', 'address', 'state', 'city', 'pin']
