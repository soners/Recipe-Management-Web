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


    # api urls
    url(r'^api_recipe/(\d+)/$', api_recipe, name='api_recipe'),
    url(r'^api_recipes/(\d+)/$', api_recipes, name='api_recipes'),
    url(r'^api_login/$', api_login, name='api_login'),
    url(r'^api_signup/$', api_signup, name='api_signup'),
]
