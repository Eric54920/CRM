from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect, reverse
from app import models

class AuthMiddleWare(MiddlewareMixin):

    def process_request(self, request):
        # 白名单
        if request.path_info in [reverse('login'),reverse('register')]:
            return
        if request.path_info.startswith('/admin/'):
            return
        is_login = request.session.get('is_login')
        if not is_login:
            return redirect(reverse('login'))
        # 已经登录
        request.user_obj = models.UserProfile.objects.get(pk=request.session.get('pk'))
