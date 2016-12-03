from django.conf.urls import url
from apitest import views

urlpatterns = [
    url(r'^projects/$', views.project_list),
    url(r'^projects/(?P<pk>[0-9]+)/$', views.project_detail),
    url(r'^projects/(?P<pk>[0-9]+)/modules/$', views.project_module_list),

    url(r'^modules/$', views.module_post),
    url(r'^modules/(?P<module_pk>[0-9]+)/$', views.module_detail),
    url(r'^modules/(?P<module_pk>[0-9]+)/cases/$', views.module_case_list),

    url(r'^cases/$', views.case_post),
    url(r'^cases/(?P<case_pk>[0-9]+)/$', views.case_detail),

    url(r'^test/(?P<pk>[0-9]+)/$', views.test),
]