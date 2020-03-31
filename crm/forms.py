from . import models
from django import forms
from django.core.exceptions import ValidationError
import hashlib


def md5(str):
    md5 = hashlib.md5()
    md5.update(str.encode('utf-8'))
    return md5.hexdigest()

class RegForm(forms.ModelForm):
    re_password = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'class': 'form-control', 'placeholder':'确认密码'}))

    class Meta:
        model = models.UserProfile
        fields = '__all__'
        exclude = ['is_active', 'memo']
        widgets = {
            'username': forms.widgets.Input(attrs={'class': 'form-control', 'placeholder':'用户名'}),
            'password': forms.widgets.PasswordInput(attrs={'class': 'form-control', 'placeholder':'密码'}),
            'name': forms.widgets.Input(attrs={'class': 'form-control', 'placeholder':'姓名'}),
            'department': forms.widgets.Select(attrs={'class': 'form-control', 'placeholder':'部门'}),
            'mobile': forms.widgets.Input(attrs={'class': 'form-control', 'placeholder':'手机号'})
        }

    def __init__(self, *args, **kwargs):
        super(RegForm, self).__init__(*args, **kwargs)
        # self.fields['username'].widgets.attrs['username'] = 'xxxx'
        self.fields['department'].choices = [('', '请选择部门')] + list(models.Department.objects.values_list('pk','name'))

    def clean(self):
        self._validate_unique = True
        password = self.cleaned_data.get('password', '')
        re_password = self.cleaned_data.get('re_password')
        if password == re_password:
            self.cleaned_data['password'] = md5(password)
            return self.cleaned_data
        self.add_error('password','两次账号不一致')
        raise ValidationError('两次账号不一致')

class Customers(forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = '__all__'
        widgets = {
            'qq': forms.widgets.Input(attrs={'class': 'form-control'}),
            'qq_name': forms.widgets.Input(attrs={'class': 'form-control'}),
            'name': forms.widgets.Input(attrs={'class': 'form-control'}),
            'sex': forms.widgets.Select(attrs={'class': 'form-control'}),
            'birthday': forms.widgets.DateInput(attrs={'class': 'form-control', 'type':"date"}),
            'phone': forms.widgets.Input(attrs={'class': 'form-control'}),
            'source': forms.widgets.Select(attrs={'class': 'form-control'}),
            'introduce_from': forms.widgets.Select(attrs={'class': 'form-control'}),
            'course': forms.widgets.SelectMultiple(attrs={'class': 'form-control'}),
            'class_type': forms.widgets.Select(attrs={'class': 'form-control'}),
            'customer_note': forms.widgets.Textarea(attrs={'class': 'form-control'}),
            'status': forms.widgets.Select(attrs={'class': 'form-control'}),
            'next_date': forms.widgets.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'consultant': forms.widgets.Select(attrs={'class': 'form-control'}),
            'class_list': forms.widgets.SelectMultiple(attrs={'class': 'form-control'})
        }
    def __init__(self, *args, **kwargs):
        super(Customers, self).__init__(*args, **kwargs)
        self.fields['sex'].choices = [('', '请选择性别')] + list(models.Customer.sex_type)
        self.fields['source'].choices = list(models.source_type)
        self.fields['introduce_from'].choices = list(models.Customer.objects.all().values_list('pk', 'name'))
        self.fields['consultant'].choices = [('', '请选择销售')] + list(models.UserProfile.objects.filter(department__name='销售部').values_list('pk', 'name'))
        # for key, val in enumerate(self.fields):
        #     if not self.fields[val].required:
        #         self.fields[val].widget.attrs['class'] = 'not-required'

class Classes(forms.ModelForm):

    class Meta:
        model = models.ClassList
        fields = '__all__'
        widgets = {
            'course': forms.widgets.Select(),
            'semester': forms.widgets.NumberInput(),
            'campuses': forms.widgets.Select(),
            'price': forms.widgets.NumberInput(),
            'start_date': forms.widgets.DateInput(attrs={'type': 'date'}),
            'graduate_date': forms.widgets.DateInput(attrs={'type': 'date'}),
            'teachers': forms.widgets.SelectMultiple(),
            'class_type': forms.widgets.Select()
        }

    def __init__(self, *args, **kwargs):
        super(Classes, self).__init__(*args, **kwargs)
        self.fields['course'].choices = [('', '请选择课程')] + list(models.course_choices)
        self.fields['campuses'].choices = [('', '请选择校区')] + list(models.Campuses.objects.all().values_list('pk', 'name'))
        self.fields['teachers'].choices = [('', '请选择老师')] + list(models.UserProfile.objects.filter(department__name='教师部').values_list('pk', 'name'))
        self.fields['class_type'].choices = [('', '请选择班级类型')] + list(models.class_type_choices)
        for key, val in enumerate(self.fields):
            self.fields[val].widget.attrs['class'] = 'form-control'


class ConsultRecords(forms.ModelForm):
    class Meta:
        model = models.ConsultRecord
        fields = '__all__'

    def __init__(self, request, *args, **kwargs):
        super(ConsultRecords, self).__init__(*args, **kwargs)
        self.fields['customer'].choices = [('', '请选择客户')] + list(models.Customer.objects.filter(consultant=request.user_obj).values_list('pk', 'name'))
        self.fields['status'].choices = [('', '请选择跟进状态')] + list(models.seek_status_choices)
        self.fields['consultant'].choices = [(request.user_obj.pk, request.user_obj.name)]

        for key, val in enumerate(self.fields):
            self.fields[val].widget.attrs['class'] = 'form-control'

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = models.Enrollment
        fields = ['customer', 'enrolment_class', 'contract_approved', 'contract_agreed', 'memo', 'why_us', 'your_expectation', 'delete_status']
        
    def __init__(self, enrollment_id, *args, **kwargs):
        super(EnrollmentForm, self).__init__(*args, **kwargs)
        cus_obj = models.Customer.objects.get(pk=enrollment_id)
        self.fields['customer'].choices = [(cus_obj.pk, cus_obj.name)]
        self.fields['enrolment_class'].choices = [('', '请选择班级')] + [(i.pk, i) for i in cus_obj.class_list.all()]
        for key, val in enumerate(self.fields):
            self.fields[val].widget.attrs['class'] = 'form-control'

class PaymentRecordForm(forms.ModelForm):

    class Meta:
        model = models.PaymentRecord
        fields = ['customer', 'course', 'pay_type', 'paid_fee', 'class_type', 'enrolment_class', 'consultant', 'delete_status', 'status', 'confirm_date', 'confirm_user', 'note']
        widgets = {
            'confirm_date': forms.widgets.DateInput(attrs={'type': 'date'})
        }
    def __init__(self, *args, **kwargs):
        super(PaymentRecordForm, self).__init__(*args, **kwargs)
        self.fields['customer'].choices = [('', '请选择客户')] + list(models.Customer.objects.all().values_list('pk', 'name'))
        self.fields['enrolment_class'].choices = [('', '请选择所报班级')] + list((i.pk, i) for i in models.ClassList.objects.all())
        self.fields['pay_type'].choices = [('', '费用类型')] + list(models.pay_type_choices)
        self.fields['course'].choices = [('', '课程名')] + list(models.course_choices)
        self.fields['class_type'].choices = [('', '班级类型')] + list(models.class_type_choices)
        self.fields['status'].choices = [('', '审核状态')] + list(models.PaymentRecord.status_choices)
        self.fields['consultant'].choices = [('', '请选择销售')] + list(models.UserProfile.objects.filter(department__name='销售部').values_list('pk', 'name'))
        self.fields['confirm_user'].choices = [('', '审核确认人')] + list(models.UserProfile.objects.filter(department__name='销售部').values_list('pk', 'name'))
        for key, val in enumerate(self.fields):
            self.fields[val].widget.attrs['class'] = 'form-control'

class CourseRecordForm(forms.ModelForm):
    class Meta:
        model = models.CourseRecord
        fields = ['re_class', 'day_num', 'course_title', 'course_memo', 'teacher', 'has_homework', 'homework_title', 'homework_memo', 'scoring_point', 'recorder']

    def __init__(self, request, *args, class_id=None, **kwargs):
        super(CourseRecordForm, self).__init__(*args, **kwargs)
        self.fields['re_class'].choices = [(class_id, models.ClassList.objects.get(pk=class_id))]
        self.fields['teacher'].choices = [('', '请选择老师')] + list(models.UserProfile.objects.filter(department__name='教师部').values_list('pk', 'name'))
        self.fields['recorder'].choices = [(request.user_obj.pk, request.user_obj)]
        for key, val in enumerate(self.fields):
            self.fields[val].widget.attrs['class'] = 'form-control'


class StudyRecordForm(forms.ModelForm):
    class Meta:
        model = models.StudyRecord
        fields = ['attendance', 'student', 'course_record', 'score', 'homework_note', 'note']

    def __init__(self, *args, **kwargs):
        super(StudyRecordForm, self).__init__(*args, **kwargs)
        self.fields['attendance'].choices = [('', '考勤')] + list(models.attendance_choices)
        self.fields['score'].choices = [('', '本节成绩')] + list(models.score_choices)
        self.fields['course_record'].choices = [('', '请选择课程')] + list(models.CourseRecord.objects.all().order_by('pk').reverse().values_list('pk', 'course_title'))
        self.fields['student'].choices = [('', '请选择学员')] + list(models.Customer.objects.all().values_list('pk', 'name'))
        for key, val in enumerate(self.fields):
            self.fields[val].widget.attrs['class'] = 'form-control'