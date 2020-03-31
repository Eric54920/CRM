from django.shortcuts import render, HttpResponse, redirect, reverse
from app import models
import hashlib
from app.forms import RegForm, CustomerForm, ConsultRecordForm, EnrollmentForm
from django.db import transaction
from .base import ShowList
from rbac.service.permission_init import permission_init


# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        md5 = hashlib.md5()
        md5.update(password.encode('utf-8'))
        password = md5.hexdigest()
        user_obj = models.UserProfile.objects.filter(username=username, password=password, is_active=True).first()
        if user_obj:
            request.session['pk'] = user_obj.pk
            # request.session['is_login'] = True
            permission_init(request, user_obj)
            return redirect(reverse('customer'))
        return render(request, 'login.html', {'error': '用户名或密码错误'})

    return render(request, 'login.html')


def register(request):
    form_obj = RegForm()
    if request.method == 'POST':
        form_obj = RegForm(request.POST)
        if form_obj.is_valid():
            # 插入数据库
            # print(form_obj.cleaned_data)
            # models.UserProfile.objects.create(**form_obj.cleaned_data)
            form_obj.save()
            return redirect(reverse('login'))

    return render(request, 'register.html', {'form_obj': form_obj})


def customer(request):
    if request.path_info == reverse('customer'):
        all_customer = models.Customer.objects.filter(consultant__isnull=True)
    else:
        all_customer = models.Customer.objects.filter(consultant=request.user_obj)

    return render(request, 'consultant/customer.html', {'all_customer': all_customer})


from django.views import View
from django.db.models import Q


class Customer(ShowList):

    def get(self, request, *args, **kwargs):
        if request.path_info == reverse('customer'):
            all_customer = models.Customer.objects.filter(consultant__isnull=True)
        else:
            all_customer = models.Customer.objects.filter(consultant=request.user_obj)
        q = self.query(['name', 'phone', 'qq'])
        all_customer = all_customer.filter(q)
        page_obj = Pagination(request.GET.get('page', 1), all_customer.count(), request.GET.copy(), 2)

        return render(request, 'consultant/customer.html',
                      {
                          'all_customer': all_customer[page_obj.start:page_obj.end],
                          'page_html': page_obj.page_html,
                          'url': reverse('customer')
                      })

    def multi_apply(self):
        # 公户转私户
        # 获取客户的id
        pk_list = self.request.POST.getlist('pk')
        from tf_crm import settings
        from django.conf import settings

        if self.request.user_obj.customers.all().count() + len(pk_list) > settings.MAX_CUSTOMER_NUM:
            return HttpResponse('做人留一线 事后好相见')
        try:
            with transaction.atomic():

                queryset = models.Customer.objects.filter(pk__in=pk_list, consultant=None).select_for_update()  # 加行级锁
                if len(pk_list) == queryset.count():
                    queryset.update(consultant=self.request.user_obj)
                else:
                    return HttpResponse('你的手速太慢了，需要再练练,你的客户已被别人抢走，请刷新页面')
        except Exception:
            pass

        # self.request.user_obj.customers.add(*models.Customer.objects.filter(pk__in=pk_list))

    def multi_pub(self):
        # 私户转公户
        # 获取客户的id
        pk_list = self.request.POST.getlist('pk')
        # models.Customer.objects.filter(pk__in=pk_list).update(consultant=None)

        self.request.user_obj.customers.remove(*models.Customer.objects.filter(pk__in=pk_list))


users = [{'name': 'alex-{}'.format(i), 'pwd': 'alexdsb{}'.format(i)} for i in range(1, 355)]

from utils.pagination import Pagination


def customer_add(request):
    form_obj = CustomerForm()
    if request.method == 'POST':
        form_obj = CustomerForm(request.POST)
        if form_obj.is_valid():
            form_obj.save()  # 新增
            return redirect(reverse('customer'))

    return render(request, 'consultant/customer_add.html', {'form_obj': form_obj})


def customer_edit(request, pk):
    obj = models.Customer.objects.filter(pk=pk).first()
    form_obj = CustomerForm(instance=obj)  # 包含原始数据
    if request.method == 'POST':
        form_obj = CustomerForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()  # 修改
            return redirect(reverse('customer'))

    return render(request, 'consultant/customer_edit.html', {'form_obj': form_obj})


def customer_change(request, pk=None):
    obj = models.Customer.objects.filter(pk=pk).first()
    form_obj = CustomerForm(instance=obj)  # 包含原始数据
    if request.method == 'POST':
        form_obj = CustomerForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            path = request.GET.get('path')
            if not path:
                path = reverse('customer')
            return redirect(path)
    title = '编辑客户' if pk else '新增客户'
    return render(request, 'consultant/customer_change.html', {'form_obj': form_obj, 'title': title})


class ConsultRecordList(ShowList):

    def get(self, request, customer_id=None, *args, **kwargs):
        q = self.query([])

        if customer_id:
            all_consult_records = models.ConsultRecord.objects.filter(q, customer_id=customer_id,
                                                                      consultant=request.user_obj, delete_status=False)
        else:
            all_consult_records = models.ConsultRecord.objects.filter(q, consultant=request.user_obj,
                                                                      delete_status=False)

        page_obj = Pagination(request.GET.get('page', 1), all_consult_records.count(), request.GET.copy(), 2)

        return render(request, 'consultant/consult_record.html',
                      {
                          'all_consult_records': all_consult_records.order_by('-date')[page_obj.start:page_obj.end],
                          'page_html': page_obj.page_html,
                      })


def consult_record_change(request, pk=None):
    obj = models.ConsultRecord.objects.filter(pk=pk).first()
    form_obj = ConsultRecordForm(request, instance=obj)  # 包含原始数据
    if request.method == 'POST':
        form_obj = ConsultRecordForm(request, data=request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            path = request.GET.get('path')
            return redirect(path)
    title = '编辑跟进记录' if pk else '新增跟进记录'
    return render(request, 'form.html', {'form_obj': form_obj, 'title': title})


class EnrollmentList(ShowList):

    def get(self, request, customer_id=None, *args, **kwargs):
        q = self.query([])

        if customer_id:
            all_enrollments = models.Enrollment.objects.filter(q, customer_id=customer_id)
        else:
            all_enrollments = models.Enrollment.objects.filter(q)

        page_obj = Pagination(request.GET.get('page', 1), all_enrollments.count(), request.GET.copy(), 2)

        return render(request, 'consultant/enrollment_list.html',
                      {
                          'all_enrollments': all_enrollments.order_by('-enrolled_date')[page_obj.start:page_obj.end],
                          'page_html': page_obj.page_html,
                      })


def enrollment_change(request, customer_id=None, pk=None):
    obj = models.Enrollment.objects.filter(pk=pk).first()
    customer_id = customer_id if customer_id else obj.customer_id
    form_obj = EnrollmentForm(customer_id, instance=obj)
    if request.method == 'POST':
        form_obj = EnrollmentForm(customer_id, data=request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()

            path = request.GET.get('path')
            return redirect(path)

    title = '编辑报名记录' if pk else '新增报名记录'
    return render(request, 'form.html', {'form_obj': form_obj, 'title': title})


def enrollment_change(request, customer_id=None, pk=None):
    obj = models.Enrollment(customer_id=customer_id) if customer_id else models.Enrollment.objects.filter(pk=pk).first()
    form_obj = EnrollmentForm(request, instance=obj)
    if request.method == 'POST':
        form_obj = EnrollmentForm(request, data=request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()

            path = request.GET.get('path')
            return redirect(path)

    title = '编辑报名记录' if pk else '新增报名记录'
    return render(request, 'form.html', {'form_obj': form_obj, 'title': title})
