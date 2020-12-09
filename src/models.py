import os
from datetime import datetime
from uuid import uuid4

from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)


class UserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
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
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=12)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    object = UserManager()

    def __str__(self):
        return self.email


class VendorUser(AbstractBaseUser):
    username = None
    email = models.EmailField(max_length=150, unique=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=12)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    object = UserManager()

    def __str__(self):
        return self.email


class State(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class City(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class AvailableServices(models.Model):
    service_name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.service_name


def content_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s_%s.%s" % (instance.name, uuid4().hex, ext)
    return os.path.join('medicalVendor/', filename)


class Vendor(models.Model):
    name = models.CharField(max_length=255, db_index=True, null=True)
    service = models.ForeignKey(AvailableServices, on_delete=models.CASCADE, null=True)
    available = models.BooleanField(default=False)
    document = models.FileField(upload_to=content_file_name, default=None)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)

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
    service = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
    pin = models.IntegerField()
    document = models.FileField(upload_to=content_file_name, default=None)
    bookingDate = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return str(self.holder.first_name) + ' booked service for ' + (str(self.patient))
