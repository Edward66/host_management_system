from django.http import QueryDict

from django.shortcuts import reverse


def memory_url(request, name, *args, **kwargs):
    """
    生成带有原搜索条件的URL（替代了模板中的url）
    :param request:
    :param name:
    :return:
    """
    basci_url = reverse(name, args=args, kwargs=kwargs)
    # 当前url中无参数
    if not request.GET:
        return basci_url

    query_dict = QueryDict(mutable=True)
    query_dict['_filter'] = request.GET.urlencode()  # mid=xxx&age=yyy

    return "%s?%s" % (basci_url, query_dict.urlencode())  # _filter="mid=xxx&age=yyy" 自动转义


def memory_reverse(request, name, *args, **kwargs):
    """
    反向生成URL
        http://127.0.0.1:8000/rbac/menu/edit/1/?_filter=mid%3D4
        1. 在URL将原来的搜索条件获取，如filter后的值
        2. reverse生成原来的URL，如：/menu/list/
        3. /menu/list/?mid%3D4
    :param request:
    :param name:
    :param args:
    :param kwargs:
    :return:
    """
    url = reverse(name, args=args, kwargs=kwargs)
    origin_params = request.GET.get('_filter')
    if origin_params:
        url = "%s?%s" % (url, origin_params)

    return url
