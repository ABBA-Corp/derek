# Generated by Django 4.1 on 2023-02-11 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='atributoptions',
            name='slug',
            field=models.SlugField(default='some-33', editable=False, unique=True, verbose_name='Slug'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productvariants',
            name='top',
            field=models.BooleanField(default=False, verbose_name='Top'),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(editable=False, unique=True, verbose_name='Slug'),
        ),
        migrations.AlterField(
            model_name='products',
            name='slug',
            field=models.SlugField(editable=False, unique=True, verbose_name='Slug'),
        ),
    ]
