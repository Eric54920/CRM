import sys
from django.shortcuts import render, redirect, reverse, HttpResponse
from django.http import JsonResponse
from django.views import View
from crm import models
from crm import forms
import math
from util.pagination import Pagination
from django.db.models import Q
from django.db import transaction
import json
from django.utils.safestring import mark_safe
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.conf import settings
from django.forms import modelformset_factory, formset_factory


def user_tr(user_obj):
    tr = f"""<tr>
                <td>{ user_obj.username }</td>
                <td>{ user_obj.name }</td>
                <td>{ user_obj.department.name }</td>
                <td>{ user_obj.mobile }</td>
                <td>{ user_obj.memo }</td>
                <td>{ user_obj.date_joined }</td>
                <td><span class="green">{ user_obj.is_active }</span></td>
            </tr>
            """
    return tr

def cus_tr(cus_obj):
    tr = f"""<tr>
                <td>
                    <input type='checkbox' name='{cus_obj.pk}'>
                </td>
                <td>{cus_obj.name}</td>
                <td>{cus_obj.qq}</td>
                <td>{cus_obj.phone}</td>
                <td>{cus_obj.get_sex_display()}</td>
                <td>{cus_obj.birthday}</td>
                <td>{cus_obj.get_source_display()}</td>
                <td>{cus_obj.introduce_from}</td>
                <td>{cus_obj.get_course_display()}</td>
                <td>{cus_obj.get_class_type_display()}</td>
                <td>{cus_obj.show_status()}</td>
                <td>{cus_obj.last_consult_date}</td>
                <td>
                    <a class="btn btn-default btn-sm" href="one_customer/{cus_obj.pk}">查看</a>
                    <button class="btn btn-default btn-sm add" data-toggle="modal" data-target="#addCustomerModal" data="/add_enrollment/{cus_obj.pk}">报名</button>
                </td>
                <td>{cus_obj.consultant}</td>
                <td>{cus_obj.show_class()}</td>
                <td>
                    <button class='btn btn-primary btn-sm edit' data='/edit_custom/{cus_obj.pk}' 
                    data-toggle='modal' data-target='#addCustomerModal'><i class='fa fa-edit'></i></button>
                </td>
            </tr>"""
    return tr


def consult_tr(consult_obj):
    tr = f"""<tr>
                <td>
                    <input type="checkbox" name="{consult_obj.pk}">
                </td>
                <td>{ consult_obj.customer.name }</td>
                <td>{ consult_obj.get_status_display() }</td>
                <td>{ consult_obj.consultant.name }</td>
                <td>{ consult_obj.date }</td>
                <td>
                    <button class="btn btn-primary btn-sm edit" data="/edit_consult/{consult_obj.pk}" data-toggle="modal"
                        data-target="#addCustomerModal"><i class="fa fa-edit"></i></button>
                    <button class="btn btn-danger btn-sm delete"  data="/del_consult/{ consult_obj.pk }"><i class="fa fa-trash-o"></i></button>
                </td>
            </tr>"""
    return tr


def class_tr(cour_obj):
    tr = f"""<tr>
                <td>
                    <input type="checkbox" name="{cour_obj.pk}">
                </td>
                <td>{cour_obj}</td>
                <td>{cour_obj.price}</td>
                <td>{cour_obj.start_date}</td>
                <td>{cour_obj.graduate_date}</td>
                <td>{cour_obj.getTeacherList()}</td>
                <td>{cour_obj.get_class_type_display()}</td>
                <td>
                    <button class="btn btn-primary btn-sm edit" data="/edit_class/{cour_obj.pk}" data-toggle="modal"
                        data-target="#addCustomerModal"><i class="fa fa-edit"></i></button>
                    <a class="btn btn-info btn-sm" href="/courserecord/{ cour_obj.pk }">课程记录</a>
                </td>
            </tr>"""
    return tr


def enrollment_tr(enrollment_obj):
    tr = f"""
            <tr>
                <td>
                    <input type="checkbox" name="{enrollment_obj.pk}">
                </td>
                <td>{ enrollment_obj.customer.name }</td>
                <td>{ enrollment_obj.enrolment_class.campuses }</td>
                <td>{ enrollment_obj.enrolment_class }</td>
                <td>{ enrollment_obj.enrolled_date }</td>
                <td>{ enrollment_obj.delete_status }</td>
                <td>{ enrollment_obj.contract_agreed }</td>
                <td>{ enrollment_obj.contract_approved }</td>
                <td>
                    <button class="btn btn-primary btn-sm edit" data="/edit_enrollment/{enrollment_obj.pk}" data-toggle="modal"
                        data-target="#addCustomerModal"><i class="fa fa-edit"></i></button>
                    <button class="btn btn-danger btn-sm delete"  data="/del_enroll/{ enrollment_obj.pk }"><i class="fa fa-trash-o"></i></button>
                </td>
            </tr>
        """
    return tr


def paymentrecord_tr(paymentrecord_obj):
    tr = f"""
            <tr>
            <td>
                <input type="checkbox" name="{paymentrecord_obj.pk}">
            </td>
            <td>{ paymentrecord_obj.customer.name }</td>
            <td>{ paymentrecord_obj.get_course_display() }</td>
            <td>{ paymentrecord_obj.get_pay_type_display() }</td>
            <td>{ paymentrecord_obj.paid_fee }</td>
            <td>{ paymentrecord_obj.date }</td>
            <td>{ paymentrecord_obj.get_class_type_display() }</td>
            <td>{ paymentrecord_obj.enrolment_class }</td>
            <td>{ paymentrecord_obj.consultant.name }</td>
            <td>{ paymentrecord_obj.delete_status }</td>
            <td>{ paymentrecord_obj.get_status_display() }</td>
            <td>{ paymentrecord_obj.confirm_date }</td>
            <td>{ paymentrecord_obj.confirm_user }</td>
            <td>
                <button class="btn btn-primary btn-sm edit" data="/edit_paymentRecord/{paymentrecord_obj.pk}" data-toggle="modal"
                    data-target="#addCustomerModal"><i class="fa fa-edit"></i></button>
                <button class="btn btn-danger btn-sm delete" data="/del_payment/{ paymentrecord_obj.pk }"><i class="fa fa-trash-o"></i></button>
            </td>
        </tr>
        """
    return tr

def courserecord_tr(courserecord_obj):
    tr = f"""<tr>
                <td>
                    <input type="checkbox" name="{courserecord_obj.pk}">
                </td>
                <td>{ courserecord_obj }</td>
                <td>{ courserecord_obj.teacher }</td>
                <td>{ courserecord_obj.day_num }</td>
                <td>{ courserecord_obj.date }</td>
                <td>{ courserecord_obj.course_title }</td>
                <td>{ courserecord_obj.has_homework }</td>
                <td>{ courserecord_obj.homework_title }</td>
                <td>{ courserecord_obj.recorder }</td>
                <td>
                    <button class="btn btn-primary btn-sm edit" data="/edit_courserecord/{courserecord_obj.pk}" data-toggle="modal"
                        data-target="#addCustomerModal"><i class="fa fa-edit"></i></button>
                    <button class="btn btn-primary btn-sm edit" data="/study_list/{courserecord_obj.pk}">查看</button>
                </td>
            </tr>"""
    return tr

def studyrecord_tr(studyrecord_obj):
    tr = f"""
            <tr>
                <td>
                    <input type="checkbox" name="{studyrecord_obj.pk}">
                </td>
                <td>{ studyrecord_obj.get_attendance_display() }</td>
                <td>{ studyrecord_obj.student.name }</td>
                <td>{ studyrecord_obj.course_record.course_title }</td>
                <td>{ studyrecord_obj.score }</td>
                <td>{ studyrecord_obj.homework_note }</td>
                <td>{ studyrecord_obj.date }</td>
                <td>{ studyrecord_obj.note }</td>
                <td>
                    <button class="btn btn-primary btn-sm edit" data="/edit_studyrecord/{studyrecord_obj.pk}" data-toggle="modal"
                        data-target="#addCustomerModal"><i class="fa fa-edit"></i></button>
                    <button class="btn btn-danger btn-sm delete" data="/del_study/{ studyrecord_obj.pk }"><i class="fa fa-trash-o"></i></button>
                </td>
            </tr>
        """
    return tr

class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        name = request.POST.get('name')
        passwd = forms.md5(request.POST.get('passwd'))
        obj = models.UserProfile.objects.filter(username=name,
                                                password=passwd).first()
        if obj:
            request.session['is_login'] = True
            request.session['pk'] = obj.pk
            return redirect(reverse('customer'))
        return render(request, 'login.html', {'msg': '账号或密码错误！'})


class Regist(View):
    regform = forms.RegForm()

    def get(self, request):
        return render(request, 'regist.html', {'regform': self.regform})

    def post(self, request):
        regform = forms.RegForm(request.POST)
        if regform.is_valid():
            regform.save()
            return redirect(reverse('login'))
        return render(request, 'regist.html', {'regform': regform})


class Delete_obj(View):
    def get(self, request, obj, id):
        try:
            if obj == 'customer':
                models.Customer.objects.filter(pk=id).first().delete()
            elif obj == 'class':
                models.ClassList.objects.filter(pk=id).first().delete()
            elif obj == 'consult':
                models.ConsultRecord.objects.filter(pk=id).first().delete()
            elif obj == 'enroll':
                models.Enrollment.objects.filter(pk=id).first().delete()
            elif obj == 'payment':
                models.PaymentRecord.objects.filter(pk=id).first().delete()
            elif obj == 'course':
                models.CourseRecord.objects.filter(pk=id).first().delete()
            elif obj == 'study':
                models.StudyRecord.objects.filter(pk=id).first().delete()
        except Exception:
            return JsonResponse({'status': 400})
        else:
            print(1)
            return JsonResponse({'status': 200})

class BaseClass(View):
    def query(self, field_name, query):
        q = Q()
        q.connector = 'OR'
        if not query:
            return q
        for i in field_name:
            q.children.append(Q((f'{i}__icontains', query)))
        return q

    def retResult(self, lst, page, temp):
        if not len(lst):
            return JsonResponse({'status': 400, 'msg': '没有您想要的结果'})
        pag = Pagination(page, len(lst))
        pagination = pag.pagination()
        result = []
        for obj in lst[pag.start:pag.end]:
            tr_dom = getattr(sys.modules[__name__], temp)(obj)
            print('tr', tr_dom)
            result.append(tr_dom)
        return result, pagination

class Customer(BaseClass):
    def get(self, request):
        page = request.GET.get('page')
        if request.path_info == reverse('customer'):
            customers = models.Customer.objects.filter(consultant__isnull=True)
            pag = Pagination(page, len(customers))
            pagination = pag.pagination()
        elif request.path_info == reverse('my_customer'):
            customers = models.Customer.objects.filter(
                consultant=request.user_obj)
            pag = Pagination(page, len(customers))
            pagination = pag.pagination()

        return render(
            request, 'customer.html', {
                'customers': customers[pag.start:pag.end],
                'pagination': pagination,
                'path': request.path_info
            })

    def post(self, request):
        page = request.GET.get('page')
        curt_page = request.POST.get('curt_page')
        search_con = request.POST.get('search_con')
        q = self.query(['name', 'qq', 'phone', 'sex'], search_con)
        if curt_page == '/customer/':
            lst = models.Customer.objects.filter(Q(Q(consultant=None)) & q)
            result, pagination = self.retResult(lst, page, 'cus_tr')

        elif curt_page == '/my_customer/':
            lst = models.Customer.objects.filter(
                Q(Q(consultant=request.user_obj)) & q)
            result, pagination = self.retResult(lst, page, 'cus_tr')

        return JsonResponse({
            'status': 200,
            'tr': result,
            'pagination': pagination
        })


class AddCustomer(BaseClass):
    def get(self, request):
        form_add = forms.Customers()
        return JsonResponse({
            'status': 200,
            'form_add': form_add.as_p(),
        })

    def post(self, request):
        form_add = forms.Customers(request.POST)
        if form_add.is_valid():
            qq = form_add.save()
            cus_obj = models.Customer.objects.filter(qq=qq).first()
            tr = cus_tr(cus_obj)
            return JsonResponse({'status': 200, 'tr': mark_safe(tr)})
        return JsonResponse({
            'status': 400,
            'form_add': form_add.as_p(),
        })


class EditCustomer(BaseClass):
    def dispatch(self, request, *args, **kwargs):
        self.id = request.path_info.split('/')[-1]
        self.cus_obj = models.Customer.objects.filter(pk=self.id).first()
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(),
                              self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

    def get(self, request):
        obj = forms.Customers(instance=self.cus_obj)
        return JsonResponse({'status': 200, 'obj': obj.as_p()})

    def post(self, request):
        obj = forms.Customers(request.POST, instance=self.cus_obj)
        if obj.is_valid():
            obj.save()
            cus_obj = models.Customer.objects.filter(pk=self.id).first()
            tr = cus_tr(cus_obj)
            return JsonResponse({'status': 200, 'tr': mark_safe(tr)})
        return JsonResponse({'status': 400, 'form_add': obj.as_p()})


class CustomTransfer(BaseClass):
    def post(self, request):
        user_list = request.POST.getlist('user_list[]')
        action = int(request.POST.get('action'))
        if action == 1:
            if self.request.user_obj.customers.all().count() + len(user_list) > settings.MAX_CUSTOMER_NUM:
                return JsonResponse({'status': 400, 'msg': '您的客户数量已达上限'})
            try:
                with transaction.atomic():
                    obj = models.Customer.objects.filter(pk__in=user_list, consultant=None).select_for_update()
                    if obj.count() == len(user_list):
                        obj.update(consultant_id=request.session.get('pk'))
                    else:
                        return JsonResponse({'status': 400, 'msg': '您的客户已经被抢走了，请重新选择'})
            except Exception as e:
                return JsonResponse({'status': 400})
        elif action == 2:
            models.Customer.objects.filter(pk__in=user_list).update(
                consultant_id=None)
        return JsonResponse({'status': 200})


class UserList(BaseClass):
    def get(self, request, *args, **kwargs):
        page = request.GET.get('page')
        user_list = models.UserProfile.objects.all()
        pag = Pagination(page, len(user_list))
        pagination = pag.pagination()
        return render(request, 'user_list.html', {
            'users': user_list[pag.start: pag.end],
            'pagination': pagination
        })

    def post(self, request):
        page = request.GET.get('page')
        search_con = request.POST.get('search_con')
        q = self.query(['username', 'name', 'mobile'], search_con)
        lst = models.UserProfile.objects.filter(q)
        result, pagination = self.retResult(lst, page, 'user_tr')
        print(lst, len(lst))

        return JsonResponse({
            'status': 200,
            'tr': result,
            'pagination': pagination
        })


class Class(BaseClass):
    def get(self, request):
        page = request.GET.get('page')
        classes = models.ClassList.objects.all()
        pag = Pagination(page, len(classes))
        pagination = pag.pagination()
        return render(request, 'class.html', {'classes': classes[pag.start: pag.end], 'pagination': pagination})

    def post(self, request):
        page = request.GET.get('page')
        search_con = request.POST.get('search_con')
        q = self.query(['course', 'price'], search_con)
        lst = models.ClassList.objects.filter(q)
        result, pagination = self.retResult(lst, page, 'class_tr')

        return JsonResponse({
            'status': 200,
            'tr': result,
            'pagination': pagination
        })

class AddClass(View):
    def get(self, request):
        form_add = forms.Classes()
        return JsonResponse({'status': 200, 'form_add': form_add.as_p()})

    def post(self, request):
        form_add = forms.Classes(request.POST)
        if form_add.is_valid():
            name = form_add.save()
            course = request.POST.get('course')
            cour_obj = models.ClassList.objects.filter(course=course).first()
            tr = class_tr(cour_obj)
            return JsonResponse({'status': 200, 'tr': mark_safe(tr)})
        return JsonResponse({'status': 400, 'form_add': form_add.as_p()})


class EditClass(View):
    def dispatch(self, request, *args, **kwargs):
        self.id = request.path_info.split('/')[-1]
        self.cour_obj = models.ClassList.objects.filter(pk=self.id).first()
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(),
                              self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

    def get(self, request):
        obj = forms.Classes(instance=self.cour_obj)
        return JsonResponse({'status': 200, 'obj': obj.as_p()})

    def post(self, request):
        obj = forms.Classes(request.POST, instance=self.cour_obj)
        if obj.is_valid():
            obj.save()
            cus_obj = models.ClassList.objects.filter(pk=self.id).first()
            tr = class_tr(cus_obj)
            return JsonResponse({'status': 200, 'tr': mark_safe(tr)})
        return JsonResponse({'status': 400, 'form_add': obj.as_p()})


class ConsultRecord(BaseClass):
    def get(self, request, customer_id=None):
        page = request.GET.get('page')
        if not customer_id:
            consults = models.ConsultRecord.objects.filter(consultant=request.user_obj, delete_status=False)
        else:
            consults = models.ConsultRecord.objects.filter(customer_id=customer_id)
        pag = Pagination(page, len(consults))
        pagination = pag.pagination()
        return render(request, 'consultrecords.html', {'consults': consults[pag.start: pag.end], 'pagination':pagination})

    def post(self, request):
        page = request.GET.get('page')
        search_con = request.POST.get('search_con')
        q = self.query(['note'], search_con)
        lst = models.ConsultRecord.objects.filter(Q(consultant=request.user_obj) & q)
        result, pagination = self.retResult(lst, page, 'consult_tr')

        return JsonResponse({
            'status': 200,
            'tr': result,
            'pagination': pagination
        })

class AddConsultRecord(View):
    def get(self, request):
        form_add = forms.ConsultRecords(request)
        return JsonResponse({'status': 200, 'form_add': form_add.as_p()})


    def post(self, request):
        form_add = forms.ConsultRecords(request, request.POST)
        if form_add.is_valid():
            form_add.save()
            id = request.POST.get('customer')
            obj = models.ConsultRecord.objects.filter(customer_id=id).first()
            tr = consult_tr(obj)
            return JsonResponse({'status': 200, 'tr': mark_safe(tr)})
        return JsonResponse({'status': 400, 'form_add': form_add.as_p()})


class EditConsultRecord(View):
    def dispatch(self, request, *args, **kwargs):
        self.id = request.path_info.split('/')[-1]
        self.consult_obj = models.ConsultRecord.objects.filter(
            pk=self.id).first()
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(),
                              self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

    def get(self, request):
        obj = forms.ConsultRecords(request, instance=self.consult_obj)
        return JsonResponse({'status': 200, 'obj': obj.as_p()})

    def post(self, request):
        obj = forms.ConsultRecords(request.POST, instance=self.consult_obj)
        if obj.is_valid():
            obj.save()
            consult_obj = models.ConsultRecord.objects.filter(
                pk=self.id).first()
            tr = consult_tr(consult_obj)
            return JsonResponse({'status': 200, 'tr': mark_safe(tr)})
        return JsonResponse({'status': 400, 'form_add': obj.as_p()})


class Enrollments(BaseClass):
    def get(self, request):
        enrollments = models.Enrollment.objects.all()
        page = request.GET.get('page')
        pag = Pagination(page, len(enrollments))
        pagination = pag.pagination()
        return render(request, 'enrollments.html', {'enrollments': enrollments[pag.start: pag.end], 'pagination': pagination})

    def post(self, request):
        page = request.GET.get('page')
        search_con = request.POST.get('search_con')
        q = self.query(['note'], search_con)
        lst = models.Enrollment.objects.filter(Q(Q(consultant=None)) & q)
        result, pagination = self.retResult(lst, page, 'enrollment_tr')

        return JsonResponse({
            'status': 200,
            'tr': result,
            'pagination': pagination
        })

class AddEnrollments(View):
    def get(self, request, enrollment_id):
        if enrollment_id:
            form_add = forms.EnrollmentForm(enrollment_id)
            return JsonResponse({'status': 200, 'form_add': form_add.as_p()})

    def post(self, request, enrollment_id):
        form_add = forms.EnrollmentForm(enrollment_id, request.POST)
        if form_add.is_valid():
            form_add.save()
            # customer = request.POST.get('customer')
            # obj = models.Enrollment.objects.filter(customer_id=customer).first()
            # tr = enrollment_tr(obj)
            return JsonResponse({'status': 200})
        return JsonResponse({'status': 400, 'form_add': form_add.as_p()})


class EditEnrollments(View):
    def dispatch(self, request, *args, **kwargs):
        self.id = request.path_info.split('/')[-1]
        self.enrollment_obj = models.Enrollment.objects.filter(
            pk=self.id).first()
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(),
                              self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

    def get(self, request):
        obj = forms.EnrollmentForm(self.id, instance=self.enrollment_obj)
        return JsonResponse({'status': 200, 'obj': obj.as_p()})

    def post(self, request):
        obj = forms.EnrollmentForm(request.POST, instance=self.enrollment_obj)
        if obj.is_valid():
            obj.save()
            enrollment_obj = models.Enrollment.objects.filter(
                pk=self.id).first()
            tr = enrollment_tr(enrollment_obj)
            return JsonResponse({'status': 200, 'tr': mark_safe(tr)})
        return JsonResponse({'status': 400, 'form_add': obj.as_p()})


class PaymentRecords(BaseClass):
    def get(self, request):
        paymentRecords = models.PaymentRecord.objects.all()
        page = request.GET.get('page')
        pag = Pagination(page, len(paymentRecords))
        pagination = pag.pagination()
        return render(request, 'paymentrecord.html',{'paymentRecords': paymentRecords[pag.start: pag.end], 'pagination': pagination})

    def post(self, request):
        page = request.GET.get('page')
        search_con = request.POST.get('search_con')
        q = self.query(['note'], search_con)
        lst = models.PaymentRecord.objects.filter(Q(Q(consultant=None)) & q)
        result, pagination = self.retResult(lst, page, 'paymentrecord_tr')

        return JsonResponse({
            'status': 200,
            'tr': result,
            'pagination': pagination
        })

class AddPaymentRecords(View):
    def get(self, request):
        form_add = forms.PaymentRecordForm()
        return JsonResponse({'status': 200, 'form_add': form_add.as_p()})

    def post(self, request):
        form_add = forms.PaymentRecordForm(request.POST)
        if form_add.is_valid():
            form_add.save()
            customer = request.POST.get('customer')
            obj = models.PaymentRecord.objects.filter(
                customer_id=customer).order_by('date').reverse().first()
            tr = paymentrecord_tr(obj)
            return JsonResponse({'status': 200, 'tr': mark_safe(tr)})
        return JsonResponse({'status': 400, 'form_add': form_add.as_p()})

class EditPaymentRecords(View):
    def dispatch(self, request, *args, **kwargs):
        self.id = request.path_info.split('/')[-1]
        self.obj = models.PaymentRecord.objects.filter(pk=self.id).first()
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(),
                              self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

    def get(self, request):
        obj = forms.PaymentRecordForm(instance=self.obj)
        return JsonResponse({'status': 200, 'obj': obj.as_p()})

    def post(self, request):
        obj = forms.PaymentRecordForm(request.POST, instance=self.obj)
        if obj.is_valid():
            obj.save()
            paymentrecord_obj = models.PaymentRecord.objects.filter(
                pk=self.id).first()
            tr = paymentrecord_tr(paymentrecord_obj)
            return JsonResponse({'status': 200, 'tr': mark_safe(tr)})
        return JsonResponse({'status': 400, 'form_add': obj.as_p()})

class CourseRecord(BaseClass):
    def get(self, request):
        class_id = request.path_info.split('/')[-1]
        courserecords = models.CourseRecord.objects.filter(re_class_id=class_id)
        if len(courserecords):
            page = request.GET.get('page')
            pag = Pagination(page, len(courserecords))
            pagination = pag.pagination()
            return render(request, 'courserecords.html', {'courserecords': courserecords[pag.start: pag.end], 'pagination': pagination, 'class_id': class_id})
        return render(request, 'courserecords.html', {'msg': '没有任何课程记录', 'class_id': class_id})

    def post(self, request):
        page = request.GET.get('page')
        search_con = request.POST.get('search_con')
        q = self.query(['course_title', 'course_memo', 'homework_title', 'homework_memo', 'scoring_point'], search_con)
        lst = models.CourseRecord.objects.filter(q)
        result, pagination = self.retResult(lst, page, 'courserecord_tr')

        return JsonResponse({
            'status': 200,
            'tr': result,
            'pagination': pagination
        })

class AddCourseRecord(View):
    def get(self, request):
        class_id = request.path_info.split('/')[-1]
        form_add = forms.CourseRecordForm(request, class_id=class_id, course_id=None)
        return JsonResponse({'status': 200, 'form_add': form_add.as_p()})

    def post(self, request):
        class_id = request.POST.get('re_class')
        form_add = forms.CourseRecordForm(request, request.POST, class_id=class_id)
        if form_add.is_valid():
            form_add.save()
            re_class = request.POST.get('re_class')
            day_num = request.POST.get('day_num')
            obj = models.CourseRecord.objects.filter(re_class_id=re_class, day_num=day_num).first()
            tr = courserecord_tr(obj)
            return JsonResponse({'status': 200, 'tr': mark_safe(tr)})
        return JsonResponse({'status': 400, 'form_add': form_add.as_p()})

class EditCourseRecord(View):
    def dispatch(self, request, *args, **kwargs):
        self.course_id = request.path_info.split('/')[-1]
        self.obj = models.CourseRecord.objects.filter(pk=self.course_id).first()
        self.class_id = self.obj.re_class_id
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(),
                              self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

    def get(self, request):
        obj = forms.CourseRecordForm(request, class_id=self.class_id, instance=self.obj)
        return JsonResponse({'status': 200, 'obj': obj.as_p()})

    def post(self, request):
        obj = forms.CourseRecordForm(request, request.POST, class_id=self.class_id, instance=self.obj)
        if obj.is_valid():
            obj.save()
            courserecord_obj = models.CourseRecord.objects.filter(pk=self.course_id).first()
            tr = courserecord_tr(courserecord_obj)
            return JsonResponse({'status': 200, 'tr': mark_safe(tr)})
        return JsonResponse({'status': 400, 'form_add': obj.as_p()})

class StudyRecords(View):
    def dispatch(self, request, course_id, *args, **kwargs):
        self.course_id = course_id
        self.StudyRecordFormSet = modelformset_factory(models.StudyRecord, forms.StudyRecordForm, extra=0)
        self.formset = self.StudyRecordFormSet(queryset=models.StudyRecord.objects.filter(course_record_id=self.course_id))
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(),
                              self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

    def get(self, request):
        # 展示某节课程学习记录
        return render(request, 'study_list.html', {'formset': self.formset})

    def post(self, request):
        # 保存编辑学习记录
        form_set = self.StudyRecordFormSet(data=request.POST)
        if form_set.is_valid():
            form_set.save()
            # ajax
        return render(request, 'study_list.html', {'formset': form_set})

class AddStudyRecords(View):
    def post(self, request):
        # 批量操作
        course_ids = request.POST.getlist('id_list[]')
        for course_record_id in course_ids:
            students = models.CourseRecord.objects.get(pk=course_record_id).re_class.customer_set.filter(status='studying')
            studyrecord_list = []
            for student in students:
                if not models.StudyRecord.objects.filter(course_record_id=course_record_id, student=student).exists():
                    studyrecord_list.append(models.StudyRecord(course_record_id=course_record_id, student=student))
            models.StudyRecord.objects.bulk_create(studyrecord_list)
        return JsonResponse({'status': 400})