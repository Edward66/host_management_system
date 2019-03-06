from django.shortcuts import render


def user_list(request):
    """
    用户列表
    :param request:
    :return:
    """

    if request.method == 'GET':
        return render(request, 'user_list.html')
