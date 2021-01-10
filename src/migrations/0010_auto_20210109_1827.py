# Generated by Django 3.1.2 on 2021-01-09 12:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0009_auto_20210109_1818'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientreport',
            name='admitted_since',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='patientreport',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]