from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, FormView
from .models import Articles, Languages, Translations, TranlsationGroups, StaticInformation, AdminInputs, ArticleCategories, FAQ
from .models import ImageGalery, VideoGalery, AboutUs, MetaTags, telephone_validator, Reviews, Partners
from main.models import Products, Category, Atributs, AtributOptions, ProductVariants, Colors, ShortApplication
from .forms import LngForm, UserForm  # , ApplicationForm
from django.core.exceptions import ValidationError
import datetime
from django.db.models import Q
import json
from django.apps import apps
from django.http import JsonResponse, QueryDict, HttpResponseRedirect
from django.core.files.storage import default_storage
from .utils import *
from .serializers import TranslationSerializer
from django.contrib.auth.models import User
from django.contrib.auth import logout
from main.serializers import AtributSerializer
# Create your views here.

# based list view


class BasedListView(ListView):
    search_fields = list()

    def search(self, queryset, fields: list, model, *args, **kwargs):
        query = self.request.GET.get("q", '')

        langs = Languages.objects.filter(active=True)
        endlist = list()

        if query == '':
            return queryset

        queryset = queryset.values()

        for field in fields:
            for item in queryset:
                for lang in langs:
                    if query.lower() in str(item.get(field, {}).get(lang.code, '')).lower():
                        if item['id'] not in [it['id'] for it in endlist]:
                            endlist.append(item)
                    continue

        queryset = list_of_dicts_to_queryset(endlist, model)

        return queryset

    def get_queryset(self):
        queryset = self.model.objects.order_by('-id')
        queryset = self.search(queryset, self.search_fields, self.model)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(BasedListView, self).get_context_data(**kwargs)

        context['objects'] = get_lst_data(
            self.get_queryset(), self.request, 20)
        context['lang'] = Languages.objects.filter(
            active=True).filter(default=True).first()
        context['page_obj'] = paginate(self.get_queryset(), self.request, 20)
        context['url'] = search_pagination(self.request)

        return context


# based create view
class BasedCreateView(CreateView):
    related_model = None
    related_model_varb_name = None
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(BasedCreateView, self).get_context_data(**kwargs)
        context['langs'] = Languages.objects.filter(
            active=True).order_by('-default')
        context['lang'] = Languages.objects.filter(default=True).first()
        context['fields'] = get_model_fields(self.model)

        if self.related_model is not None:
            context['relateds'] = self.related_model.objects.order_by('-id')

        context['dropzone_key'] = self.model._meta.verbose_name
        context['images'] = []

        if self.request.session.get(context['dropzone_key']):
            context['images'] = list({'name': it['name'], 'id': clean_text(
                it['name'])} for it in self.request.session[context['dropzone_key']] if it['id'] == '')

        return context

    def form_valid(self, form):
        return None


# home admin
def home(request):
    return render(request, 'admin/base_template.html')


# delete model item
def delete_item(request):
    model_name = request.POST.get("model_name_del")
    app_name = request.POST.get('app_name_del')
    id = request.POST.get('item_id')
    url = request.POST.get("url")

    try:
        model = apps.get_model(model_name=model_name, app_label=app_name)
        model.objects.get(id=int(id)).delete()
    except:
        pass

    return redirect(url)


def delete_alot(request):
    model_name = request.POST.get("model_name")
    app_name = request.POST.get('app_name')
    id_list = request.POST.getlist('id')

    url = request.POST.get('url')

    try:
        model = apps.get_model(model_name=model_name, app_label=app_name)
        for item in id_list:
            if f'id[{item}]' in request.POST:
                model.objects.get(id=int(item)).delete()
    except:
        pass

    return redirect(url)


# save images
def save_images(request):
    if request.method == 'POST':
        key = request.POST.get("key")
        file = request.FILES.get('file')
        id = request.POST.get("id")

        request.session[key] = request.session.get(key, [])
        file_name = default_storage.save('dropzone/' + file.name, file)

        data = {
            'id': id,
            'name': file_name
        }

        request.session[key].append(data)
        request.session.modified = True

    return JsonResponse(file_name, safe=False)


# del lang icond
def del_lang_icon(request):
    id = request.POST.get("item_id")
    url = request.POST.get('url')
    try:
        Languages.objects.get(id=int(id)).icon.delete()
    except:
        pass

    return redirect(url)


# delete article group image
def delete_article_group_img(request):
    id = request.POST.get('item_id')

    try:
        ArticleCategories.objects.get(id=int(id)).image.delete()
    except:
        return JsonResponse("error", safe=False)

    return JsonResponse('success', safe=False)


# add static image
def add_static_image(request):
    url = request.POST.get('url')
    key = request.POST.get("key")
    file = request.FILES.get('file')


    try:
        model = StaticInformation.objects.get(id=1)

        if key == 'logo1':
            model.logo_first = file
        elif key == 'logo2':
            model.logo_second = file

        model.save()
    except:
        pass

    return redirect(url)


# delete article images
def del_statics_image(request):
    url = request.POST.get('url')
    key = request.POST.get("key")

    try:
        model = StaticInformation.objects.get(id=1)

        if key == 'logo1':
            model.logo_first.delete()
        elif key == 'logo2':
            model.logo_second.delete()
        elif key == 'cotalog':
            model.cotalog.delete()

        model.save()
    except:
        pass

    return redirect(url)


# delete image
def delete_image(request):
    if request.method == 'POST':
        key = request.POST.get('key')
        file = request.POST.get("file")

        if request.session.get(key):
            for it in request.session[key]:
                if it['name'] == file:
                    request.session[key].remove(it)
                    request.session.modified = True

    return redirect(request.META.get("HTTP_REFERER"))


# articles create
class ArticleCreateView(BasedCreateView):
    model = Articles
    template_name = 'admin/new_article.html'
    success_url = 'articles_list'

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data_dict = serialize_request(self.model, request)
        data_dict['created_date'] = data_dict.get(
            'created_date', str(datetime.date.today()))
        data_dict['author'] = request.user
        key = request.POST.get('dropzone-key')

        data = self.get_context_data()

        if is_valid_field(data_dict, 'title') == False:
            data['request_post'] = data_dict
            data['error'] = 'This field is required.'
            return render(request, self.template_name, data)

        try:
            article = Articles(**data_dict)
            article.full_clean()
            article.save()

            key = self.model._meta.verbose_name
            sess_images = request.session.get(key)

            if sess_images and len([it for it in request.session.get(key) if it['id'] == '']) > 0:
                image = [it for it in request.session.get(
                    key) if it['id'] == ''][0]

                article.image = image['name']
                article.save()
                request.session.get(key).remove(image)
                request.session.modified = True

            meta_dict = serialize_request(MetaTags, request)
            try:
                meta = MetaTags(**meta_dict)
                meta.full_clean()
                meta.save()
                article.meta = meta
                article.save()
            except:
                pass

            article.save()

        except ValidationError:
            pass

        return redirect('articles_list')  # redirect("")


# articles list
class ArticlesList(BasedListView):
    model = Articles
    template_name = 'admin/articles_list.html'
    search_fields = ['title', 'body']


# article update
class ArticleUpdate(UpdateView):
    model = Articles
    template_name = 'admin/new_article.html'
    success_url = 'articles_list'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(ArticleUpdate, self).get_context_data(**kwargs)
        context['langs'] = Languages.objects.filter(
            active=True).order_by('-default')
        context['lang'] = Languages.objects.filter(default=True).first()
        context['fields'] = get_model_fields(self.model)
        context['relateds'] = ArticleCategories.objects.order_by('-id')
        context['dropzone_key'] = self.model._meta.verbose_name

        return context

    def post(self, request, *args, **kwargs):
        context = super().post(request, *args, **kwargs)
        data_dict = serialize_request(self.model, request)
        key = self.model._meta.verbose_name

        data = self.get_context_data()
        if is_valid_field(data_dict, 'title') == False:
            data['request_post'] = data_dict
            data['error'] = 'This field is required.'
            return render(request, self.template_name, data)

        try:
            file = [it for it in request.session.get(
                key, []) if it['id'] == str(self.get_object().pk)][0]
        except:
            file = None

        try:
            instance = self.get_object()

            for attr, value in data_dict.items():
                setattr(instance, attr, value)

            instance.save()

            if file:
                instance.image = file['name']
                for it in request.session.get(key):
                    if it['id'] == str(self.get_object().pk):
                        try:
                            request.session.get(key).remove(it)
                            request.session.modified = True
                        except:
                            pass
                instance.save()

            meta_dict = serialize_request(MetaTags, request)
            meta = instance.meta
            if meta is None:
                meta = MetaTags.objects.create()
                instance.meta = meta
                instance.save()

            try:
                for attr, value in meta_dict.items():
                    if str(attr) != 'id':
                        setattr(instance.meta, attr, value)
                instance.meta.save()
            except:
                pass

        except ValidationError:
            pass

        return redirect('articles_list')


# langs list
class LangsList(ListView):
    model = Languages
    context_object_name = 'langs'
    template_name = 'admin/lang_list.html'

    def get_queryset(self):
        queryset = Languages.objects.all().order_by('-default')
        query = self.request.GET.get("q")
        if query == '':
            query = None

        if query:
            queryset = queryset.filter(
                Q(name__iregex=query) | Q(code__iregex=query))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(LangsList, self).get_context_data(**kwargs)
        context['q'] = self.request.GET.get("q")
        context['langs'] = get_lst_data(self.get_queryset(), self.request, 20)
        context['page_obj'] = paginate(self.get_queryset(), self.request, 20)
        context['url'] = search_pagination(self.request)

        return context


# langs create
class LngCreateView(CreateView):
    model = Languages
    form_class = LngForm
    success_url = '/admin/langs'
    template_name = "admin/lng_create.html"

    def form_valid(self, form):
        lang_save(form, self.request)

        return redirect('langs_list')

    def get_context_data(self, **kwargs):
        context = super(LngCreateView, self).get_context_data(**kwargs)
        context['fields'] = get_model_fields(self.model)
        context['dropzone_key'] = self.model._meta.verbose_name
        context['images'] = []

        if self.request.session.get(context['dropzone_key']):
            context['images'] = list({'name': it['name'], 'id': clean_text(str(
                it['name']))} for it in self.request.session[context['dropzone_key']] if it['id'] == '')

        return context


# langs update
class LangsUpdate(UpdateView):
    model = Languages
    form_class = LngForm
    success_url = '/admin/langs'
    template_name = "admin/lng_create.html"

    def get_context_data(self, **kwargs):
        context = super(LangsUpdate, self).get_context_data(**kwargs)
        context['fields'] = get_model_fields(self.model)
        context['dropzone_key'] = self.model._meta.verbose_name

        return context

    def form_valid(self, form):
        lang_save(form, self.request)

        return redirect('langs_list')


# langs delete
def delete_langs(request):
    if request.method == 'POST':
        lng_id = request.POST.get("id")
        try:
            Languages.objects.get(id=int(lng_id)).delete()
        except:
            pass

        url = request.POST.get("url", request.META.get('HTTP_REFERER'))

        return redirect(url)


# static update
class StaticUpdate(UpdateView):
    model = StaticInformation
    fields = "__all__"
    template_name = 'admin/static_add.html'
    success_url = '/admin/'

    def get_object(self):
        try:
            object = StaticInformation.objects.get(id=1)
        except:
            object = StaticInformation.objects.create()

        return object

    def get_context_data(self, **kwargs):
        context = super(StaticUpdate, self).get_context_data(**kwargs)
        context['langs'] = Languages.objects.filter(active=True).order_by('-default')
        context['dropzone_key'] = self.model._meta.verbose_name

        return context

    def form_valid(self, form):
        return None

    def post(self, request, *args, **kwargs):
        context = super().post(request, *args, **kwargs)
        data_dict = serialize_request(StaticInformation, request)
        instance = self.get_object()
        cotalog = request.FILES.get("cotalog")

        data = self.get_context_data()
        if is_valid_field(data_dict, 'title') == False:
            data['request_post'] = data_dict
            data['error'] = 'This field is required'
            return render(request, self.template_name, data)
        else:
            try:
                for attr, value in data_dict.items():
                    setattr(instance, attr, value)

                if cotalog:
                    instance.cotalog = cotalog

                instance.save()
            except:
                data['request_post'] = data_dict
                data['error_all'] = 'There is some errors'
                return render(request, self.template_name, data)

        return redirect('static_info')


def class_list():
    my_apps = ['admins']
    my_app_models = [apps.all_models[name] for name in my_apps]
    return my_app_models


# translations list
class TranslationList(ListView):
    model = Translations
    template_name = 'admin/translation_list.html'

    def get_queryset(self):
        queryset = Translations.objects.order_by("-id")
        query = self.request.GET.get("q")
        queryset = search_translation(query, queryset)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(TranslationList, self).get_context_data(**kwargs)
        context['groups'] = TranlsationGroups.objects.all()
        context['langs'] = Languages.objects.filter(
            active=True).order_by('-default')
        context['url'] = search_pagination(self.request)

        # pagination
        context['translations'] = get_lst_data(
            self.get_queryset(), self.request, 20)
        context['page_obj'] = paginate(self.get_queryset(), self.request, 20)

        return context


# translation group
class TranslationGroupDetail(DetailView):
    model = TranlsationGroups
    template_name = 'admin/translation_list.html'

    def get_context_data(self, **kwargs):
        context = super(TranslationGroupDetail,
                        self).get_context_data(**kwargs)
        context['groups'] = TranlsationGroups.objects.all()
        context['langs'] = Languages.objects.filter(
            active=True).order_by('-default')
        lst_one = self.get_object().translations.order_by('-id')

        # search
        query = self.request.GET.get("q")
        lst_one = search_translation(query, lst_one)

        # range
        lst_two = range(1, len(lst_one) + 1)

        # zip 2 lst
        context['translations'] = dict(pairs=zip(lst_one, lst_two))

        return context


# transtion update
def translation_update(request):
    if request.method == 'GET':
        id = request.GET.get('id')

        try:
            translation = Translations.objects.get(id=int(id))
            serializer = TranslationSerializer(translation)

            return JsonResponse(serializer.data)
        except:
            return JsonResponse({'error': 'error'}, safe=False)

    elif request.method == 'POST':
        data = serialize_request(Translations, request)
        id = request.POST.get("id")
        lang = Languages.objects.filter(
            active=True).filter(default=True).first()

        if data.get('value').get(lang.code, '') == '':
            return JsonResponse({'lng_error': 'This language is required'})

        try:
            translation = Translations.objects.get(id=int(id))
            key = data.get('key', '')

            if key == '':
                return JsonResponse({'key_error': 'Key is required'})

            if str(key) in [str(it.key) for it in Translations.objects.filter(group=translation.group).exclude(id=translation.pk)]:
                return JsonResponse({'key_error': 'Key is already in use'})

            translation.key = key
            translation.value = data['value']
            translation.full_clean()
            translation.save()
        except:
            return JsonResponse('some error', safe=False)

        serializer = TranslationSerializer(translation)

        return JsonResponse(serializer.data)


# add translation group
def add_trans_group(request):
    if request.method == 'POST':
        data_dict = serialize_request(TranlsationGroups, request)

        if data_dict.get('sub_text', '') == '':
            return JsonResponse({'key_error': 'Sub text is required'})
        elif (data_dict.get('sub_text'), ) in TranlsationGroups.objects.values_list('sub_text'):
            return JsonResponse({'key_error': 'This key is already in use'})

        try:
            transl_group = TranlsationGroups(**data_dict)
            transl_group.full_clean()
            transl_group.save()
        except ValidationError:
            return JsonResponse({'title_error': 'This title is empty or already in use'})

        data = {
            'id': transl_group.id,
            'name': transl_group.title,
            'key': transl_group.sub_text
        }
        return JsonResponse(data)


# translation group udate
class TranslationGroupUdpate(UpdateView):
    model = TranlsationGroups
    template_name = 'admin/translation_edit.html'
    fields = '__all__'
    success_url = '/admin/translations'

    def get_context_data(self, **kwargs):
        context = super(TranslationGroupUdpate,
                        self).get_context_data(**kwargs)
        context['groups'] = TranlsationGroups.objects.all()
        context['langs'] = Languages.objects.filter(
            active=True).order_by('-default')
        context['lng'] = Languages.objects.filter(
            active=True).filter(default=True).first()
        lst_one = self.get_object().translations.all()

        # range
        lst_two = range(1, len(lst_one) + 1)

        # zip 2 lst
        context['translations'] = dict(pairs=zip(lst_one, lst_two))

        return context

    def post(self, request, *args, **kwargs):
        transls = list(self.get_object().translations.all())
        langs = Languages.objects.filter(active=True).order_by('-default')
        lang = Languages.objects.filter(
            active=True).filter(default=True).first()
        items_count = request.POST.get("item_count")

        data = []
        for l in range(1, int(items_count) + 1):
            new_data = {}
            new_data['id'] = l
            new_data['key'] = request.POST[f'key[{l}]']
            new_data['values'] = []
            for lng in langs:
                new_data['values'].append(
                    {'key': f'value[{l}][{lng.code}]', 'value': request.POST[f'value[{l}][{lng.code}]'], 'def_lang': lang.code, 'lng': lng.code})

            data.append(new_data)

        objects = dict(pairs=zip(data, list(range(1, int(items_count) + 1))))

        for i in range(len(transls)):
            transls[i].key = request.POST.get(f'key[{i + 1}]', '')

            if transls[i].key == '':
                return render(request, template_name=self.template_name, context={'key_errors': {str(i+1): 'Key is required'},  'new_objects': objects, 'langs': langs, 'len': int(items_count) + 1})

            in_default_lng = request.POST.get(f'value[{i+1}][{lang.code}]', '')

            if in_default_lng == '':
                return render(request, template_name=self.template_name, context={'lng_errors': {str(i+1): 'This language is required'}, 'new_objects': objects, 'langs': langs, 'len': int(items_count) + 1})

            value_dict = {}
            for lang in langs:
                value_dict[str(lang.code)
                           ] = request.POST[f'value[{i + 1}][{lang.code}]']

            transls[i].value = value_dict
            try:
                transls[i].full_clean()
                transls[i].save()
            except:
                return render(request, template_name=self.template_name, context={'key_errors': {str(i): 'Key is alredy in use'},  'new_objects': objects, 'langs': langs, 'len': items_count})

        for i in range(len(transls) + 1, int(items_count) + 1):
            new_trans = Translations()
            data = {}
            new_trans.key = request.POST.get(f'key[{i}]', '')

            if new_trans.key == '':
                return render(request, template_name=self.template_name, context={'key_errors': {str(i): 'Key is required'},  'new_objects': objects, 'langs': langs, 'len': items_count})

            value_dict = {}
            in_default_lng = request.POST.get(f'value[{i}][{lang.code}]', '')

            if in_default_lng == '':
                return render(request, template_name=self.template_name, context={'lng_errors': {str(i): 'This language is required'}, 'new_objects': objects, 'langs': langs, 'len': items_count})

            for lang in langs:
                value_dict[str(lang.code)
                           ] = request.POST[f'value[{i}][{lang.code}]']

            new_trans.value = value_dict
            new_trans.group = self.get_object()

            try:
                new_trans.full_clean()
                new_trans.save()
            except:
                return render(request, template_name=self.template_name, context={'key_errors': {str(i): 'Key is alredy in use'}, 'new_objects': objects, 'langs': langs, 'len': items_count})

        return redirect('transl_group_detail', pk=self.get_object().id)


# article ctg list
class ArticleCtgList(BasedListView):
    model = ArticleCategories
    template_name = 'admin/article_ctg.lst.html'
    search_fields = ['name']


# add article ctg
class AddArticleCtg(BasedCreateView):
    model = ArticleCategories
    template_name = 'admin/article_ctg_form.html'
    fields = '__all__'
    success_url = 'article_ctg_list'
    related_model = ArticleCategories

    def form_valid(self, form):
        return None

    def post(self, request, *args, **kwargs):
        context = super().post(request, *args, **kwargs)
        data_dict = serialize_request(self.model, request)

        data = self.get_context_data()
        try:
            data_dict['parent'] = ArticleCategories.objects.get(
                id=int(data_dict.get('parent')))
        except:
            if data_dict.get("parent"):
                del data_dict['parent']

        if is_valid_field(data_dict, 'name') == False:
            data['request_post'] = data_dict
            data['error'] = 'This field is required.'
            return render(request, self.template_name, data)
        else:
            try:
                art_ctg = ArticleCategories(**data_dict)
                art_ctg.full_clean()
                art_ctg.save()

                key = self.model._meta.verbose_name
                sess_images = request.session.get(key)

                if sess_images and len([it for it in request.session.get(key) if it['id'] == '']) > 0:
                    image = [it for it in request.session.get(
                        key) if it['id'] == ''][0]

                    art_ctg.image = image['name']
                    art_ctg.save()
                    request.session.get(key).remove(image)
                    request.session.modified = True
            except:
                pass

        return redirect('article_ctg_list')


# article ctg edit
class ArticleCtgEdit(UpdateView):
    model = ArticleCategories
    fields = "__all__"
    template_name = 'admin/article_ctg_form.html'
    success_url = '/admin/article_categories'

    def get_context_data(self, **kwargs):
        context = super(ArticleCtgEdit, self).get_context_data(**kwargs)
        context['langs'] = Languages.objects.filter(
            active=True).order_by('-default')
        context['relateds'] = ArticleCategories.objects.exclude(
            id=self.get_object().id).order_by('-id')
        context['lang'] = Languages.objects.filter(
            active=True).filter(default=True).first()
        context['dropzone_key'] = self.model._meta.verbose_name

        return context

    def form_valid(self, form):
        return None

    def post(self, request, *args, **kwargs):
        context = super().post(request, *args, **kwargs)
        data_dict = serialize_request(self.model, self.request)
        key = self.model._meta.verbose_name
        try:
            file = [it for it in request.session.get(
                key, []) if it['id'] == str(self.get_object().id)][0]
        except:
            file = None

        try:
            data_dict['parent'] = ArticleCategories.objects.get(
                id=int(data_dict.get('parent')))
        except:
            if data_dict.get("parent"):
                del data_dict['parent']

        data = self.get_context_data()
        if is_valid_field(data_dict, 'name') == False:
            data['request_post'] = data_dict
            data['error'] = 'This field is required.'
            return render(request, self.template_name, data)

        instance = self.get_object()

        for attr, value in data_dict.items():
            setattr(instance, attr, value)

        instance.save()

        if file:
            instance.image = file['name']
            for it in request.session.get(key):
                if it['id'] == str(self.get_object().id):
                    try:
                        request.session.get(key).remove(it)
                        request.session.modified = True
                    except:
                        pass
            instance.save()

        return redirect('article_ctg_list')

# delete about us video


def delete_about_video(request):
    try:
        model = AboutUs.objects.get(id=1)
        model.video.delete()
    except:
        return JsonResponse("error", safe=False)

    return JsonResponse("success", safe=False)


# set about video
def set_about_video(request):
    video = request.FILES.get("file")
    try:
        model = AboutUs.objects.get(id=1)
    except:
        model = AboutUs().save()
        return JsonResponse({'error': 'error'})

    model.video = video
    model.save()

    return JsonResponse('success', safe=False)

# super users list


class AdminsList(BasedListView):
    model = User
    template_name = 'admin/moterators_list.html'

    def get_queryset(self):
        queryset = User.objects.filter(is_superuser=True)
        query = self.request.GET.get("q", '')

        if query != '':
            queryset = queryset.filter(Q(username__iregex=query) | Q(
                first_name__iregex=query) | Q(last_name__iregex=query))

        return queryset


# super user create
class AdminCreate(CreateView):
    model = User
    form_class = UserForm
    success_url = '/'
    template_name = 'admin/moder_form.html'

    def form_valid(self, form):
        new_user = form.save()
        new_user.is_superuser = True
        full_name = self.request.POST.get("name")

        if full_name:
            if len(full_name.split(' ')) == 1:
                new_user.first_name = full_name.split(' ')[0]

            if len(full_name.split(' ')) == 2:
                new_user.last_name = full_name.split(' ')[1]

        new_user.save()

        return redirect('admin_list')


# admin udate
class AdminUpdate(UpdateView):
    model = User
    form_class = UserForm
    success_url = '/'
    template_name = 'admin/moder_form.html'

    def get_context_data(self, **kwargs):
        context = super(AdminUpdate, self).get_context_data(**kwargs)
        context['full_name'] = None

        if self.get_object().first_name:
            context['full_name'] = self.get_object().first_name

        if self.get_object().last_name:
            context['full_name'] += self.get_object().last_name

        return context

    def form_valid(self, form):
        user = form.save()
        user.is_superuser = True
        full_name = self.request.POST.get("name")

        if full_name:
            if len(full_name.split(' ')) == 1:
                user.first_name = full_name.split(' ')[0]

            if len(full_name.split(' ')) == 2:
                user.last_name = full_name.split(' ')[1]

        user.save()

        return redirect('admin_list')


# del article image
def delete_article_image(request):
    id = request.POST.get("item_id")

    try:
        Articles.objects.get(id=int(id)).image.delete()
    except:
        return JsonResponse({'detail': 'error'})

    return JsonResponse('success', safe=False)


# quic applications
class ShortApplicationList(BasedListView):
    model = ShortApplication
    template_name = 'admin/short_apls.html'


# short application update
class ShortApplicationUpdate(UpdateView):
    model = ShortApplication
    fields = ['nbm', 'status', 'first_name', 'last_name']
    template_name = 'admin/short_apl_edit.html'
    success_url = '/admin/quick_applications'

    def get_context_data(self, **kwargs):
        context = super(ShortApplicationUpdate,
                        self).get_context_data(**kwargs)
        context['statuses'] = ["На рассмотрении", "Рассмотрено", "Отклонено"]
        context['lang'] = Languages.objects.filter(default=True).first()

        return context


# class reviews list
class ReviewsList(BasedListView):
    model = Reviews
    template_name = 'admin/reviews_list.html'
    search_fields = ['title']


# reviews crete
class ReviewsCreate(BasedCreateView):
    model = Reviews
    fields = '__all__'
    template_name = 'admin/reviews_form.html'

    def post(self, request, *args, **kwargs):
        context = super().post(request, *args, **kwargs)
        data_dict = serialize_request(self.model, request)
        data = self.get_context_data()
        req_fields = ['title', 'text']

        for field in req_fields:
            if is_valid_field(data_dict, field) == False:
                data['request_post'] = data_dict
                data[f'{field}_error'] = 'This field is required.'
                return render(request, self.template_name, data)

        rating = data_dict.get('rating', 0)
        if type(rating) == float or int(rating) < 0 or int(rating) > 5:
            data['request_post'] = data_dict
            data['rating_error'] = 'Рейтинг должен быть натуральным числом в интервале от 0 до 5'
            return render(request, self.template_name, data)

        try:
            review = Reviews(**data_dict)
            review.full_clean()
            review.save()

            key = self.model._meta.verbose_name
            sess_images = request.session.get(key)

            if sess_images and len([it for it in request.session.get(key) if it['id'] == '']) > 0:
                image = [it for it in request.session.get(
                    key) if it['id'] == ''][0]

                review.image = image['name']
                review.save()
                request.session.get(key).remove(image)
                request.session.modified = True
        except:
            pass

        return redirect('review_list')


# reviews update
class ReviewsUpdate(UpdateView):
    model = Reviews
    fields = '__all__'
    template_name = 'admin/reviews_form.html'

    def get_context_data(self, **kwargs):
        context = super(ReviewsUpdate, self).get_context_data(**kwargs)
        context['langs'] = Languages.objects.filter(
            active=True).order_by('-default')
        context['dropzone_key'] = self.model._meta.verbose_name
        return context

    def form_valid(self, form):
        return None

    def post(self, request, *args, **kwargs):
        context = super().post(request, *args, **kwargs)
        data_dict = serialize_request(self.model, request)
        data = self.get_context_data()

        if is_valid_field(data_dict, 'title') == False:
            data['request_post'] = data_dict
            data['title_error'] = 'This field is required.'
            return render(request, self.template_name, data)

        if is_valid_field(data_dict, 'text') == False:
            data['request_post'] = data_dict
            data['text_error'] = 'This field is required.'
            return render(request, self.template_name, data)

        rating = data_dict.get('rating', 0)
        if type(rating) == float or int(rating) < 0 or int(rating) > 5:
            data['request_post'] = data_dict
            data['rating_error'] = 'Рейтинг должен быть натуральным числом в интервале от 0 до 5'
            return render(request, self.template_name, data)

        instance = self.get_object()
        key = self.model._meta.verbose_name

        for attr, value in data_dict.items():
            setattr(instance, attr, value)

        try:
            file = [it for it in request.session.get(
                key, []) if it['id'] == str(self.get_object().id)][0]
        except:
            file = None

        if file:
            instance.image = file['name']
            for it in request.session.get(key):
                if it['id'] == str(self.get_object().id):
                    try:
                        request.session.get(key).remove(it)
                        request.session.modified = True
                    except:
                        pass

        instance.save()

        return redirect("review_list")


# del review image
def delete_review_image(request):
    id = request.POST.get('obj_id')
    try:
        model = Reviews.objects.get(id=id)
        model.image.delete()
    except:
        return JsonResponse("error", safe=False)

    return JsonResponse("success", safe=False)


# logout
def logout_view(request):
    logout(request)

    return redirect('login_admin')


# partners
class PartnersList(BasedListView):
    model = Partners
    template_name = 'admin/partners.html'
    search_fields = ['name']


# partners create
class PartnersCreate(BasedCreateView):
    model = Partners
    fields = "__all__"
    template_name = 'admin/partners_form.html'

    def post(self, request, *args, **kwargs):
        context = super().post(request, *args, **kwargs)
        data_dict = serialize_request(self.model, request)
        data = self.get_context_data()

        if is_valid_field(data_dict, 'name') == False:
            data['request_post'] = data_dict
            data['name_error'] = 'This field is required.'
            return render(request, self.template_name, data)

        try:
            partner = Partners(**data_dict)
            partner.full_clean()
            partner.save()

            key = self.model._meta.verbose_name
            sess_images = request.session.get(key)
            images = [it for it in request.session.get(key) if it['id'] == '']

            if sess_images and len(images) > 0:
                image = images[0]

                partner.image = image['name']
                partner.save()
                request.session.get(key).remove(image)
                request.session.modified = True
        except:
            pass

        return redirect('partners_list')


# pertners eidt
class PartnersEdit(UpdateView):
    model = Partners
    fields = "__all__"
    template_name = 'admin/partners_form.html'

    def get_context_data(self, **kwargs):
        context = super(PartnersEdit, self).get_context_data(**kwargs)
        context['langs'] = Languages.objects.filter(
            active=True).order_by('-default')
        context['lang'] = Languages.objects.filter(default=True).first()
        context['dropzone_key'] = self.model._meta.verbose_name

        return context

    def form_valid(self, form):
        return None

    def post(self, request, *args, **kwargs):
        context = super().post(request, *args, **kwargs)
        data_dict = serialize_request(self.model, request)
        data = self.get_context_data()

        if is_valid_field(data_dict, 'name') == False:
            data['request_post'] = data_dict
            data['name_error'] = 'This field is required.'
            return render(request, self.template_name, data)

        instance = self.get_object()
        key = self.model._meta.verbose_name

        for attr, value in data_dict.items():
            setattr(instance, attr, value)

        try:
            file = [it for it in request.session.get(
                key, []) if it['id'] == str(self.get_object().id)][0]
        except:
            file = None

        if file:
            instance.image = file['name']
            for it in request.session.get(key):
                if it['id'] == str(self.get_object().id):
                    try:
                        request.session.get(key).remove(it)
                        request.session.modified = True
                    except:
                        pass

        instance.save()

        return redirect("partners_list")


# category list
class CategoryList(BasedListView):
    model = Category
    search_fields = ['name']
    template_name = 'admin/category_list.html'


# category create
class CategoryCreate(BasedCreateView):
    model = Category
    fields = '__all__'
    template_name = 'admin/category_form.html'
    related_model = Atributs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.session.get(f"{context['dropzone_key']}_image"):
            context['images'] = list({'name': it['name'], 'id': clean_text(str(
                it['name']))} for it in self.request.session[f"{context['dropzone_key']}_image"] if it['id'] == '')

        if self.request.session.get(f"{context['dropzone_key']}_icon"):
            context['icons'] = list({'name': it['name'], 'id': clean_text(str(
                it['name']))} for it in self.request.session[f"{context['dropzone_key']}_icon"] if it['id'] == '')

        return context

    def post(self, request, *args, **kwargs):
        context = super().post(request, *args, **kwargs)
        data_dict = serialize_request(self.model, request)
        data = self.get_context_data()
        atributs = request.POST.getlist('atributs[]')
        cotalog = request.FILES.get("cotalog")

        if is_valid_field(data_dict, 'name') == False:
            data['request_post'] = data_dict
            data['name_error'] = 'This field is required.'
            return render(request, self.template_name, data)

        try:
            category = Category(**data_dict)
            category.full_clean()
            category.save()

            if cotalog:
                category.cotalog = cotalog

            if atributs:
                try:
                    atr_list = [Atributs.objects.get(
                        id=int(it)) for it in atributs]
                    category.atributs.set(atr_list)
                except:
                    pass

            key = self.model._meta.verbose_name
            sess_images = request.session.get(f'{key}_image')
            if sess_images:
                images = [it for it in sess_images if it['id'] == '']

            if sess_images and len(images) > 0:
                image = images[0]

                category.image = image['name']
                request.session.get(f'{key}_image').remove(image)
                request.session.modified = True

            sess_icons = request.session.get(f'{key}_icon')

            if sess_icons:
                icons = [it for it in sess_icons if it['id'] == '']

            if sess_icons and len(icons) > 0:
                icon = icons[0]

                category.icon = icon['name']
                request.session.get(f'{key}_icon').remove(icon)
                request.session.modified = True

            category.save()
        except:
            data['request_post'] = data_dict
            data['some_error'] = 'This field is required.'
            return render(request, self.template_name, data)

        return redirect('category_list')


# category edit
class CategoryEdit(UpdateView):
    model = Category
    fields = '__all__'
    template_name = 'admin/category_form.html'

    def get_context_data(self, **kwargs):
        context = super(CategoryEdit, self).get_context_data(**kwargs)
        context['langs'] = Languages.objects.filter(
            active=True).order_by('-default')
        context['lang'] = Languages.objects.filter(default=True).first()
        context['dropzone_key'] = self.model._meta.verbose_name
        context['relateds'] = Atributs.objects.all()

        return context

    def form_valid(self, form):
        return None

    def post(self, request, *args, **kwargs):
        context = super().post(request, *args, **kwargs)
        data_dict = serialize_request(self.model, request)
        data = self.get_context_data()
        atributs = request.POST.getlist('atributs[]')
        cotalog = request.FILES.get("cotalog")

        if is_valid_field(data_dict, 'name') == False:
            data['request_post'] = data_dict
            data['name_error'] = 'This field is required.'
            return render(request, self.template_name, data)

        instance = self.get_object()
        key = self.model._meta.verbose_name

        for attr, value in data_dict.items():
            setattr(instance, attr, value)

        if cotalog:
            instance.cotalog = cotalog

        if atributs:
            try:
                atr_list = [Atributs.objects.get(
                    id=int(it)) for it in atributs]
                instance.atributs.set(atr_list)
            except:
                pass

        try:
            images = [it for it in request.session.get(
                f'{key}_image', []) if it['id'] == str(self.get_object().id)][0]
        except:
            images = None

        try:
            icons = [it for it in request.session.get(
                f'{key}_icon', []) if it['id'] == str(self.get_object().id)][0]
        except:
            icons = None

        if images:
            instance.image = images['name']
            for it in request.session.get(f'{key}_image'):
                if it['id'] == str(self.get_object().id):
                    try:
                        request.session.get(f'{key}_image').remove(it)
                        request.session.modified = True
                    except:
                        pass

        if icons:
            instance.icon = icons['name']
            for it in request.session.get(f'{key}_icon'):
                if it['id'] == str(self.get_object().id):
                    try:
                        request.session.get(f'{key}_icon').remove(it)
                        request.session.modified = True
                    except:
                        pass

        instance.save()

        return redirect("category_list")


def del_category_file(request):
    pk = request.POST.get('obj_id')
    key = request.POST.get('key')

    try:
        ctg = Category.objects.get(pk=int(pk))
        if key == 'image':
            ctg.image.delete()
        elif key == 'icon':
            ctg.icon.delete()
        elif key == 'cotalog':
            ctg.cotalog.delete()

        ctg.save()

    except:
        return JsonResponse("error", safe=False)

    return JsonResponse('success', safe=False)




# atributs
class AtributsList(BasedListView):
    model = Atributs
    search_fields = ['name']
    template_name = 'admin/atributs.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['langs'] = Languages.objects.filter(active=True)

        return context


# atributs create
class AtributsCreate(BasedCreateView):
    model = Atributs
    fields = '__all__'
    template_name = 'admin/atributs_form.html'

    def post(self, request, *args, **kwargs):
        context = super().post(request, *args, **kwargs)
        data_dict = serialize_request(self.model, request)
        data = self.get_context_data()
        options_count = request.POST.get("options_count", 0)
        lang = Languages.objects.filter(default=True).first()

        try:
            options = collect_options(int(options_count), request)
        except:
            options = collect_options(0, request)

        if is_valid_field(data_dict, 'name') == False:
            data['request_post'] = data_dict
            lst_one = options
            lst_two = range(1, len(options) + 1)
            data['options_list'] = dict(pairs=zip(lst_one, lst_two))
            data['name_error'] = 'This field is required.'
            return render(request, self.template_name, data)


        try:
            atribut = Atributs(**data_dict)
            atribut.full_clean()
            atribut.save()

            for l in range(1, int(options_count)+1):
                opt_dict = get_option_from_post(l, request)
                opt_dict['atribut'] = atribut

                if opt_dict.get('name', {}).get(lang.code, '') == '':
                    data['request_post'] = data_dict
                    data['opt_count'] = len(options)
                    lst_one = options
                    lst_two = range(1, len(options) + 1)
                    data['options_list'] = dict(pairs=zip(lst_one, lst_two))
                    data['error_option'] = {}
                    data['error_option'][f'{l}'] = 'This field is required.'
                    return render(request, self.template_name, data)

                try:
                    option = AtributOptions.objects.create(**opt_dict)
                    option.save()
                except:
                    pass

            '''lang = Languages.objects.filter(active=True).filter(default=True)

            if lang.exists():
                for opt in options:
                    opt_name = {lang.first().code: opt.get('value', '')}

                    options = AtributOptions.objects.create(
                        atribut=atribut, name=opt_name)
                    options.save()'''
        except:
            pass

        return redirect("atr_list")


# atributs edit
class AtributEdit(UpdateView):
    model = Atributs
    fields = '__all__'
    template_name = 'admin/atributs_form.html'

    def get_context_data(self, **kwargs):
        context = super(AtributEdit, self).get_context_data(**kwargs)
        context['langs'] = Languages.objects.filter(
            active=True).order_by('-default')
        context['lang'] = Languages.objects.filter(default=True).first()

        lst_one = self.get_object().options.all()
        lst_two = range(1, lst_one.count() + 1)
        context['options'] = dict(pairs=zip(lst_one, lst_two))

        return context

    def form_valid(self, form):
        return None

    def post(self, request, *args, **kwargs):
        context = super().post(request, *args, **kwargs)
        data_dict = serialize_request(self.model, request)
        data = self.get_context_data()
        options_count = request.POST.get("options_count", 0)
        old_count = self.get_object().options.count()
        lang = Languages.objects.filter(default=True).first()

        try:
            options = collect_options(int(options_count), request)
        except:
            options = collect_options(0, request)

        if is_valid_field(data_dict, 'name') == False:
            data['request_post'] = data_dict
            lst_one = options
            lst_two = range(1, len(options) + 1)
            data['options_list'] = dict(pairs=zip(lst_one, lst_two))
            data['name_error'] = 'This field is required.'
            return render(request, self.template_name, data)

        instance = self.get_object()

        for attr, value in data_dict.items():
            setattr(instance, attr, value)

        instance.save()


        for i in range(1, old_count + 1):
            opt_dict = get_option_from_post(i, request)

            if opt_dict.get('name', {}).get(lang.code, '') == '':
                data['request_post'] = data_dict
                data['opt_count'] = len(options)
                lst_one = options
                lst_two = range(1, len(options) + 1)
                data['options_list'] = dict(pairs=zip(lst_one, lst_two))
                data['error_option'] = {}
                data['error_option'][f'{i}'] = 'This field is required.'
                return render(request, self.template_name, data)



            try:
                option = instance.options.all()[i-1]


                for attr, value in opt_dict.items():
                    setattr(option, attr, value)
                option.save()
            except:
                pass


        for l in range(old_count+1, int(options_count)+1):
            opt_dict = get_option_from_post(l, request)
            opt_dict['atribut'] = instance

            if opt_dict.get('name', {}).get(lang.code, '') == '':
                data['request_post'] = data_dict
                data['opt_count'] = len(options)
                lst_one = options
                lst_two = range(1, len(options) + 1)
                data['options_list'] = dict(pairs=zip(lst_one, lst_two))
                data['error_option'] = {}
                data['error_option'][f'{l}'] = 'This field is required.'
                return render(request, self.template_name, data)

            try:
                option = AtributOptions.objects.create(**opt_dict)
                option.save()
            except:
                pass

        return redirect("atr_list")


# get option
def get_option(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        try:
            option = AtributOptions.objects.get(id=int(id))
        except:
            return JsonResponse({'error': 'id is invalid'})

    data = {}
    data['id'] = option.id

    for lang in Languages.objects.filter(active=True):
        data[lang.code] = option.name.get(lang.code, '')

    return JsonResponse(data)


# atribut options edit
class AtributOptionEdit(UpdateView):
    model = AtributOptions
    fields = '__all__'

    def get_object(self):
        try:
            id = self.request.POST.get("id")
            return AtributOptions.objects.get(id=int(id))
        except:
            return None

    def form_valid(self, form):
        return None

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data_dict = serialize_request(self.model, request)

        if is_valid_field(data_dict, 'name') == False:
            return JsonResponse({'error': 'Name is required'})

        instance = self.get_object()

        if instance:
            for attr, value in data_dict.items():
                setattr(instance, attr, value)

        instance.save()

        return JsonResponse('success', safe=False)


# colors
class ColorsList(BasedListView):
    model = Colors
    search_fields = ['name']
    template_name = 'admin/colors_list.html'


# colors create
class ColorsCreate(BasedCreateView):
    model = Colors
    fields = '__all__'
    template_name = 'admin/colors_form.html'

    def post(self, request, *args, **kwargs):
        context = super().post(request, *args, **kwargs)
        data_dict = serialize_request(self.model, request)
        data = self.get_context_data()

        if is_valid_field(data_dict, 'name') == False:
            data['request_post'] = data_dict
            data['name_error'] = 'This field is required.'
            return render(request, self.template_name, data)

        if data_dict.get('hex') is None:
            data['request_post'] = data_dict
            data['hex_error'] = 'This field is required.'
            return render(request, self.template_name, data)

        try:
            color = Colors(**data_dict)
            color.full_clean()
            color.save()
        except:
            pass

        return redirect('color_list')


# color edit
class ColorEdit(UpdateView):
    model = Colors
    fields = '__all__'
    template_name = 'admin/colors_form.html'

    def get_context_data(self, **kwargs):
        context = super(ColorEdit, self).get_context_data(**kwargs)
        context['langs'] = Languages.objects.filter(
            active=True).order_by('-default')
        context['lang'] = Languages.objects.filter(default=True).first()

        return context

    def form_valid(self, form):
        return None

    def post(self, request, *args, **kwargs):
        context = super().post(request, *args, **kwargs)
        data_dict = serialize_request(self.model, request)
        data = self.get_context_data()

        if is_valid_field(data_dict, 'name') == False:
            data['request_post'] = data_dict
            data['name_error'] = 'This field is required.'
            return render(request, self.template_name, data)

        instance = self.get_object()

        for attr, value in data_dict.items():
            setattr(instance, attr, value)

        instance.save()

        return redirect("color_list")


# products list
class ProductsList(BasedListView):
    model = Products
    search_fields = ['name']
    template_name = 'admin/products.html'


# checkbox to boolean
CHECKBOX_MAPPING = {'on': True, 'off': False}


# get variants data
def get_variants_list(request, range):
    end_variant_list = []
    
    for i in range:
        data_dict = {}
        data_dict['i'] = i
        data_dict['price'] = request.POST.get(f'price[{i}]')
        data_dict['code'] = request.POST.get(f'code[{i}]')

        option_ids = request.POST.getlist(f'option[{i}]')

        data_dict['options'] = []
        for it in option_ids:
            try:
                data_dict['options'].append(AtributOptions.objects.get(id=int(it)))
            except:
                pass   

        color_id = request.POST.get(f'color[{i}]')
        try:
            data_dict['color'] = Colors.objects.get(id=int(color_id))
        except:
            data_dict['color'] = None

        image = request.FILES.get(f'image[{i}]')
        if image:
            data_dict['image'] = image

        top_val = request.POST.get(f'top[{i}]', 'off')
        data_dict['top'] = CHECKBOX_MAPPING.get(top_val)

        default_val = request.POST.get(f'default[{i}]', 'off')
        data_dict['default'] = CHECKBOX_MAPPING.get(default_val)

        end_variant_list.append(data_dict)

    return end_variant_list


def costruct_variant_error(field, data, message, request_d, var_d, i):
    data['request_post'] = request_d
    
    rang = range(1, len(var_d) + 1)
    data['variants_request'] = dict(pairs=zip(var_d, rang))
    data[f'{field}_error'] = {}
    data[f'{field}_error']['error'] = message
    data[f'{field}_error']['item'] = i

    return data


def is_valid_variant(var_dict, i, data, product, data_dict, variant_list):
    valid = True
    if var_dict.get('price', '') == '' or 0 > float(var_dict['price']):
        data = costruct_variant_error(
            'price', data, 'This fiedl is required and shoulb be grater than 0', data_dict, variant_list, i)
        valid = False

    if var_dict.get('code') is None:
        data = costruct_variant_error(
            'code', data, 'This field is required', data_dict, variant_list, i)
        valid = False

    if len(var_dict.get('options')) != product.category.atributs.count():
        data = costruct_variant_error(
            'options', data, 'This options count is invalid', data_dict, variant_list, i)
        valid = False

    if var_dict.get('color') is None:
        data = costruct_variant_error(
            'color', data, 'Choosen color is invalid.', data_dict, variant_list, i)
        valid = False

    if valid is False:
        return {'valid': False, 'data': data}


    return {'valid': True}



# products create
class ProductsCreate(BasedCreateView):
    model = Products
    fields = '__all__'
    template_name = 'admin/products_form.html'
    related_model = Category


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['colors'] = Colors.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        context = super().post(request, *args, **kwargs)
        data_dict = serialize_request(self.model, request)
        category_id = request.POST.get('category', 0)

        data = self.get_context_data()
        variants_count = request.POST.get('variant_count')
        variant_list = get_variants_list(request, range(1, int(variants_count)+1))

        category = Category.objects.filter(id=int(category_id))
        
        if category.exists():
            data_dict['category'] = category.first()
        '''else:
            data['request_post'] = data_dict
            data['variants_request'] = variant_list
            data['category_error'] = 'This field is invalid.'
            return render(request, self.template_name, data)

        if variants_count is None:
            data['request_post'] = data_dict
            data['variants_request'] = variant_list
            return render(request, self.template_name, data)

        if is_valid_field(data_dict, 'name') == False:
            data['request_post'] = data_dict
            data['variants_request'] = variant_list
            data['name_error'] = 'This field is required.'
            return render(request, self.template_name, data)'''

        try:
            product = Products(**data_dict)
            product.full_clean()
            product.save()

            meta_dict = serialize_request(MetaTags, request)
            try:
                meta = MetaTags(**meta_dict)
                meta.full_clean()
                meta.save()
                product.meta = meta
                product.save()
            except:
                pass

            product.save()

            for var_dict in variant_list:
                var_dict['product'] = product
                options = var_dict.pop('options')
                del var_dict['i']
                try:
                    variant = ProductVariants.objects.create(**var_dict)
                    variant.options.set(options)
                    variant.full_clean()
                except:
                    pass
        except:
            pass

        return redirect("products_list")

        


# products edit
class ProductEdit(UpdateView):
    model = Products
    fields = '__all__'
    template_name = 'admin/products_form.html'

    def get_context_data(self, **kwargs):
        context = super(ProductEdit, self).get_context_data(**kwargs)
        context['langs'] = Languages.objects.filter(
            active=True).order_by('-default')
        context['lang'] = Languages.objects.filter(default=True).first()
        context['relateds'] = Category.objects.order_by('-id')
        context['colors'] = Colors.objects.all()
        variants = self.get_object().variants.all()
        rang = range(1, variants.count() + 1)

        context['variants'] = dict(pairs=zip(variants, rang))

        return context

    def form_valid(self, form):
        return None

    def post(self, request, *args, **kwargs):
        context = super().post(request, *args, **kwargs)
        data_dict = serialize_request(self.model, request)
        data = self.get_context_data()
        instance = self.get_object()
        category_id = request.POST.get('category')
        category = Category.objects.filter(id=int(category_id))

        if category.exists():
            data_dict['category'] = category.first()


        items_count = int(request.POST.get('variant_count', 0))
        old_count = instance.variants.count()
        
        for attr, value in data_dict.items():
            setattr(instance, attr, value)
        instance.save()

        meta_dict = serialize_request(MetaTags, request)
        try:
            meta = instance.meta
            if meta is None:
                meta = MetaTags.objects.create()
                instance.meta = meta
                instance.save()

            for attr, value in meta_dict.items():
                if str(attr) != 'id':
                    setattr(meta, attr, value)
            instance.meta.save()
        except:
            pass
        
        old_vars = get_variants_list(request, range(1, old_count+1))
        for vars in old_vars:
            try:
                variant = instance.variants.all()[vars['i']-1]
                options = vars.pop('options')

                for attr, value in vars.items():
                    setattr(variant, attr, value)
                variant.options.set(options)
                variant.save()
            except:
                pass

        new_vars = get_variants_list(request, range(old_count+1, items_count + 1))
        for var in new_vars:
            var['product'] = instance
            options = var.pop('options')
            del var['i']
            try:
                variant = ProductVariants.objects.create(**var)
                variant.options.set(options)
                variant.full_clean()
            except:
                pass

        return redirect('products_detail', pk=self.get_object().pk)


# class products detail view
class ProductsDetailView(DetailView):
    model = Products
    template_name = 'admin/product_view.html'

    def get_context_data(self, **kwargs):
        context = super(ProductsDetailView, self).get_context_data(**kwargs)
        context['langs'] = Languages.objects.filter(
            active=True).order_by('-default')
        context['lang'] = Languages.objects.filter(default=True).first()
        
        variants = self.get_object().variants.all()
        rang = range(1, variants.count() + 1)

        context['variants'] = dict(pairs=zip(variants, rang))

        return context



# get category atributs
def get_ctg_atributs(request):
    id = request.GET.get('id')
    try:
        category = Category.objects.get(id=int(id))
    except:
        return JsonResponse({'error': 'Category id is invalid'})

    atributs = category.atributs.all()
    serializer = AtributSerializer(atributs, many=True, context={'request': request})

    return JsonResponse(serializer.data, safe=False)


# delete partner video
def delete_partner_image(request):
    pk = request.POST.get("obj_id")

    try:
        Partners.objects.get(id=pk).image.delete()
    except:
        pass

    return JsonResponse('success', safe=False)


# FIX: Search, application in frontend