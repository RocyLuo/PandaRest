from django.conf.urls import url
from ui import views

urlpatterns = [
    url(r'^projects/(?P<pk>[0-9]+)/$', views.project_detail),
    url(r'^$', views.index),
]