from django.shortcuts import HttpResponse, render, redirect

from host.forms.host import HostModelForm
from host import models
from rbac.service.urls import memory_reverse


def host_list(request):
    host_queryset = models.Host.objects.all()
    context = {
        'host_queryset': host_queryset
    }
    return render(request, 'host_list.html', context)


def host_add(request):
    if request.method == 'GET':
        form = HostModelForm()
        return render(request, 'rbac/change.html', {'form': form})

    form = HostModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        url = memory_reverse(request, 'host_list')
        return redirect(url)
    return render(request, 'rbac/change.html', {'form': form})


def host_edit(request, pk):
    obj = models.Host.objects.filter(id=pk).first()
    if not obj:
        return HttpResponse('主机不存在')

    if request.method == 'GET':
        form = HostModelForm(instance=obj)
        return render(request, 'rbac/change.html', {'form': form})

    form = HostModelForm(data=request.POST, instance=obj)
    if form.is_valid():
        form.save()
        url = memory_reverse(request, 'host_list')
        return redirect(url)

    return render(request, 'rbac/change.html', {'form': form})


def host_delete(request, pk):
    original_url = memory_reverse(request, 'host_list')

    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': original_url})

    models.Host.objects.filter(id=pk).delete()

    return redirect(original_url)
