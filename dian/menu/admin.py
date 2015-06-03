from django.contrib import admin

from menu.models import Menu
from menu.models import Category
from menu.models import Product

# Register your models here.
admin.site.register(Menu)
admin.site.register(Category)
admin.site.register(Product)
