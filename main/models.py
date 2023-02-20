from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, FileExtensionValidator
from easy_thumbnails.fields import ThumbnailerImageField
from colorfield.fields import ColorField
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from autoslug import AutoSlugField
from admins.models import Languages
from django.utils.text import slugify
import string
import random
from admins.models import unique_slug_generator
import cyrtranslit
from admins.models import MetaTags
# Create your models here.


# colors
class Colors(models.Model):
    name = models.JSONField('Name', blank=True, null=True)
    slug = models.SlugField('Slug', editable=False, unique=True, blank=True, null=True)
    hex = ColorField(default='#FF0000')
    

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            lng = Languages.objects.filter(active=True).filter(default=True).first()
            str = cyrtranslit.to_latin(self.name.get(lng.code, '')[:50])
            slug = slugify(str)
            self.slug = unique_slug_generator(self, slug)

        return super().save(*args, **kwargs)



# atributs
class Atributs(models.Model):
    name = models.JSONField("name", blank=True, null=True)


# atribut option
class AtributOptions(models.Model):
    name = models.JSONField("Name", blank=True, null=True)
    atribut = models.ForeignKey(Atributs, on_delete=models.CASCADE, related_name='options')



# category
class Category(models.Model):
    name = models.JSONField('Name', blank=True, null=True)
    deckription = models.JSONField("Deckription", blank=True, null=True)
    icon = ThumbnailerImageField(upload_to='ctg_icons', blank=True, null=True)
    image = ThumbnailerImageField(upload_to='ctg_image', blank=True, null=True)
    atributs = models.ManyToManyField(Atributs, blank=True, null=True)
    cotalog = models.FileField('Cotalog for download', upload_to='cotalog_fiels', blank=True, null=True)



# products
class Products(models.Model):
    name = models.JSONField('Name', blank=True, null=True)
    slug = models.SlugField('Slug', editable=False, unique=True, blank=True, null=True)
    type = models.JSONField("Type", blank=True, null=True)
    manufacturer = models.JSONField("Manuf", blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description = models.JSONField('Descr', blank=True, null=True)
    active = models.BooleanField('Active', default=True)
    meta = models.ForeignKey(MetaTags, on_delete=models.CASCADE, blank=True, null=True)

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            lng = Languages.objects.filter(active=True).filter(default=True).first()
            str = cyrtranslit.to_latin(self.name.get(lng.code, '')[:50])
            slug = slugify(str)
            self.slug = unique_slug_generator(self, slug)

        return super().save(*args, **kwargs)


@receiver(pre_save, sender=Products)
def delete_variants(sender, instance, **kwargs):
    try:
        obj = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        # Object is new, so field hasn't technically changed, but you may want to do something else here.
        pass
    else:
        if obj.category != instance.category:  # Field has changed
            ProductVariants.objects.filter(product=obj).delete()
    



# product variant
class ProductVariants(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='variants')
    price = models.FloatField('Price', validators=[MinValueValidator(0)])
    color = models.ForeignKey(Colors, on_delete=models.CASCADE)
    slug = models.SlugField('Slug', editable=False, unique=True)
    options = models.ManyToManyField(AtributOptions, blank=True, null=True)
    image = ThumbnailerImageField(upload_to='variant_images', blank=True, null=True)
    code = models.CharField('Code', max_length=255)
    top = models.BooleanField('Top', default=False)
    default = models.BooleanField("Default", default=False)

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            lng = Languages.objects.filter(active=True).filter(default=True).first()
            str = cyrtranslit.to_latin(self.product.name.get(lng.code, 'prod') + self.color.name.get(lng.code, 'color'))
            slug = slugify(str[:50])
            self.slug = unique_slug_generator(self, slug, Products)

        variants = ProductVariants.objects.filter(product=self.product).exclude(pk=self.pk)
        if variants.count() > 1 and self.default:
            for variant in variants:
                variant.default = False
                variant.save()

        return super().save(*args, **kwargs)


# short applications
class ShortApplication(models.Model):
    STATUS = [('На рассмотрении', "На рассмотрении"),
              ("Рассмотрено", "Рассмотрено"), ("Отклонено", "Отклонено")]

    first_name = models.CharField('First name', max_length=255)
    last_name = models.CharField('Last name', max_length=255, blank=True, null=True)
    nbm = models.CharField('Nbm', max_length=255)
    product = models.ForeignKey(ProductVariants, blank=True, null=True, on_delete=models.SET_NULL)
    status = models.CharField(
        'Status', default='На рассмотрении', max_length=255, choices=STATUS)

    def get_full_name(self):
        try:
            return self.first_name + ' ' + self.last_name
        except:
            return self.first_name





