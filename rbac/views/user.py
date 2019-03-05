"""
用户管理
"""
from django.shortcuts import render, redirect, reverse, HttpResponse

from rbac import models
from rbac.forms.user import UserModelForm, UpdateUserModelForm, ResetPwdUserModelForm


def user_list(request):
    """
    用户列表
    :param request:
    :return:
    """
    user_queryset = models.UserInfo.objects.all()
    return render(request, 'rbac/user_list.html', {'user_list': user_queryset})


def user_add(request):
    """
    添加用户
    :param request:
    :return:
    """
    if request.method == 'GET':
        form = UserModelForm()
        return render(request, 'rbac/change.html', {'form': form})
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('rbac:user_list'))
    return render(request, 'rbac/change.html', {'form': form})


def user_edit(request, pk):
    """
    编辑用户
    :param request:
    :param pk: 要修改的角色id
    :return:
    """
    obj = models.UserInfo.objects.filter(id=pk).first()

    if not obj:
        return HttpResponse('角色不存在')

    if request.method == 'GET':
        form = UpdateUserModelForm(instance=obj)
        # 添加和编辑都是一个模板
        return render(request, 'rbac/change.html', {'form': form})
    form = UpdateUserModelForm(instance=obj, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('rbac:user_list'))
    return render(request, 'rbac/change.html', {'form': form})


def user_reset_pwd(request, pk):
    """
    重置密码
    :param request:
    :param pk:
    :return:
    """

    obj = models.UserInfo.objects.filter(id=pk).first()

    if not obj:
        return HttpResponse('角色不存在')

    if request.method == 'GET':
        form = ResetPwdUserModelForm()
        # 添加和编辑都是一个模板
        return render(request, 'rbac/change.html', {'form': form})
    form = ResetPwdUserModelForm(instance=obj, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('rbac:user_list'))
    return render(request, 'rbac/change.html', {'form': form})


def user_delele(request, pk):
    """
    删除角色
    :param request:
    :param pk:
    :return:
    """

    # 传cancel是为了delete成为一个公共页面，大家都能使用。
    origin_url = reverse('rbac:user_list')

    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': origin_url})

    models.UserInfo.objects.filter(id=pk).delete()
    return redirect(origin_url)
