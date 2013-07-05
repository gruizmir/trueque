from django.contrib import admin
from products.models import Product, Category, ProductCategory,Comment

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(ProductCategory)
admin.site.register(Comment)
