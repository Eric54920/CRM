from django import template

register = template.Library()
from django.conf import settings
import re


@register.inclusion_tag('rbac/menu.html')
def menu(request):
    url = request.path_info
    menu_list = request.session.get(settings.MENU_SESSION_KEY)

    for i in menu_list:  # [ { url title icon  class:'active' }   { url title icon   } ]
        print(i['url'].split('/')[1])
        if re.search(r'{}'.format(i['url'].split('/')[1]), url):
            i['class'] = 'active'

    return {'menu_list': menu_list}


from collections import OrderedDict


@register.inclusion_tag('rbac/menu2.html')
def menu2(request):
    menu_dict = request.session.get(settings.MENU_SESSION_KEY)
    order_dict = OrderedDict()

    for key in sorted(menu_dict, key=lambda x: menu_dict[x]['weight'], reverse=True):
        order_dict[key] = menu_dict[key]

    for i in order_dict.values():
        i['class'] = 'hidden'
        for child in i['children']:
            if child['id'] == request.current_menu_id:
                i['class'] = ''
                child['class'] = 'active'

    return {'menu_list': order_dict.values()}


@register.inclusion_tag('rbac/breadcrumb.html')
def breadcrumb(request):
    return {'request': request}


@register.filter()
def has_permission(request, name):
    if name in request.session.get(settings.PERMISSION_SESSION_KEY):
        return True


@register.simple_tag
def gen_role_url(request, rid):
    params = request.GET.copy()
    params['rid'] = rid
    return params.urlencode()
