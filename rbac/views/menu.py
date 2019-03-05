from collections import OrderedDict

from django.shortcuts import HttpResponse, render, redirect
from django.forms import formset_factory

from rbac import models
from rbac.forms.menu import (
    MenuModelForm, SecondMenuModelForm, PermissionModelForm,
    MultiAddPermissionForm, MultiEditPermissionForm
)
from rbac.service.urls import memory_reverse
from rbac.service.routers import get_all_url_dict


def menu_list(request):
    """
    菜单和权限列表
    :param request:
    :return:
    """
    menus = models.Menu.objects.all()
    menu_id = request.GET.get('mid')  # 用户选择的一级菜单
    second_menu_id = request.GET.get('sid')  # 用户选择的二级菜单

    menus_exists = models.Menu.objects.filter(id=menu_id).exists()
    if not menus_exists:
        menu_id = None

    if menu_id:
        second_menus = models.Permission.objects.filter(menu_id=menu_id)
    else:
        second_menus = []

    if second_menu_id:
        permissions = models.Permission.objects.filter(pid__id=second_menu_id)
    else:
        permissions = []

    second_menus_exists = models.Permission.objects.filter(id=second_menu_id).exists()
    if not second_menus_exists:
        second_menu_id = None

    context = {
        'menus': menus,
        'menu_id': menu_id,
        'second_menus': second_menus,
        'second_menu_id': second_menu_id,
        'permissions': permissions,
    }
    return render(request, 'rbac/menu_list.html', context)


def menu_add(request):
    """
    添加一级菜单
    :param request:
    :return:
    """
    if request.method == 'GET':
        form = MenuModelForm()

        return render(request, 'rbac/change.html', {'form': form})

    form = MenuModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        url = memory_reverse(request, 'rbac:menu_list')
        return redirect(url)

    return render(request, 'rbac/change.html', {'form': form})


def menu_edit(request, pk):
    obj = models.Menu.objects.filter(id=pk).first()
    if not obj:
        return HttpResponse('菜单不存在')
    if request.method == 'GET':
        form = MenuModelForm(instance=obj)
        return render(request, 'rbac/change.html', {'form': form})

    form = MenuModelForm(data=request.POST, instance=obj)
    if form.is_valid():
        form.save()
        url = memory_reverse(request, 'rbac:menu_list')
        return redirect(url)

    return render(request, 'rbac/change.html', {'form': form})


def menu_delete(request, pk):
    """
    删除一级菜单
    :param request:
    :param pk:
    :return:
    """
    url = memory_reverse(request, 'rbac:menu_list')

    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': url})

    models.Menu.objects.filter(id=pk).delete()

    return redirect(url)


def second_menu_add(request, menu_id):
    """
    添加二级菜单
    :param request:
    :param menu_id: 已经选择的一级菜单ID（用于设置默认值）
    :return:
    """
    menu_obj = models.Menu.objects.filter(id=menu_id).first()

    if request.method == 'GET':
        form = SecondMenuModelForm(initial={'menu': menu_obj})
        return render(request, 'rbac/change.html', {'form': form})
    form = SecondMenuModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        url = memory_reverse(request, 'rbac:menu_list')
        return redirect(url)
    return render(request, 'rbac/change.html', {'form': form})


def second_menu_edit(request, pk):
    """
    编辑二级菜单
    :param request:
    :param menu_id:
    :return:
    """
    permission_obj = models.Permission.objects.filter(id=pk).first()

    if request.method == 'GET':
        form = SecondMenuModelForm(instance=permission_obj)
        return render(request, 'rbac/change.html', {'form': form})

    form = SecondMenuModelForm(data=request.POST, instance=permission_obj)
    if form.is_valid():
        form.save()
        url = memory_reverse(request, 'rbac:menu_list')
        return redirect(url)
    return render(request, 'rbac/change.html', {'form': form})


def second_menu_delete(request, pk):
    """
    删除二级菜单
    :param request:
    :param pk:
    :return:
    """
    url = memory_reverse(request, 'rbac:menu_list')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': url})

    models.Permission.objects.filter(id=pk).delete()

    return redirect(url)


def permission_add(request, second_menu_id):
    """
    添加权限
    :param request:
    :param second_menu_id:
    :return:
    """
    if request.method == 'GET':
        form = PermissionModelForm()
        return render(request, 'rbac/change.html', {'form': form})

    form = PermissionModelForm(data=request.POST)
    if form.is_valid():
        second_menu_obj = models.Permission.objects.filter(id=second_menu_id).first()
        if not second_menu_obj:
            return HttpResponse('二级菜单不存在，请重新选择!')
        # form.instance中包含用户提交的所有值
        form.instance.pid = second_menu_obj
        form.save()
        url = memory_reverse(request, 'rbac:menu_list')
        return redirect(url)
    return render(request, 'rbac/change.html', {'form': form})


def permission_edit(request, pk):
    """
    编辑权限
    :param request:
    :param pk: 要编辑的权限id
    :return:
    """
    permission_obj = models.Permission.objects.filter(id=pk).first()

    if request.method == 'GET':
        form = PermissionModelForm(instance=permission_obj)
        return render(request, 'rbac/change.html', {'form': form})

    form = PermissionModelForm(data=request.POST, instance=permission_obj)
    if form.is_valid():
        form.save()
        url = memory_reverse(request, 'rbac:menu_list')
        return redirect(url)
    return render(request, 'rbac/change.html', {'form': form})


def permission_delete(request, pk):
    """
    删除权限
    :param request:
    :param pk:
    :return:
    """
    url = memory_reverse(request, 'rbac:menu_list')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': url})

    models.Permission.objects.filter(id=pk).delete()
    return redirect(url)


def multi_permissions(request):
    """
    批量操作权限
    :param request:
    :return:
    """

    post_type = request.GET.get('type')

    generate_formset_class = formset_factory(MultiAddPermissionForm, extra=0)
    update_formset_class = formset_factory(MultiEditPermissionForm, extra=0)
    generate_formset = None
    update_formset = None

    if request.method == 'POST' and post_type == 'generate':
        # 批量添加
        formset = generate_formset_class(data=request.POST)
        if formset.is_valid():
            object_list = []
            post_row_list = formset.cleaned_data
            has_error = False
            for i in range(0, formset.total_form_count()):
                row_dict = post_row_list[i]
                try:
                    new_obj = models.Permission(**row_dict)
                    new_obj.validate_unique()
                    object_list.append(new_obj)
                except Exception as e:
                    formset.errors[i].update(e)
                    generate_formset = formset
                    has_error = True
            if not has_error:
                models.Permission.objects.bulk_create(object_list, batch_size=100)

        else:
            generate_formset = formset

    if request.method == 'POST' and post_type == 'update':
        # 批量更新
        formset = update_formset_class(data=request.POST)
        if formset.is_valid():
            post_row_list = formset.cleaned_data
            for i in range(0, formset.total_form_count()):
                row_dict = post_row_list[i]
                permission_id = row_dict.pop('id')
                try:
                    row_object = models.Permission.objects.filter(id=permission_id).first()
                    for k, v in row_dict.items():
                        setattr(row_object, k, v)
                    row_object.validate_unique()
                    row_object.save()
                except Exception as e:
                    formset.errors[i].update(e)
                    update_formset = formset
        else:
            update_formset = formset

    # 1.获取项目中所有的url

    """
         {
             'rbac:menu_list':{name:'rbac:role_list',url:'/rbac/role/list'},
             ......
         }
    """

    all_url_dict = get_all_url_dict()

    router_name_set = set(all_url_dict.keys())

    # 2.获取数据库中所有的url
    permissions = models.Permission.objects.all().values('id', 'title', 'name', 'url', 'menu_id', 'pid_id')
    permission_name_set = set()
    permission_dict = OrderedDict()
    for row in permissions:
        permission_dict[row['name']] = row
        permission_name_set.add(row['name'])

    """
        {
            'rbac:menu_list':{'id':1,'title':'角色列表',name:'rbac:role_list',url:'/rbac/role/list'},
            ......
        }
    """

    for name, value in permission_dict.items():
        router_row_dict = all_url_dict.get(name)  # {'name':'rbac:role_list','url':'/rbac/role/list'},
        if not router_row_dict:
            continue
        if value['url'] != router_row_dict['url']:
            value['url'] = '路由和数据库中不一致'

    # 3. 应该添加、删除、修改的权限有哪些？
    # 3.1 计算出应该增加的name

    if not generate_formset:  # 如果目标没有通过验证，就不会执行下面的代码，页面就会显示错误信息
        generate_name_list = router_name_set - permission_name_set
        generate_formset = generate_formset_class(
            initial=[row_dict for name, row_dict in all_url_dict.items() if name in generate_name_list])

    # 3.2 计算出应该删除的name

    delete_name_list = permission_name_set - router_name_set
    delete_row_list = [row_dict for name, row_dict in permission_dict.items() if name in delete_name_list]

    # 3.3 计算出应该更新的name

    if not update_formset:
        update_name_list = permission_name_set & router_name_set
        update_formset = update_formset_class(
            initial=[row_dict for name, row_dict in permission_dict.items() if name in update_name_list])

    context = {
        'generate_formset': generate_formset,
        'delete_row_list': delete_row_list,
        'update_formset': update_formset,
    }
    return render(request, 'rbac/multi_permissions.html', context)


def multi_permissions_delete(request, pk):
    """
    批量页面的权限删除
    :param request:
    :param pk:
    :return:
    """
    url = memory_reverse(request, 'rbac:multi_permissions')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': url})
    models.Permission.objects.filter(id=pk).delete()
    return redirect(url)


def distribute_permissions(request):
    """
    权限分配
    :param request:
    :return:
    """

    user_id = request.GET.get('uid')
    user_object = models.UserInfo.objects.filter(id=user_id).first()

    if not user_object:
        user_id = None

    role_id = request.GET.get('rid')
    role_object = models.Role.objects.filter(id=role_id).first()

    if not role_object:
        role_id = None

    if request.method == 'POST' and request.POST.get('type') == 'role':
        role_id_list = request.POST.getlist('roles')
        # 用户和角色的关系添加到第三张表（关系表）
        if not user_object:
            return HttpResponse('请选择用户，然后再分配角色！')  # 一般人不会进行到这一步操作，技术人员会
        user_object.roles.set(role_id_list)

    if request.method == 'POST' and request.POST.get('type') == 'permission':
        permission_id_list = request.POST.getlist('permissions')
        if not role_object:
            return HttpResponse('请选择角色然后再分配权限！')
        role_object.permissions.set(permission_id_list)

    # 获取当前用户拥有的所有角色
    if user_id:
        user_has_roles = user_object.roles.all()
    else:
        user_has_roles = []
    user_has_roles_dict = {item.id: None for item in user_has_roles}  # 字典查找速度更快
    """
        {
            1:None,
            2:None,
            3:None
        }
    """
    # 获取当前用户拥有的所有权限

    # 如果选中了角色，优先显示选中角色所拥有的权限
    # 如果没有选角色，才显示用户所拥有的权限
    if role_object:  # 选择了角色
        user_has_permissions = role_object.permissions.all()
        user_has_permissions_dict = {item.id: None for item in user_has_permissions}
    elif user_object:  # 未选择角色，但选择了用户
        user_has_permissions = user_object.roles.filter(permissions__id__isnull=False).values('id',
                                                                                              'permissions').distinct()
        user_has_permissions_dict = {item['permissions']: None for item in user_has_permissions}
    else:
        user_has_permissions_dict = {}

    user_list = models.UserInfo.objects.all()
    all_role_list = models.Role.objects.all()

    # 所有的一级菜单
    all_menu_list = models.Menu.objects.all().values('id', 'title')
    """
    [
        {id:1, title:菜单1，children:[{id:1, title:x1, menu_id:1,children:[{id:11,title:11,pid:1},]]} ,{id:2, title:x2, menu_id:1,children:[]}},]}
        {id:2, title:菜单2，children:[{id:3, title:x3, menu_id:2,children:[]} ,{id:4, title:x2, menu_id:1},children:[]},]}
    ]
    """
    all_menu_dict = {}
    """
        {
            1:{id:1,title:菜单1,children:[{id:1,title:x1,menu_id:1:children[{id:11,title:11,pid:1},],},{id:2, title:x2, menu_id:1,chidlren:[]}]},
            1:{id:2,title:菜单2,children:[{id:3,title:x3,menu_id:2,:children:[]},{id:4, title:x4, menu_id:2}:children:[]]},
            ......
        }
    """
    for item in all_menu_list:
        item['children'] = []  # 用于放二级菜单
        all_menu_dict[item['id']] = item

    # 所有的二级菜单
    all_second_menu_list = models.Permission.objects.filter(menu__isnull=False).values('id', 'title', 'menu_id')

    """
    [
        {id:1, title:x1, menu_id:1,children:[]},
        {id:2, title:x2, menu_id:1,children:[]} ,
        {id:3, title:x3, menu_id:2,children:[]},
        {id:4, title:x4, menu_id:2,children:[]},
    ]
    """
    all_second_menu_dict = {}
    """
     {
         1: {id:1, title:x1, menu_id:1,children:[{id:11,title:11,pid:1},]},
         2: {id:2, title:x2, menu_id:1,children:[]} ,
         3: {id:3, title:x3, menu_id:2,children:[]},
         4: {id:4, title:x4, menu_id:2,children:[]},
     }
     """

    for row in all_second_menu_list:
        row['children'] = []  # 用于放三级菜单（具体权限）
        all_second_menu_dict[row['id']] = row
        menu_id = row['menu_id']
        all_menu_dict[menu_id]['children'].append(row)

    # 所有的三级菜单（不能做菜单的权限）
    all_permission_list = models.Permission.objects.filter(menu__isnull=True).values('id', 'title', 'pid_id')
    """
    [
        {id:11, title:x2,pid:1}, 
        {id:12, title:x2,pid:1}
        {id:13, title:x2,pid:2}
    ]
    """

    for row in all_permission_list:
        pid = row['pid_id']
        if not pid:  # 表示数据不合法，也就是菜单和父权限都没有，那就不处理了
            continue
        all_second_menu_dict[pid]['children'].append(row)
    """
    [
        {
            id:1,
            title:'业务管理',
            children:[
                {
                    'id':1,
                    title:'账单列表',
                    children:[
                        {'id':12, 'title':'添加账单'}
                    ]
                },
                {'id':11, 'title':'客户列表'},
            ]
        },
    ]
    """

    context = {
        'user_list': user_list,
        'role_list': all_role_list,
        'all_menu_list': all_menu_list,
        'user_id': user_id,
        'user_has_roles_dict': user_has_roles_dict,
        'user_has_permissions_dict': user_has_permissions_dict,
        'role_id': role_id,
    }

    return render(request, 'rbac/distribute_permissions.html', context=context)
