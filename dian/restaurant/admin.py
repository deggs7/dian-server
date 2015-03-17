from django.contrib import admin
from .models import Restaurant
from .models import TableType
from .models import Strategy

# Register your models here.
admin.site.register(Restaurant)
admin.site.register(TableType)
admin.site.register(Strategy)
