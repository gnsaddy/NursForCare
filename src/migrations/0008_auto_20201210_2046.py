# Generated by Django 3.1.2 on 2020-12-10 15:16

from django.db import migrations, models
import src.models


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0007_auto_20201210_2031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='document',
            field=models.FileField(default=None, upload_to=src.models.content_file_name),
        ),
    ]