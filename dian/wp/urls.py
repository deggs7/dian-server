from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^(?P<restaurant_openid>\w+)/register/$', views.register),
]
