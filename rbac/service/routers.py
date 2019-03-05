import re
from collections import OrderedDict

from django.conf import settings
from django.utils.module_loading import import_string  # 根据字符串的形式，帮我们去导入模块
from django.urls import URLPattern, URLResolver  # 路由分发：URLResolver。不是路由分发：URLPattern


def check_url_exclude(url):
    """
    排除一些特定的url
    :param url:
    :return:
    """
    exclude_url = [
        '/admin.*',
        '/login/'
    ]
    for regex in settings.AUTO_DISCOVER_EXCLUDE:
        if re.match(regex, url):
            return True


def recursion_urls(pre_namespace, pre_url, urlpatterns, url_ordered_dict):
    """

    :param pre_namespace: namespace前缀（rbac:......），以后用于拼接name
    :param pre_url: url的前缀（rbac/......），以后用于拼接url
    :param urlpatterns: 路由关系列表
    :param url_ordered_dict: 用于保存递归中获取的所有路由
    :return:
    """
    for item in urlpatterns:
        if isinstance(item, URLPattern):  # 非路由分发，将路由添加到url_ordered_dict
            if not item.name:  # url中反向命名的name
                continue
            if pre_namespace:
                name = f"{pre_namespace}:{item.name}"
            else:
                name = item.name
            url = pre_url + item.pattern.regex.pattern  # /^rbac/^user/edit/(?P<pk>\d_+)/$
            url = url.replace('^', '').replace('$', '')  # /rbac/user/edit/(?P<pk>\d_+)/

            if check_url_exclude(url):
                continue
            url_ordered_dict[name] = {'name': name, 'url': url}

        elif isinstance(item, URLResolver):  # 路由分发，进行递归操作
            if pre_namespace:
                if item.namespace:
                    namespace = f"{pre_namespace}:{item.namespace}"
                else:
                    namespace = item.namespace
            else:
                if item.namespace:
                    namespace = item.namespace
                else:
                    namespace = None
            recursion_urls(namespace, pre_url + item.pattern.regex.pattern, item.url_patterns, url_ordered_dict)


def get_all_url_dict():
    """
    获取项目中所有的URL（必须有name别名）
    :return:
    """
    url_ordered_dict = OrderedDict()
    """
    {
        'rbac:menu_list':{name:'rbac:menu_list',url:'xxxxx/yyyy/menu/list'}
    }
    """

    md = import_string(settings.ROOT_URLCONF)  # from permision_learn import urls

    recursion_urls(None, '/', md.urlpatterns, url_ordered_dict)  # 递归的去获取所有的路由。根目录没有namespace，根路由用/

    return url_ordered_dict
