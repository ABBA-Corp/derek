# Generated by Django 4.1 on 2023-02-16 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shortapplication',
            name='nbm',
            field=models.CharField(max_length=255, verbose_name='Nbm'),
        ),
    ]
