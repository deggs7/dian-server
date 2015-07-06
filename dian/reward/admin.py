from django.contrib import admin
from reward.models import Table
from table.models import TableType

# Register your models here.
admin.site.register(Table)
admin.site.register(TableType)