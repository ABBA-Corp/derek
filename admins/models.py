from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField
from easy_thumbnails.templatetags.thumbnail import get_thumbnailer
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, FileExtensionValidator
import re
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.utils.text import slugify
import random
import string
import cyrtranslit
# telephone nbm validator


# sace image function
def save_image(image):
    aliases = ['product_img', 'original', 'avatar', 'btn_img', 'prod_photo', 'ten']
    thumbs = []

    for alias in aliases:
        thumb = get_thumbnailer(image)[alias]
        thumbs.append(thumb)

    return thumbs


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, slug, extra_class=None):
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists or (extra_class and extra_class.objects.filter(slug=slug)):
        new_slug = "{slug}-{randstr}".format(slug=slug, randstr=random_string_generator(size=4))
        return unique_slug_generator(instance, new_slug, extra_class)
    
    return slug


def is_numeric_validator(value):
    if str(value).isnumeric() is False:
        raise ValidationError(
            ("Your telephone number is invalid"),
            params={'value': value}
        )

class MetaTags(models.Model):
    meta_deck = models.JSONField('Meta desk', blank=True, null=True)
    meta_keys = models.JSONField('Meta keys', blank=True, null=True)



def telephone_validator(value):
    number_temp = r"\+998\d{9}"
    if bool(re.match(number_temp, value)) == False:
        raise ValidationError(
            ("Your telephone number is invalid"),
            params={'value': value}
        )


# Create your models here.
class StaticInformation(models.Model):
    title = models.JSONField('Заголовок сайта', blank=True, null=True)
    subtitle = models.JSONField('Подзаголовок сайта', blank=True, null=True)
    deskription = models.JSONField("Описание сайта", blank=True, null=True)
    about_us = models.JSONField("О нас", blank=True, null=True)
    adres = models.JSONField("Адрес", blank=True, null=True)
    logo_first = ThumbnailerImageField("Лого сайта", blank=True, null=True, upload_to='site_logo')
    logo_second = ThumbnailerImageField("Второе лого", blank=True, null=True, upload_to='site_logo')
    email = models.EmailField("Эмейл", blank=True, null=True)
    telegram = models.URLField("Ссылка на телеграм", blank=True, null=True, max_length=255)
    instagram = models.URLField("Ссылка на инстаграм", blank=True, null=True, max_length=255)
    facebook = models.URLField("Ссылка на фэйсбук", blank=True, null=True, max_length=255)
    youtube = models.URLField("Ютуб", blank=True, null=True, max_length=255)
    nbm = models.CharField("Номер телефона", blank=True, null=True, max_length=255)
    map = models.TextField('Iframe карты', blank=True, null=True)
    work_time = models.JSONField('Время работы', blank=True, null=True)
    cotalog = models.FileField('Cotalog docx', upload_to='cotalog_docx', blank=True, null=True)


    class Meta:
        verbose_name = 'static_inf'


    def __str__(self):
        return 'Static information'

    
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)




# media images
class ImageGalery(models.Model):
    title = models.JSONField('Заголовок изображения', blank=True, null=True)

    def __str__(self):
        return 'Image' + str(self.id)
    
    class Meta:
        verbose_name = 'img_gal'


# image gallery images
class ImageGalleryFiles(models.Model):
    gallery = models.ForeignKey(ImageGalery, on_delete=models.CASCADE)
    image = ThumbnailerImageField('Изображение', upload_to='image_gallery')



# media videos
class VideoGalery(models.Model):
    title = models.JSONField('Заголовок видео', blank=True, null=True)

    def __str__(self):
        return 'Video' + str(self.id)

    class Meta:
        verbose_name = 'vid_gal'


# video gallery videos 
class VideoGalleryVideos(models.Model):
    gallery = models.ForeignKey(VideoGalery, on_delete=models.CASCADE)
    video = models.FileField('Видео', upload_to='videos_gallery', null=True, validators=[FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])])



# article categories
class ArticleCategories(models.Model):
    name = models.JSONField('Заголовок', blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')
    image = ThumbnailerImageField(upload_to='article_group_image', blank=True, null=True)

    class Meta:
        verbose_name = 'ArticleCategory'

# blog 
class Articles(models.Model):
    image = ThumbnailerImageField(upload_to='article_images', blank=True, null=True)
    title = models.JSONField('Заголовок')
    slug = models.SlugField('Slug', editable=False, unique=True)
    body = models.JSONField("Статья")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    created_date = models.DateField()
    active = models.BooleanField(default=True)
    meta = models.ForeignKey(MetaTags, on_delete=models.CASCADE, blank=True, null=True)


    def get_format_data(self):
        return str(self.created_date.year) + '-' + str(self.created_date.month) + '-' + str(self.created_date.day)

    def get_dot_date(self):
        m = str(self.created_date.month)
        if len(m) == 1:
            m = '0' + m

        d = str(self.created_date.day)
        if len(d) == 1:
            d = '0' + d

        return d + '.' + m + '.' + str(self.created_date.year)

    class Meta:
        verbose_name = 'articles'

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            lng = Languages.objects.filter(active=True).filter(default=True).first()
            str = cyrtranslit.to_latin(self.title.get(lng.code, '')[:50])
            print(str)
            slug = slugify(str)
            self.slug = unique_slug_generator(self, slug)

        return super().save(*args, **kwargs)


# languages
class Languages(models.Model):
    name = models.CharField('Названия', max_length=255, blank=True, null=True)
    code = models.CharField('Код языка', max_length=255, blank=True, null=True, unique=True)
    icon = ThumbnailerImageField(upload_to='lng_icon', blank=True, null=True)
    active = models.BooleanField(default=False)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'lang'


# translation groups
class TranlsationGroups(models.Model):
    title = models.CharField('Название', max_length=255, unique=True)
    sub_text = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'transl_group'


# translations
class Translations(models.Model):
    group = models.ForeignKey(TranlsationGroups, on_delete=models.CASCADE, related_name='translations')
    key = models.CharField(max_length=255)
    value = models.JSONField("Значение")


    def __str__(self):
        return f'{self.group.sub_text}.{self.key}'

    class Meta:
        verbose_name = 'transl'
        unique_together = ['key', 'group']



# faq
class FAQ(models.Model):
    question = models.JSONField('Вопрос')
    answer = models.JSONField('Ответ')
    active = models.BooleanField(default=True, blank=True, null=True)

    
    class Meta:
        verbose_name = 'faq'



# inputs model
class AdminInputs(models.Model):
    inputs = models.JSONField('Input', blank=True, null=True)



# about us
class AboutUs(models.Model):
    title_one = models.JSONField('Title', blank=True, null=True)
    title_second = models.JSONField('Title', blank=True, null=True)
    text_first = models.JSONField("Text", blank=True, null=True)
    text_second = models.JSONField("Text", blank=True, null=True)
    video = models.FileField('Video', upload_to='about_us', blank=True, null=True)


# about us images
class AboutUsImages(models.Model):
    parent = models.ForeignKey(AboutUs, on_delete=models.CASCADE, related_name='images', blank=True, null=True)
    image = ThumbnailerImageField(upload_to='about_us_images', blank=True, null=True)

# reviews
class Reviews(models.Model):
    image = ThumbnailerImageField(upload_to='rev_image', blank=True, null=True)
    title = models.JSONField("Title", blank=True, null=True)
    text = models.JSONField('Text', blank=True, null=True)
    active = models.BooleanField('Active', default=True)
    rating = models.PositiveBigIntegerField('Stars', validators=[MaxValueValidator(5)], default=0)


 # partners
class Partners(models.Model):
    name = models.JSONField('Name')
    deckription = models.JSONField('Deckription', blank=True, null=True)
    image = ThumbnailerImageField(upload_to='partners_images', blank=True, null=True)