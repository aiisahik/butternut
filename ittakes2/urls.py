"""ittakes2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

from ittakes2.matches.views import MatchCalculatorView

from tastypie.api import Api
from ittakes2.account.api import UserResource, ProfileResource
from ittakes2.matches.api import MatchResource



# from ittakes2.matches.views import GameView

v1_api = Api(api_name='v1')
v1_api.register(UserResource(),canonical=True)
v1_api.register(ProfileResource(),canonical=True)
v1_api.register(MatchResource(),canonical=True)


urlpatterns = [
    url(r'^api/', include(v1_api.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url('^', include('django.contrib.auth.urls')),
    url(r'^account/', include('ittakes2.account.urls')),
    # url(r'/', GameView.as_view()) ),
    url(r'^$', TemplateView.as_view(template_name="home.html") ),
    url(r'^calc/', MatchCalculatorView.as_view() ),
]
