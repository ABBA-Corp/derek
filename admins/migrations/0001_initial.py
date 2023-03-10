# Generated by Django 4.1 on 2023-02-15 17:52

import admins.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import easy_thumbnails.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AboutUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_one', models.JSONField(blank=True, null=True, verbose_name='Title')),
                ('title_second', models.JSONField(blank=True, null=True, verbose_name='Title')),
                ('text_first', models.JSONField(blank=True, null=True, verbose_name='Text')),
                ('text_second', models.JSONField(blank=True, null=True, verbose_name='Text')),
                ('video', models.FileField(blank=True, null=True, upload_to='about_us', verbose_name='Video')),
            ],
        ),
        migrations.CreateModel(
            name='AdminInputs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inputs', models.JSONField(blank=True, null=True, verbose_name='Input')),
            ],
        ),
        migrations.CreateModel(
            name='ArticleCategories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.JSONField(blank=True, null=True, verbose_name='Заголовок')),
                ('image', easy_thumbnails.fields.ThumbnailerImageField(blank=True, null=True, upload_to='article_group_image')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='admins.articlecategories')),
            ],
            options={
                'verbose_name': 'ArticleCategory',
            },
        ),
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.JSONField(verbose_name='Вопрос')),
                ('answer', models.JSONField(verbose_name='Ответ')),
                ('active', models.BooleanField(blank=True, default=True, null=True)),
            ],
            options={
                'verbose_name': 'faq',
            },
        ),
        migrations.CreateModel(
            name='ImageGalery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.JSONField(blank=True, null=True, verbose_name='Заголовок изображения')),
            ],
            options={
                'verbose_name': 'img_gal',
            },
        ),
        migrations.CreateModel(
            name='Languages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Названия')),
                ('code', models.CharField(blank=True, max_length=255, null=True, unique=True, verbose_name='Код языка')),
                ('icon', easy_thumbnails.fields.ThumbnailerImageField(blank=True, null=True, upload_to='lng_icon')),
                ('active', models.BooleanField(default=False)),
                ('default', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'lang',
            },
        ),
        migrations.CreateModel(
            name='MetaTags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meta_deck', models.JSONField(blank=True, null=True, verbose_name='Meta desk')),
                ('meta_keys', models.JSONField(blank=True, null=True, verbose_name='Meta keys')),
            ],
        ),
        migrations.CreateModel(
            name='Partners',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.JSONField(verbose_name='Name')),
                ('deckription', models.JSONField(blank=True, null=True, verbose_name='Deckription')),
                ('image', easy_thumbnails.fields.ThumbnailerImageField(blank=True, null=True, upload_to='partners_images')),
            ],
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', easy_thumbnails.fields.ThumbnailerImageField(blank=True, null=True, upload_to='rev_image')),
                ('title', models.JSONField(blank=True, null=True, verbose_name='Title')),
                ('text', models.JSONField(blank=True, null=True, verbose_name='Text')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('rating', models.PositiveBigIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(5)], verbose_name='Stars')),
            ],
        ),
        migrations.CreateModel(
            name='ShortApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255, verbose_name='First name')),
                ('last_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Last name')),
                ('nbm', models.CharField(max_length=255, validators=[admins.models.is_numeric_validator], verbose_name='Nbm')),
                ('status', models.CharField(choices=[('На рассмотрении', 'На рассмотрении'), ('Рассмотрено', 'Рассмотрено'), ('Отклонено', 'Отклонено')], default='На рассмотрении', max_length=255, verbose_name='Status')),
            ],
        ),
        migrations.CreateModel(
            name='StaticInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.JSONField(blank=True, null=True, verbose_name='Заголовок сайта')),
                ('subtitle', models.JSONField(blank=True, null=True, verbose_name='Подзаголовок сайта')),
                ('deskription', models.JSONField(blank=True, null=True, verbose_name='Описание сайта')),
                ('about_us', models.JSONField(blank=True, null=True, verbose_name='О нас')),
                ('adres', models.JSONField(blank=True, null=True, verbose_name='Адрес')),
                ('logo_first', easy_thumbnails.fields.ThumbnailerImageField(blank=True, null=True, upload_to='site_logo', verbose_name='Лого сайта')),
                ('logo_second', easy_thumbnails.fields.ThumbnailerImageField(blank=True, null=True, upload_to='site_logo', verbose_name='Второе лого')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Эмейл')),
                ('telegram', models.URLField(blank=True, max_length=255, null=True, verbose_name='Ссылка на телеграм')),
                ('instagram', models.URLField(blank=True, max_length=255, null=True, verbose_name='Ссылка на инстаграм')),
                ('facebook', models.URLField(blank=True, max_length=255, null=True, verbose_name='Ссылка на фэйсбук')),
                ('youtube', models.URLField(blank=True, max_length=255, null=True, verbose_name='Ютуб')),
                ('nbm', models.CharField(blank=True, max_length=255, null=True, verbose_name='Номер телефона')),
                ('map', models.TextField(blank=True, null=True, verbose_name='Iframe карты')),
                ('work_time', models.JSONField(blank=True, null=True, verbose_name='Время работы')),
                ('cotalog', models.FileField(blank=True, null=True, upload_to='cotalog_docx', verbose_name='Cotalog docx')),
            ],
            options={
                'verbose_name': 'static_inf',
            },
        ),
        migrations.CreateModel(
            name='TranlsationGroups',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True, verbose_name='Название')),
                ('sub_text', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name': 'transl_group',
            },
        ),
        migrations.CreateModel(
            name='VideoGalery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.JSONField(blank=True, null=True, verbose_name='Заголовок видео')),
            ],
            options={
                'verbose_name': 'vid_gal',
            },
        ),
        migrations.CreateModel(
            name='VideoGalleryVideos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.FileField(null=True, upload_to='videos_gallery', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])], verbose_name='Видео')),
                ('gallery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admins.videogalery')),
            ],
        ),
        migrations.CreateModel(
            name='ImageGalleryFiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', easy_thumbnails.fields.ThumbnailerImageField(upload_to='image_gallery', verbose_name='Изображение')),
                ('gallery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admins.imagegalery')),
            ],
        ),
        migrations.CreateModel(
            name='Articles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', easy_thumbnails.fields.ThumbnailerImageField(blank=True, null=True, upload_to='article_images')),
                ('title', models.JSONField(verbose_name='Заголовок')),
                ('slug', models.SlugField(editable=False, unique=True, verbose_name='Slug')),
                ('subtitle', models.JSONField(verbose_name='Пост заголовок')),
                ('body', models.JSONField(verbose_name='Статья')),
                ('created_date', models.DateField()),
                ('active', models.BooleanField(default=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articles', to=settings.AUTH_USER_MODEL)),
                ('category', models.ManyToManyField(blank=True, null=True, related_name='articles', to='admins.articlecategories')),
                ('meta', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='admins.metatags')),
            ],
            options={
                'verbose_name': 'articles',
            },
        ),
        migrations.CreateModel(
            name='AboutUsImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', easy_thumbnails.fields.ThumbnailerImageField(blank=True, null=True, upload_to='about_us_images')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='admins.aboutus')),
            ],
        ),
        migrations.CreateModel(
            name='Translations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=255)),
                ('value', models.JSONField(verbose_name='Значение')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='admins.tranlsationgroups')),
            ],
            options={
                'verbose_name': 'transl',
                'unique_together': {('key', 'group')},
            },
        ),
    ]
