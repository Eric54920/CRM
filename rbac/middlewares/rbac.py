from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect, reverse, HttpResponse
from django.conf import settings
import re


class AuthMiddleWare(MiddlewareMixin):

    def process_request(self, request):
        url = request.path_info
        # 白名单
        for i in settings.WHITE_LIST:
            if re.match(i, url):
                return
        # 登录状态的校验
        is_login = request.session.get('is_login')
        if not is_login:
            return redirect(reverse('login'))

        request.current_menu_id = None
        request.breadcrumb_list = [{'title': '首页', 'url': '/index/'}]

        # 免认证的地址校验
        for i in settings.PASS_LIST:
            if re.match(i, url):
                return
        # 权限的校验
        permissions = request.session.get(settings.PERMISSION_SESSION_KEY)
        for i in permissions.values():
            if re.match(r'^{}$'.format(i['url']), url):
                id = i['id']
                pid = i['pid']
                if pid:
                    # 当前访问的是子权限   三级菜单   pid
                    request.current_menu_id = pid
                    pname = i['pname']
                    p_permission = permissions[pname]
                    request.breadcrumb_list.append({'title': p_permission['title'], 'url': p_permission['url']})
                    request.breadcrumb_list.append({'title': i['title'], 'url': i['url']})
                else:
                    # 当前访问的是父权限 二级菜单   id
                    request.current_menu_id = id
                    request.breadcrumb_list.append({'title': i['title'], 'url': i['url']})
                print(request.current_menu_id)
                return

        return HttpResponse('没有访问的权限，请联系管理员')
