from django.conf.urls import url

from . import views

app_name = 'food_toolbox'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^featured/(?P<recipe_id>[0-9]+)/$', views.featured, name='featured'),
    url(r'^create/$', views.create_recipe, name='create'),
    url(r'^create/(?P<error_message>.+)/$', views.create_recipe, name='create'),
    url(r'^add_recipe/$', views.add_recipe, name='add_recipe'),
    url(r'^add_ingredient/$', views.add_ingredient, name='add_ingredient'),
    url(r'^search/$', views.search, name='search'),
]
