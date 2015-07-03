from django.contrib import admin

from trade.models import Cart
from trade.models import CartItem
from trade.models import Order
from trade.models import OrderItem

# Register your models here.
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
