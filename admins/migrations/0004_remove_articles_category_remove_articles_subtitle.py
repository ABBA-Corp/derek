# Generated by Django 4.1 on 2023-02-24 11:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0003_delete_shortapplication'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articles',
            name='category',
        ),
        migrations.RemoveField(
            model_name='articles',
            name='subtitle',
        ),
    ]