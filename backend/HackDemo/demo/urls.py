__author__ = 'kuolin'
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^api/image', views.image, name='image'),
    url(r'^api/information', views.information, name='information'),
    url(r'^api/history', views.past_information, name='history')
]