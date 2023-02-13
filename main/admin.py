from django.contrib import admin
from .models import Products, ProductVariants, Category, AtributOptions, Atributs, Colors
# Register your models here.


admin.site.register(Products)
admin.site.register(Category)
admin.site.register(ProductVariants)
admin.site.register(Atributs)
admin.site.register(AtributOptions)
admin.site.register(Colors)