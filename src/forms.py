from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Patient, City, Vendor, Chaperone, VendorUser


class ExtendedUserCreationForm(UserCreationForm):
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

    phone = forms.CharField(label="Mobile", max_length=100, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control rounded-pill',
        'placeholder': 'Mobile Number'
    }))

    class Meta:
        model = Chaperone
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2', 'phone']


class ExtendedVendorCreationForm(UserCreationForm):
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

    phone = forms.CharField(label="Mobile", max_length=100, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control rounded-pill',
        'placeholder': 'Mobile Number'
    }))

    vendor_name = forms.CharField(label="Organization Name", max_length=255, required=True,
                                  widget=forms.TextInput(attrs={
                                      'class': 'form-control rounded-pill',
                                      'placeholder': 'Last Name'
                                  }))

    class Meta:
        model = VendorUser
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2', 'phone', 'vendor_name', 'state', 'city']


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
        model = Patient
        fields = ['patient', 'mobile', 'service', 'address', 'state', 'city', 'pin', 'document']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.none()
        self.fields['service'].queryset = Vendor.objects.none()

        if 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                self.fields['city'].queryset = City.objects.filter(state_id=state_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.state.city_set.order_by('name')

        if 'city' in self.data:
            try:
                city_id = int(self.data.get('city'))
                self.fields['service'].queryset = Vendor.objects.filter(city_id=city_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['service'].queryset = self.instance.city.vendor_set.order_by('name')
