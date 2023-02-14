# Generated by Django 4.1 on 2023-02-13 13:01

import admins.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0006_articles_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shortapplication',
            name='nbm',
            field=models.CharField(default='99999', max_length=10, validators=[admins.models.is_numeric_validator], verbose_name='Nbm'),
            preserve_default=False,
        ),
    ]