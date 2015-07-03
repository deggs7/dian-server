from django.contrib import admin
from registration.models import Registration
from registration.models import Strategy
from registration.models import StrategyDup

# Register your models here.
admin.site.register(Registration)
admin.site.register(Strategy)
admin.site.register(StrategyDup)
