"""host_management_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, re_path

from host.views import user

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/list', user.user_list, name='user_list'),
    path('user/add', user.user_add, name='user_add'),
    re_path(r'^user/edit/(?P<pk>\d+)/$', user.user_edit, name='user_edit'),
    re_path(r'^user/delete/(?P<pk>\d+)/$', user.user_delete, name='user_delete'),
    re_path(r'^user/reset/pwd/(?P<pk>\d+)/$', user.user_reset_pwd, name='user_reset_pwd'),
]
