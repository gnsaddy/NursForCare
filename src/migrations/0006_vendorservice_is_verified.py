# Generated by Django 3.1.2 on 2020-12-25 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0005_auto_20201225_1505'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendorservice',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]