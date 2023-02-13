# Generated by Django 4.1 on 2023-02-13 13:04

import admins.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0007_alter_shortapplication_nbm'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shortapplication',
            name='nbm',
            field=models.CharField(max_length=255, validators=[admins.models.is_numeric_validator], verbose_name='Nbm'),
        ),
    ]
