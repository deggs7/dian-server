from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
import views


urlpatterns = [
    url(r'^registration/$', views.RegistrationList.as_view()),
    url(r'^registration/(?P<pk>[0-9]+)/$', views.update_registration),

    url(r'^msg-task/$', views.create_msg_task),
]

urlpatterns = format_suffix_patterns(urlpatterns)
