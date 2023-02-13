from .models import Products, Atributs, AtributOptions, Category, Colors, ProductVariants
from admins.models import Languages
from rest_framework import serializers
from easy_thumbnails.templatetags.thumbnail import thumbnail_url
from admins.models import Articles, StaticInformation, AboutUs, Languages, Translations, MetaTags, Reviews, Partners, ShortApplication
from .utils import translator


class ThumbnailSerializer(serializers.ImageField):
    def __init__(self, alias, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.alias = alias

    def to_representation(self, instance):
        url = thumbnail_url(instance, self.alias)

        if url == '':
            return None

        request = self.context.get('request', None)
        if request is not None:
            return request.build_absolute_uri(url)

        return url


# field lang serializer
class JsonFieldSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        language = self.context['request'].headers.get('Language')

        if not language:
            language = Languages.objects.filter(default=True).first().code
        
        data = instance.get(language)

        return data


# meta serializer
class MetaFieldSerializer(serializers.ModelSerializer):
    meta_keys = JsonFieldSerializer()
    meta_deck = JsonFieldSerializer()

    class Meta:
        model = MetaTags
        exclude = ['id']



# atribut options serializer
class AtributOptionsSerializer(serializers.ModelSerializer):
    name = JsonFieldSerializer()

    class Meta:
        model = AtributOptions
        exclude = ['atribut']


# atribut serializer
class AtributSerializer(serializers.ModelSerializer):
    name = JsonFieldSerializer()
    options = AtributOptionsSerializer(many=True)

    class Meta:
        model = Atributs
        fields = '__all__'



# color serializer
class ColorSerializer(serializers.ModelSerializer):
    name = JsonFieldSerializer()

    class Meta:
        model = Colors
        fields = '__all__'



# category serializer
class Categoryserializer(serializers.ModelSerializer):
    name = JsonFieldSerializer()
    deckription = JsonFieldSerializer()
    icon = ThumbnailSerializer(alias='cart')
    image = ThumbnailSerializer(alias='cart')

    class Meta:
        model = Category
        exclude = ['atributs']


# category simple serializer
class CategorySimpleSerializer(serializers.ModelSerializer):
    name = JsonFieldSerializer()

    class Meta:
        model = Category
        fields = ['name', 'slug']



# product serializer
class ProductsSerializer(serializers.ModelSerializer):
    name = JsonFieldSerializer()
    type = JsonFieldSerializer()
    manufacturer = JsonFieldSerializer()
    category = CategorySimpleSerializer()
    description = JsonFieldSerializer()

    class Meta:
        model = Products
        fields = '__all__'



# product variant serializer
class ProductVariantSimpleSerializer(serializers.ModelSerializer):
    product = ProductsSerializer()
    options = AtributOptionsSerializer(many=True)
    image = ThumbnailSerializer(alias='product_img')

    class Meta:
        model = ProductVariants
        fields = '__all__'


# product variant detail serializer
class ProductVariantDetailSerializer(serializers.ModelSerializer):
    product = ProductsSerializer()
    image = ThumbnailSerializer(alias='prod_photo')

    class Meta:
        model = ProductVariants
        exclude = ['color', 'options']

    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        language = self.context.get('request', {}).headers.get('Language')

        if not language:
            language = Languages.objects.filter(default=True).first().code

        color_label = Translations.objects.filter(key='color_label')

        if color_label.exists():
            color_label = color_label.first().value.get(language)
        else:
            color_label = None
        
        atributs = instance.product.category.atributs.all()
        colors = list(set([it.color for it in instance.product.variants.all()]))
        data['atributs'] = []

        for atr in atributs:
            data_dict = {}
            data_dict['name'] = JsonFieldSerializer(atr.name, context={'request': self.context.get('request')}).data
            data_dict['options'] = []

            for opt in atr.options.all():
                opt_dict = {}
                opt_dict['id'] = opt.id
                opt_dict['slug'] = opt.slug
                opt_dict['name'] = JsonFieldSerializer(opt.name, context={'request': self.context.get('request')}).data
                opt_dict['curent'] = opt in instance.options.all()

                data_dict['options'].append(opt_dict)

            data['atributs'].append(data_dict)

        
        data['colors'] = []
        if instance.color:
            for color in colors:
                color_opt_dict = {}
                color_opt_dict['id'] = color.id
                color_opt_dict['slug'] = color.slug
                color_opt_dict['name'] = JsonFieldSerializer(color.name, context={'request': self.context.get('request')}).data
                color_opt_dict['curent'] = color == instance.color

            data['colors'].append(color_opt_dict)


        return data


# articles
class ArticleSerializer(serializers.ModelSerializer):
    title = JsonFieldSerializer()
    subtitle = JsonFieldSerializer()
    body = JsonFieldSerializer()
    created_date = serializers.DateField(format="%d.%m.%Y")
    image = ThumbnailSerializer(alias='prod_photo')
    author = serializers.ReadOnlyField(source='author.username')
    meta = MetaFieldSerializer()

    class Meta:
        model = Articles
        fields = '__all__'


# static information
class StaticInformationSerializer(serializers.ModelSerializer):
    title = JsonFieldSerializer()
    subtitle = JsonFieldSerializer()
    deskription = JsonFieldSerializer()
    about_us = JsonFieldSerializer()
    adres = JsonFieldSerializer()
    work_time = JsonFieldSerializer()
    logo_first = ThumbnailSerializer(alias='prod_photo')
    logo_second = ThumbnailSerializer(alias='prod_photo')

    class Meta:
        model = StaticInformation
        exclude = ['id']


# translation serializer
class TranslationSerializer(serializers.Serializer):
    def to_representation(self, instance):
        data = {}

        for item in instance:
            language = self.context['request'].headers.get('Language')

            if not language:
                language = Languages.objects.filter(default=True).first().code

            val = item.value.get(language, '')
            key = str(item.group.sub_text) + '.' + str(item.key)
            data[key] = val

        return data


# class TransaltionForDostonaka
class TranslationsSerializerBadVersion(serializers.Serializer): 
    def to_representation(self, instance):
        data = {}
        languages = Languages.objects.filter(active=True)
        
        for lang in languages:
            data[lang.code] = {}
            new_data = {}
            for item in instance:
                val = item.value.get(lang.code, '')
                key = str(item.key)
                new_data[key] = val

            data[lang.code] = new_data

        return data


# langs serializer
class LangsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Languages
        fields = '__all__'


# reviews serializer
class ReviewSerializer(serializers.ModelSerializer):
    title = JsonFieldSerializer()
    text = JsonFieldSerializer()
    image = ThumbnailSerializer(alias='avatar')

    class Meta:
        model = Reviews
        fields = '__all__'



# parnters serializer
class PartnersSerializer(serializers.ModelSerializer):
    name = JsonFieldSerializer()
    deckription = JsonFieldSerializer()
    image = ThumbnailSerializer(alias='avatar')

    class Meta:
        model = Partners
        fields = '__all__'



# short apl serializer
class ShortApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortApplication
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['full_name'] = instance.get_full_name()
        return data
