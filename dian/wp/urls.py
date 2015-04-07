from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^register-qrcode/$', views.get_register_qrcode),
    url(r'^(?P<restaurant_openid>\w+)/register/$', views.register),
    url(r'^confirm-table-type/$', views.confirm_table_type),
]
