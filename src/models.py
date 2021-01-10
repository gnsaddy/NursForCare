import os
from datetime import datetime
from django.utils import timezone
from uuid import uuid4
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)


class UserManager(BaseUserManager):

    def create_user(self, email, password, is_active=True, is_staff=False, is_superuser=False,
                    is_attendant=False, is_vendor=False, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.admin = is_superuser
        user.active = is_active
        user.staff = is_staff
        user.attendant = is_attendant
        user.vendor = is_vendor
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = None
    email = models.EmailField(max_length=150, unique=True, db_index=True)
    admin = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    attendant = models.BooleanField(default=False)
    vendor = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=12)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    object = UserManager()

    def __str__(self):
        return str(self.first_name + " " + self.last_name)

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_active(self):
        return self.active

    @property
    def is_superuser(self):
        return self.admin

    @property
    def is_attendant(self):
        return self.attendant

    @property
    def is_vendor(self):
        return self.vendor


class Chaperone(User):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    object = UserManager()

    def __str__(self):
        return self.email

    @property
    def days_active(self):
        diff = timezone.now() - self.created_at
        return diff.days


class VendorUser(User):
    vendor_name = models.CharField(max_length=255, null=True)
    state = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    object = UserManager()

    def __str__(self):
        return self.email

    @property
    def days_active(self):
        diff = timezone.now() - self.created_at
        return diff.days


class State(models.Model):
    name = models.CharField(max_length=50, null=True, unique=True)

    def __str__(self):
        return self.name


class City(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class AvailableServices(models.Model):
    service_name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.service_name


def content_file_name_v(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s_%s.%s" % (instance.name, uuid4().hex, ext)
    return os.path.join('medicalVendor/', filename)


class VendorService(models.Model):
    vendor_name = models.ForeignKey(VendorUser, on_delete=models.CASCADE, null=True)
    registered_by = models.CharField(max_length=155, default="None")
    name = models.CharField(max_length=255, db_index=True, null=True)
    service = models.ForeignKey(AvailableServices, on_delete=models.CASCADE, null=True)
    available = models.BooleanField(default=False, null=True)
    mobile = models.CharField(max_length=11, null=True)
    address = models.CharField(max_length=255, null=True)
    pin = models.CharField(max_length=10, null=True)
    document = models.FileField(upload_to=content_file_name_v, default=None)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        if self.available:
            self.available = "Available"
        else:
            self.available = "Not Available"

        return self.name + " provides " + str(self.service.service_name) + " Status " + str(self.available)


def content_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s_%s.%s" % (instance.patient, uuid4().hex, ext)
    return os.path.join('documents/', filename)


class Patient(models.Model):
    holder = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
    patient = models.CharField(max_length=100)
    mobile = models.IntegerField()
    address = models.CharField(max_length=500)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    service = models.ForeignKey(VendorService, on_delete=models.SET_NULL, null=True)
    pin = models.IntegerField()
    document = models.FileField(upload_to=content_file_name, default=None)
    bookingDate = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return str(self.holder) + ' booked service for ' + (str(self.patient))

    @property
    def days_active(self):
        diff = timezone.now() - self.bookingDate
        return diff.days


class PatientReport(models.Model):
    pid = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    pname = models.CharField(max_length=100, null=True)
    pcontact = models.CharField(max_length=12, null=True)
    paddress = models.CharField(max_length=255, null=True)
    pstate = models.CharField(max_length=50, null=True)
    pcity = models.CharField(max_length=50, null=True)
    ppin = models.CharField(max_length=50, null=True)
    description = models.TextField(null=True)
    admitted_since = models.CharField(max_length=155, null=True)
    created_on = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.pname + " : " + str(self.pid.holder.first_name)
