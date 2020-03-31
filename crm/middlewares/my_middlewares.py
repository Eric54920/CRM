from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect, reverse
from crm import  models

class AuthMiddle(MiddlewareMixin):
    def process_request(self, request):

        if request.path_info in [reverse('login'), reverse('regist')]:
            return
        elif request.path_info.startswith('/admin/'):
            return
        if not request.session.get('is_login'):
            return redirect(reverse('login'))
        request.user_obj = models.UserProfile.objects.get(pk=request.session.get('pk'))