# Generated by Django 3.1.2 on 2020-12-20 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0002_auto_20201220_1343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='vendor',
            field=models.BooleanField(default=False),
        ),
    ]