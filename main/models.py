from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, FileExtensionValidator
from easy_thumbnails.fields import ThumbnailerImageField
from colorfield.fields import ColorField
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from autoslug import AutoSlugField
from admins.models import Languages
from django.utils.text import slugify
import string
import random
from admins.models import unique_slug_generator
# Create your models here.


# colors
class Colors(models.Model):
    name = models.JSONField('Name', blank=True, null=True)
    slug = models.SlugField('Slug', editable=False, unique=True)
    hex = ColorField(default='#FF0000')
    

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            lng = Languages.objects.filter(active=True).filter(default=True).first()
            str = self.name.get(lng.code)
            slug = slugify(str)
            self.slug = unique_slug_generator(self, slug)

        return super().save(*args, **kwargs)



# atributs
class Atributs(models.Model):
    name = models.JSONField("name", blank=True, null=True)


# atribut option
class AtributOptions(models.Model):
    name = models.JSONField("Name", blank=True, null=True)
    slug = models.SlugField('Slug', editable=False, unique=True)
    atribut = models.ForeignKey(Atributs, on_delete=models.CASCADE, related_name='options')


    def save(self, *args, **kwargs):  # new
        if not self.slug:
            lng = Languages.objects.filter(active=True).filter(default=True).first()
            str = self.name.get(lng.code)
            slug = slugify(str)
            self.slug = unique_slug_generator(self, slug)

        return super().save(*args, **kwargs)

    


# category
class Category(models.Model):
    name = models.JSONField('Name', blank=True, null=True)
    slug = models.SlugField('Slug', editable=False, unique=True)
    deckription = models.JSONField("Deckription", blank=True, null=True)
    icon = ThumbnailerImageField(upload_to='ctg_icons', blank=True, null=True)
    image = ThumbnailerImageField(upload_to='ctg_image', blank=True, null=True)
    atributs = models.ManyToManyField(Atributs, blank=True, null=True)

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            lng = Languages.objects.filter(active=True).filter(default=True).first()
            str = self.name.get(lng.code)
            slug = slugify(str)
            self.slug = unique_slug_generator(self, slug)

        return super().save(*args, **kwargs)


# products
class Products(models.Model):
    name = models.JSONField('Name', blank=True, null=True)
    slug = models.SlugField('Slug', editable=False, unique=True)
    type = models.JSONField("Type", blank=True, null=True)
    manufacturer = models.JSONField("Manuf", blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description = models.JSONField('Descr', blank=True, null=True)
    active = models.BooleanField('Active', default=True)

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            lng = Languages.objects.filter(active=True).filter(default=True).first()
            str = self.name.get(lng.code)
            slug = slugify(str)
            self.slug = unique_slug_generator(self, slug)

        return super().save(*args, **kwargs)



# product variant
class ProductVariants(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='variants')
    price = models.FloatField('Price', validators=[MinValueValidator(0)])
    color = models.ForeignKey(Colors, on_delete=models.CASCADE)
    slug = models.SlugField('Slug', editable=False, unique=True)
    options = models.ManyToManyField(AtributOptions, blank=True, null=True)
    image = ThumbnailerImageField(upload_to='variant_images', blank=True, null=True)
    code = models.CharField('Code', max_length=6, unique=True)
    top = models.BooleanField('Top', default=False)
    default = models.BooleanField("Default", default=False)

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            lng = Languages.objects.filter(active=True).filter(default=True).first()
            str = self.product.name.get(lng.code, 'prod') + self.color.name.get(lng.code, 'color')
            slug = slugify(str)
            self.slug = unique_slug_generator(self, slug, Products)

        return super().save(*args, **kwargs)









