from django.shortcuts import render, redirect, reverse

from host import models
from rbac.service.init_permission import init_permission


def login(request):
    """
    登录
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'login.html')
    user = request.POST.get('username')
    pwd = request.POST.get('password')

    user_obj = models.UserInfo.objects.filter(name=user, password=pwd).first()

    if not user_obj:
        return render(request, 'login.html', {'error': '用户名或密码错误'})

    # 用户权限信息的初始化
    init_permission(user_obj, request)

    return redirect(reverse('index'))


def logout(request):
    """
    注销
    :param request:
    :return:
    """
    request.session.delete()
    return redirect(reverse('logout'))


def index(request):
    """
    首页
    :param request:
    :return:
    """
    return render(request, 'index.html')
