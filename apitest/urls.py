from django.conf.urls import url
from apitest import views

urlpatterns = [



    # url(r'^projects/$', views.project_list),
    # url(r'^projects/(?P<pk>[0-9]+)/$', views.project_detail),
    # url(r'^projects/(?P<pk>[0-9]+)/modules/$', views.project_module_list),
    #
    # url(r'^modules/$', views.module_post),
    # url(r'^modules/(?P<module_pk>[0-9]+)/$', views.module_detail),
    # url(r'^modules/(?P<module_pk>[0-9]+)/cases/$', views.module_case_list),
    #
    # url(r'^cases/$', views.case_post),
    # url(r'^cases/(?P<case_pk>[0-9]+)/$', views.case_detail),

    url(r'^test/(?P<pk>[0-9]+)$', views.test),

    url(r'^(?P<scope>[a-z]+)/(?P<scope_id>[0-9]+)/variables$', views.var_list),
    url(r'^(?P<scope>[a-z]+)/(?P<scope_id>[0-9]+)/variables/(?P<var_id>[0-9]+)$', views.var_detail),

    url(r'^(?P<scope>[a-z]+)/(?P<scope_id>[0-9]+)/requests$', views.request_list),
    url(r'^(?P<scope>[a-z]+)/(?P<scope_id>[0-9]+)/requests/(?P<request_id>[0-9]+)$', views.request_detail),

    url(r'^(?P<scope>[a-z]+)$', views.catalog_list),
    url(r'^(?P<scope>[a-z]+)/(?P<pk>[0-9]+)$', views.catalog_detail),
    url(r'^(?P<scope>[a-z]+)/(?P<pk>[0-9]+)/(?P<subscope>[a-z]+)$', views.catalog_subctalog),
]