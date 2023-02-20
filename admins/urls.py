from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required, user_passes_test


urlpatterns = [
    path('', user_passes_test(lambda u: u.is_superuser,
         login_url='login_admin')(views.home), name='home'),
    path('articles', user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(
        views.ArticlesList.as_view()), name='articles_list'),
    path('articles/create', user_passes_test(lambda u: u.is_superuser,
         login_url='login_admin')(views.ArticleCreateView.as_view()), name='articles_create'),
    path('articles/<int:pk>/edit', user_passes_test(lambda u: u.is_superuser,
         login_url='login_admin')(views.ArticleUpdate.as_view()), name='articles_edit'),
    path('langs', user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(
        views.LangsList.as_view()), name='langs_list'),
    path('langs/create', user_passes_test(lambda u: u.is_superuser,
         login_url='login_admin')(views.LngCreateView.as_view()), name='create_lang'),
    path('langs/<int:pk>/edit', user_passes_test(lambda u: u.is_superuser,
         login_url='login_admin')(views.LangsUpdate.as_view()), name='lang_update'),
    path('langs/delete', user_passes_test(lambda u: u.is_superuser,
         login_url='login_admin')(views.delete_langs), name='lang_del'),
    path("site_infos", user_passes_test(lambda u: u.is_superuser,
         login_url='login_admin')(views.StaticUpdate.as_view()), name='static_info'),
    path('images/save', user_passes_test(lambda u: u.is_superuser,
         login_url='login_admin')(views.save_images), name='images_save'),
    path("images/delete", user_passes_test(lambda u: u.is_superuser,
         login_url='login_admin')(views.delete_image), name='del-img'),
    path('translations', user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(
        views.TranslationList.as_view()), name='translation_list'),
    path("translations/<int:pk>", user_passes_test(lambda u: u.is_superuser, login_url='login_admin')
         (views.TranslationGroupDetail.as_view()), name='transl_group_detail'),
    path('translation/edit', user_passes_test(lambda u: u.is_superuser,
         login_url='login_admin')(views.translation_update), name='translation_edit'),
    path("translations/<int:pk>/edit", user_passes_test(lambda u: u.is_superuser,
         login_url='login_admin')(views.TranslationGroupUdpate.as_view()), name='transl_group_edit'),
    path("translation_group/create", user_passes_test(lambda u: u.is_superuser,
         login_url='login_admin')(views.add_trans_group), name='transl_group_create'),
    path('article_categories', user_passes_test(lambda u: u.is_superuser,
         login_url='login_admin')(views.ArticleCtgList.as_view()), name='article_ctg_list'),
    path('article_categories/create', user_passes_test(lambda u: u.is_superuser,
         login_url='login_admin')(views.AddArticleCtg.as_view()), name='add_acticle_ctg'),
    path("article_categories/<int:pk>/edit", user_passes_test(lambda u: u.is_superuser,
         login_url='login_admin')(views.ArticleCtgEdit.as_view()), name='article_ctg_update'),
    path("delete", user_passes_test(lambda u: u.is_superuser,
         login_url='login_admin')(views.delete_item), name='delete'),
    path('delete_alot', user_passes_test(lambda u: u.is_superuser,
         login_url='login_admin')(views.delete_alot), name='del_alot'),
    path("lang_icon_delete", user_passes_test(lambda u: u.is_superuser,
         login_url='login_admin')(views.del_lang_icon), name='lang_icon_del'),
    path("add_static_image", user_passes_test(lambda u: u.is_superuser,
         login_url='login_admin')(views.add_static_image), name='add_static_logos'),
    path("delete_static_image", user_passes_test(lambda u: u.is_superuser,
         login_url='login_admin')(views.del_statics_image), name='del_static_image'),
    path('delete_article_ctg_images', user_passes_test(lambda u: u.is_superuser,
         login_url='login_admin')(views.delete_article_group_img), name='art_ctg_image_del'),
    path("about_us/video/delete", user_passes_test(lambda u: u.is_superuser,
         login_url='login_admin')(views.delete_about_video), name='del_about_video'),
    path('about_us/video/set', user_passes_test(lambda u: u.is_superuser,
         login_url='login_admin')(views.set_about_video), name='set_about_video'),
    path('login', LoginView.as_view(
        template_name='admin/sing-in.html',
        success_url='/admin/',
    ), name='login_admin'),
    path('logout', views.logout_view, name='logout_url'),
    path('admins', user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(
        views.AdminsList.as_view()), name='admin_list'),
    path("admins/create", user_passes_test(lambda u: u.is_superuser,
         login_url='login_admin')(views.AdminCreate.as_view()), name='admins_create'),
    path("admins/<int:pk>/edit", user_passes_test(lambda u: u.is_superuser,
         login_url='login_admin')(views.AdminUpdate.as_view()), name='admins_edit'),
    path("delete_article_image", user_passes_test(lambda u: u.is_superuser,
         login_url='login_admin')(views.delete_article_image), name='del_article_img'),
    path("reviews", user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.ReviewsList.as_view()), name='review_list'),
    path("reviews/create", user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.ReviewsCreate.as_view()), name='review_create'),
    path('reviews/<int:pk>/edit', user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.ReviewsUpdate.as_view()), name='review_edit'),
    path('delete_review_image', user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.delete_review_image), name='del_review_image'),
    path("partners", user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.PartnersList.as_view()), name='partners_list'),
    path("partners/create", user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.PartnersCreate.as_view()), name='partners_create'),
    path("partners/<int:pk>/edit", user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.PartnersEdit.as_view()), name='partners_edit'),
    path('quick_applications', user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.ShortApplicationList.as_view()), name='short_aplic_list'),
    path('quick_applications/<int:pk>/edit', user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.ShortApplicationUpdate.as_view()), name='short_aplic_edit'),
    path('categories', user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.CategoryList.as_view()), name='category_list'),
    path('categories/create', user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.CategoryCreate.as_view()), name='category_create'),
    path("categories/<int:pk>/edit", user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.CategoryEdit.as_view()), name='category_edit'),
    path('del_ctg_files', user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.del_category_file), name='del_ctg_file'),
    path('atributs', user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.AtributsList.as_view()), name='atr_list'),
    path("atributs/create", user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.AtributsCreate.as_view()), name='atr_create'),
    path("atributs/<int:pk>/edit", user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.AtributEdit.as_view()), name='atribut_edit'),
    path("atribut_options/edit", user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.AtributOptionEdit.as_view()), name='atr_options_edit'),
    path("atribut_options/get", user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.get_option), name='get_atr_option'),
    path('colors', user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.ColorsList.as_view()), name='color_list'),
    path("colors/create", user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.ColorsCreate.as_view()), name='color_create'),
    path("colors/<int:pk>/edit", user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.ColorEdit.as_view()), name='colors_edit'),
    path("products", user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.ProductsList.as_view()), name='products_list'),
    path('products/create', user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.ProductsCreate.as_view()), name='products_create'),
    path('products/<int:pk>', user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.ProductsDetailView.as_view()), name='products_detail'),
    path('products/<int:pk>/edit', user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.ProductEdit.as_view()), name='products_edit'),
    path("get_ctg_atributs", user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.get_ctg_atributs), name='get_ctg_atributs'),
    

    #path("fill_db_qwertyuiop", user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.fill_db_view))
]
