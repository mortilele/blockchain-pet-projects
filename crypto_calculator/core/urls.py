from django.conf.urls import url

from core import views

urlpatterns = [
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
]
