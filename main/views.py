from .models import Products, Category, AtributOptions, Atributs, ProductVariants, Colors, ShortApplication
from rest_framework import generics, views, pagination, filters
from .serializers import ProductsSerializer, Categoryserializer, ProductVariantSimpleSerializer, ReviewSerializer, ShortApplicationSerializer, TranslationsSerializerBadVersion
from .serializers import ArticleSerializer, StaticInformationSerializer, TranslationSerializer, LangsSerializer, PartnersSerializer, ProductVariantDetailSerializer, ArticleDetailSerializer
from admins.models import Articles, StaticInformation, Partners, Reviews, Translations, Languages
from rest_framework.response import Response
from .utils import search_func
# Create your views here.

# pagination
class BasePagination(pagination.PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 1000


# articles list
class ArticlesList(generics.ListAPIView):
    queryset = Articles.objects.filter(active=True)
    serializer_class = ArticleSerializer
    pagination_class = BasePagination


# articles detail
class ArticlesDetail(generics.RetrieveAPIView):
    queryset = Articles.objects.filter(active=True)
    serializer_class = ArticleDetailSerializer
    lookup_field = 'slug'


# static information
class StaticInfView(views.APIView):
    def get(self, request, format=None):
        try:
            obj = StaticInformation.objects.get(id=1)
        except:
            obj = StaticInformation.objects.create()

        serializer = StaticInformationSerializer(obj, context={'request': request})

        return Response(serializer.data)


# translations
class TranslationsView(views.APIView):
    def get(self, request, fromat=None):
        translations = Translations.objects.all()
        serializer = TranslationSerializer(translations, context={'request': request})
        return Response(serializer.data)


# langs list
class LangsList(generics.ListAPIView):
    queryset = Languages.objects.filter(active=True)
    serializer_class = LangsSerializer
    pagination_class = BasePagination


# reviews list
class ReviewList(generics.ListAPIView):
    queryset = Reviews.objects.filter(active=True)
    serializer_class = ReviewSerializer
    pagination_class = BasePagination


# partners list
class PartnersList(generics.ListAPIView):
    queryset = Partners.objects.all()
    serializer_class = PartnersSerializer
    pagination_class = BasePagination


# category list
class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = Categoryserializer
    pagination_class = BasePagination


# category detail
class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = Categoryserializer


# products list
class ProductsList(generics.ListAPIView):
    serializer_class = ProductVariantSimpleSerializer
    pagination_class = BasePagination


    def get_queryset(self):
        queryset = ProductVariants.objects.filter(default=True)
        ctg_id = self.request.GET.get("category")

        try:
            category = Category.objects.get(id=ctg_id)
            queryset = queryset.filter(product__category=category)
        except:
            pass

        return queryset


    def get(self, request, *args, **kwargs):
        ctg_id = self.request.GET.get("category")

        if ctg_id is not None:
            try:
                Category.objects.get(id=ctg_id)
            except:
                return Response({'error': 'There is no category with this ID'})


        return super().get(request, *args, **kwargs)


# product variant detail view
class ProductVariantDetail(generics.RetrieveAPIView):
    queryset = ProductVariants.objects.select_related('product').filter(product__active=True)
    serializer_class = ProductVariantDetailSerializer
    lookup_field = 'slug'


# top products view
class TopProductsView(generics.ListAPIView):
    serializer_class = ProductVariantSimpleSerializer
    queryset = ProductVariants.objects.select_related('product').filter(product__active=True).filter(top=True)
    pagination_class = BasePagination


# serach
class ProductsSearch(generics.ListAPIView):
    serializer_class = ProductVariantSimpleSerializer
    pagination_class = BasePagination
    

    def get_queryset(self): 
        queryset = ProductVariants.objects.select_related('product').filter(product__active=True).filter(default=True)
        q = self.request.GET.get('q')

        lang = self.request.headers.get("Languages", '')
        if lang == '':
            lang = Languages.objects.filter(active=True).filter(default=True).first().code
        

        for item in queryset:
            if q.lower() not in str(item.product.name.get(lang)).lower():
                queryset = queryset.exclude(id=item.id)
                    
        return queryset


    def get(self, request, *args, **kwargs):
        q = request.GET.get('q', '')

        if q == '':
            return Response({'error': 'q param is required'})

        return super().get(request, *args, **kwargs)


# search 
class Search(views.APIView):
    def get(self, request, fromat=None):
        q = request.GET.get("q", '')
        if q == '':
            return Response({'error': 'q param is required'})
        
        products = ProductVariants.objects.select_related('product').filter(product__active=True).filter(default=True).filter()
        categories = Category.objects.all()
        articles = Articles.objects.filter(active=True)

        articles_results = search_func(q, 'title', queryset=articles, fields=['subtitle', 'title', 'description', 'slug', 'created_date'], image_fields=['image'], request=request)
        product_results = search_func(q, 'name', queryset=products, fields=['slug', 'name', 'description'], image_fields=['image'], request=request, product=True)
        cotalog_results = search_func(q, 'name', queryset=categories, fields=['name', 'id'], image_fields=['image'], request=request)

        res_data = {}
        res_data['products'] = product_results
        res_data['categories'] = cotalog_results
        res_data['articles'] = articles_results


        return Response(res_data)


# application add
class NewAppliction(generics.CreateAPIView):
    serializer_class = ShortApplicationSerializer
    queryset = ShortApplication.objects.all()



# product variant get
class ProductVariantGet(views.APIView):
    def get(self, request, format=None):
        product_slug = request.GET.get('product', '')
        product = Products.objects.filter(slug=product_slug)

        if product.exists():
            product = product.first()
        else:
            return Response({'detail': 'Error. There is no product with this slug.'})
        
        color_id = request.GET.get("color", 0) 
        color = Colors.objects.filter(id=int(color_id))

        if color.exists():
            color = color.first()
        else:
            return Response({'detail': 'Color id is invalid or empty'})


        variants = ProductVariants.objects.filter(product=product).filter(color=color)


        options_list = []
        for key, value in request.GET.items():
            if 'option_' in str(key):
                option = AtributOptions.objects.filter(id=int(value))

                if option.exists():
                    options_list.append(option.first())
                else:
                    return Response({'detail': 'option id is invalid'})

        excepted_count = product.category.atributs.count()
        
        if len(options_list) != excepted_count:
            return Response({'error': f'There is {len(options_list)} options, but expected {excepted_count}'})

        if len(options_list) > 0:
            for opt in options_list:
                for var in variants:
                    if opt not in var.options.all():
                        variants = variants.exclude(id=var.id)

        if variants.exists():
            serialazer = ProductVariantDetailSerializer(variants.first(), context={'request': request})
            return Response(serialazer.data)
        else:
            return Response({'detail': 'There is no Product Variant with this options'})

        







        
        




