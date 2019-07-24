"""crescendo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from crescendo.management.views import *
from crescendo.management.api import *

urlpatterns = [
    path('', main, name='main'),
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^signin/', signin, name='signin'),
    url(r'^signup/', signup, name='signup'),
    url(r'^recipes/', recipes, name='recipes'),
    url(r'^add_recipe/', add_recipe, name='add_recipe'),
    url(r'^process_recipe/', process_recipe, name='process_recipe'),
    url(r'^detail/(\d+)/$', detail, name='detail'),
    url(r'^delete/(\d+)/$', delete, name='delete'),
    url(r'^profile/$', profile, name='profile'),
    url(r'^save_threshold/$', save_threshold, name='save_threshold'),

    # api urls
    url(r'^api_recipe/(\d+)/$', api_recipe, name='api_recipe'),
    url(r'^api_recipes/(\d+)/$', api_recipes, name='api_recipes'),
    url(r'^api_login/$', api_login, name='api_login'),
    url(r'^api_signup/$', api_signup, name='api_signup'),
    url(r'^api_add_recipe/$', api_add_recipe, name='api_add_recipe'),
    url(r'^api_delete_recipe/(\d+)/$', api_delete_recipe, name='api_delete_recipe'),

    url(r'^api_add_details_recipe/(\d+)/$', api_add_details_recipe, name='api_add_details_recipe'),

    url(r'^api_get_threshold/(\d+)/$', api_get_threshold, name='api_get_threshold'),
    url(r'^api_save_threshold/(\d+)/$', api_save_threshold, name='api_save_threshold'),
    url(r'^api_search_recipe/$', api_search_recipe, name='api_search_recipe'),

]
