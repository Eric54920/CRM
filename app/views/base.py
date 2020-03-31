from django.shortcuts import HttpResponse
from django.views import View
from django.db.models import Q


class ShowList(View):

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        func = getattr(self, action)
        if not func:
            return HttpResponse('没有的此方法')
        ret = func()  # 可以有返回值 必须是HttpResponse
        if ret:
            return ret
        # return redirect(request.path_info)
        return self.get(request, *args, **kwargs)

    def query(self, field_names):
        query = self.request.GET.get('query', '')
        # query_field = request.GET.get('query_field','')
        # if query_field:
        #     all_customer = all_customer.filter(Q(('{}__contains'.format(query_field),query)))     #   Q(qq__contains=query)  Q(('qq__contains',query))

        # all_customer = all_customer.filter(Q(Q(qq__contains=query) | Q(name__contains=query) | Q(phone__contains=query)))

        q = Q()
        q.connector = 'OR'
        if not query:
            return q

        for field in field_names:
            q.children.append(Q(('{}__contains'.format(field), query)))

        return q