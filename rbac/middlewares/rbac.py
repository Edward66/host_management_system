import re
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse
from django.conf import settings


class RbacMiddleware(MiddlewareMixin):
    """
    用户权限信息校验
    """

    def process_request(self, request):
        """
        当前用户请求刚进入时候触发执行
        :param request:
        :return:
        """
        white_list = settings.WHITE_LIST
        current_url = request.path_info
        for valid_url in white_list:
            if re.match(valid_url, current_url):
                # 白名单的url不用进行权限验证
                return None
        permission_dict = request.session.get(settings.PERMISSION_SESSION_KEY)
        if not permission_dict:
            return HttpResponse('未获取用户权限，请登录！')

        url_record = [
            {'title': '首页', 'url': '#'}
        ]

        # 此处代码进行判断：/logout/,/index/  无需权限校验，但是需要登录才能访问
        for url in settings.NO_PERMISSION_LIST:
            if re.match(url, request.path_info):
                # 需要登录，但无需权限校验
                request.current_selected_permission = 0
                request.breadcrumb = url_record
                return None

        flag = False

        for item in permission_dict.values():
            reg = "^%s$" % item['url']
            if re.match(reg, current_url):
                flag = True
                request.current_selected_permission = item['pid'] or item['id']
                if not item['pid']:
                    url_record.extend([
                        {'title': item['title'], 'url': item['url'], 'class': 'active'}
                    ])
                else:
                    url_record.extend([
                        {'title': item['p_title'], 'url': item['p_url']},
                        {'title': item['title'], 'url': item['url'], 'class': 'active'},
                    ])
                request.breadcrumb = url_record
                break

        if not flag:
            return HttpResponse('无权访问')
