# Generated by Django 3.1.2 on 2021-01-10 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0011_auto_20210110_2154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientreport',
            name='admitted_since',
            field=models.CharField(max_length=155, null=True),
        ),
    ]