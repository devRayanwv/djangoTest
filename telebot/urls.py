from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^test/', views.run, name='run'),
    url(r'^telebot/', views.index, name='index'),
]