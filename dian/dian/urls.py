from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dian.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls',\
        namespace='rest_framework')),
    url(r'^api-token-auth/',\
        'rest_framework.authtoken.views.obtain_auth_token'),

    url(r'^account/', include('account.urls')),

    url(r'^restaurant/', include('restaurant.urls')),
    url(r'^registration/', include('registration.urls')),

    url(r'^table/', include('table.urls')),
    url(r'^menu/', include('menu.urls')),
    url(r'^trade/', include('trade.urls')),

    url(r'^captcha/$', views.captcha),
    url(r'^reset-passwd/$', views.reset_passwd),

    url(r'^wp/', include('wp.urls')),

    # Swagger Documentation Generator for Django REST Framework
    # https://github.com/marcgibbons/django-rest-swagger
    url(r'^docs/', include('rest_framework_swagger.urls')),
)
