# Generated by Django 4.1 on 2023-02-14 12:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_category_cotalog'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='atributoptions',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='category',
            name='slug',
        ),
    ]