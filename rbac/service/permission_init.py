from django.conf import settings


def permission_init(request, user_obj):
    # 用户名和密码校验成功
    # 获取权限的信息  保存到session中
    # ret = user_obj.roles.exclude(permissions__url=None).values('permissions__url').distinct()
    permissions = user_obj.roles.filter(permissions__url__isnull=False).values(
        'permissions__url',
        'permissions__title',
        'permissions__menu__title',
        'permissions__menu__icon',
        'permissions__menu__weight',
        'permissions__menu_id',
        'permissions__id',
        'permissions__name',
        'permissions__parent__name',
        'permissions__parent_id',
    ).distinct()

    # 权限字典
    permission_dict = {}

    # 菜单字典
    menu_dict = {}

    for i in permissions:

        permission_dict[i['permissions__name']] = {
            'url': i['permissions__url'],
            'title': i['permissions__title'],
            'id': i['permissions__id'],
            'pid': i['permissions__parent_id'],
            'pname': i['permissions__parent__name'],
        }
        menu_id = i.get('permissions__menu_id')

        if not menu_id:
            continue

        menu_dict.setdefault(menu_id, {
            'title': i['permissions__menu__title'],
            'icon': i['permissions__menu__icon'],
            'weight': i['permissions__menu__weight'],
            'children': []
        })
        menu_dict[menu_id]['children'].append({
            "title": i['permissions__title'],
            "url": i['permissions__url'],
            "id": i['permissions__id'],
        })

    request.session['is_login'] = True
    request.session[settings.PERMISSION_SESSION_KEY] = permission_dict
    request.session[settings.MENU_SESSION_KEY] = menu_dict
