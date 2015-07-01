from django.conf.urls import url
from django.conf.urls import patterns

#console api
urlpatterns = patterns(
    'wp.views',

    url(r'^register-qrcode/$', 'get_register_qrcode'),
    # url(r'^(?P<restaurant_openid>\w+)/register/$', 'unuse_register'),
    # url(r'^confirm-table-type/$', 'unuse_confirm_table_type'),

    # url(r'^register-qrcode/$', 'unuse_get_register_qrcode'),
    # url(r'^(?P<restaurant_openid>\w+)/register/$', 'unuse_register'),
    # url(r'^confirm-table-type/$', 'unuse_confirm_table_type'),

    # url(r'^get-member-info/$', 'get_member_info'),
    # url(r'^confirm-table-type/$', 'confirm_table_type'),
)

