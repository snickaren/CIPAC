from django.conf.urls import url, include
from hsnominal import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^search/$', views.search, name='search'),
    url(r'^om/$', views.about, name='about'),
    url(r'^(?P<card_catalog_sequence_number>[0-9]+)/$', views.browse, name='cardurl'),
]
