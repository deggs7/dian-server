from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
import views


urlpatterns = [
    url(r'^regstration/$', views.RegstrationList.as_view()),
    url(r'^regstration/(?P<pk>[0-9]+)/$', views.RegstrationDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
