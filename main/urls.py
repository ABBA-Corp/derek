from django.urls import path, include
from . import views


urlpatterns = [
    path('articles', views.ArticlesList.as_view()),
    path("articles/<slug:slug>", views.ArticlesDetail.as_view()),
    path("static_infos", views.StaticInfView.as_view()),
    path("translations", views.TranslationsView.as_view()),
    path('languages', views.LangsList.as_view()),
    path('partners', views.PartnersList.as_view()),
    path('reviews', views.ReviewList.as_view()),
    path('categories', views.CategoryList.as_view()),
    path("categories/<slug:slug>", views.CategoryDetailView.as_view()),
    path('products', views.ProductsList.as_view()),
    path('products/<slug:slug>', views.ProductVariantDetail.as_view()),
    path("top_produts", views.TopProductsView.as_view()),
    path("add_aplication", views.NewAppliction.as_view()),
    path("search", views.Search.as_view()),
    path("get_product_variant", views.ProductVariantGet.as_view()),
]