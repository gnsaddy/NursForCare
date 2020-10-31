from datetime import datetime
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    holder = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    mobile = models.IntegerField()

    def __str__(self):
        return self.holder.first_name + " " + self.holder.last_name


services = (
    ('', 'Choose...'),
    ('nr', 'Nursing'),
    ('vc', 'Vaccination'),
    ('ec', 'Elder care'),
    ('dc', 'Doctor consultation'),
    ('md', 'Medicine delivery'),
    ('ndc', 'Nutrition & Diet consultation'),
    ('am', 'Ambulance')
)

states = (
    ('', 'Choose...'),
    ('br', 'Bihar'),
    ('ka', 'Karnataka'),
    ('mh', 'Maharashtra'),
    ('up', 'UP')
)

cities = (
    ('', 'Choose...'),
    ('ar', 'Patna'),
    ('blr', 'Bangalore'),
    ('mb', 'Mumbai'),
    ('nd', 'Noida')
)


class ServiceBooking(models.Model):
    holder = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
    patient = models.CharField(max_length=100)
    mobile = models.IntegerField()
    service = models.CharField(max_length=100, choices=services)
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=100, choices=cities)
    state = models.CharField(max_length=100, choices=states)
    pin = models.IntegerField()
    bookingDate = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.patient + " treated by " + self.holder.first_name
