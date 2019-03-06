from django.contrib import admin
from django.urls import path, re_path, include

from host.views import user
from host.views import host
from host.views import account

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),

    re_path(r'^login/$', account.login, name='login'),
    re_path(r'^logout/$', account.logout, name='logout'),

    re_path(r'^index/$', account.index, name='index'),

    # 用户管理
    re_path(r'^user/list/$', user.user_list, name='user_list'),
    re_path(r'^user/add/$', user.user_add, name='user_add'),
    re_path(r'^user/edit/(?P<pk>\d+)/$', user.user_edit, name='user_edit'),
    re_path(r'^user/delete/(?P<pk>\d+)/$', user.user_delete, name='user_delete'),
    re_path(r'^user/reset/pwd/(?P<pk>\d+)/$', user.user_reset_pwd, name='user_reset_pwd'),

    # 主机管理
    re_path(r'^host/list/$', host.host_list, name='host_list'),
    re_path(r'^host/add/$', host.host_add, name='host_add'),
    re_path(r'^host/edit/(?P<pk>\d+)/$', host.host_edit, name='host_edit'),
    re_path(r'^host/delete/(?P<pk>\d+)/$', host.host_delete, name='host_delete'),

    # 权限组件
    re_path('^rbac/', include(('rbac.urls', 'rbac'))),

]
