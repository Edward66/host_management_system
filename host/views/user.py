from django.shortcuts import render, redirect, HttpResponse

from host import models
from host.forms.user import UserModelForm, UpdateUserModelForm, ResetPwdUserModelForm
from rbac.service.urls import memory_reverse


def user_list(request):
    """
    用户列表
    :param request:
    :return:
    """

    user_queryset = models.UserInfo.objects.all()
    context = {
        'user_queryset': user_queryset
    }
    return render(request, 'user_list.html', context)


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
        url = memory_reverse(request, 'user_list')
        return redirect(url)

    return render(request, 'rbac/change.html', {'form': form})


def user_edit(request, pk):
    """
    编辑用户
    :param request:
    :return:
    """
    obj = models.UserInfo.objects.filter(id=pk).first()
    if not obj:
        return HttpResponse('用户不存在')

    if request.method == 'GET':
        form = UpdateUserModelForm(instance=obj)
        return render(request, 'rbac/change.html', {"form": form})

    form = UpdateUserModelForm(data=request.POST, instance=obj)
    if form.is_valid():
        form.save()
        url = memory_reverse(request, 'user_list')
        return redirect(url)
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
        return HttpResponse('用户不存在')

    if request.method == 'GET':
        form = ResetPwdUserModelForm()
        return render(request, 'rbac/change.html', {'form': form})

    form = ResetPwdUserModelForm(data=request.POST, instance=obj)
    if form.is_valid():
        form.save()
        url = memory_reverse(request, 'user_list')
        return redirect(url)

    return render(request, 'rbac/change.html', {'form': form})


def user_delete(request, pk):
    """
    删除用户
    :param request:
    :param pk:
    :return:
    """

    origin_url = memory_reverse(request, 'user_list')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': origin_url})
    models.UserInfo.objects.filter(id=pk).delete()
    return redirect(origin_url)
