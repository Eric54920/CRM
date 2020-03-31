from django import template
from django.urls import reverse
from django.http.request import QueryDict

register = template.Library()


@register.simple_tag()
def reverse_url(request, name, *args, **kwargs):
    dic = QueryDict(mutable=True)
    dic['path'] = request.get_full_path()
    url = '{}?{}'.format(reverse(name, args=args, kwargs=kwargs), dic.urlencode())

    return url
