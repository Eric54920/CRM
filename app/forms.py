from django import forms
from django.core.exceptions import ValidationError
import hashlib
from app import models


class RegForm(forms.ModelForm):
    re_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '确认密码'}))

    class Meta:
        model = models.UserProfile
        fields = "__all__"
        exclude = ['is_active']
        widgets = {
            'username': forms.EmailInput(attrs={'placeholder': '用户名'}),
            'password': forms.PasswordInput(attrs={'placeholder': '密码'}),
        }
        labels = {
            'username': '用户名'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 自定义的操作
        self.fields['username'].widget.attrs['placeholder'] = '用户名'
        self.fields['password'].widget = forms.PasswordInput(attrs={'placeholder': '密码'})
        self.fields['name'].widget.attrs['placeholder'] = '姓名'
        self.fields['mobile'].widget.attrs['placeholder'] = '手机号'
        self.fields['department'].choices = [('', '请选择部门')] + list(models.Department.objects.values_list('id', 'name'))

    def clean(self):
        self._validate_unique = True  # 在数据库校验唯一性
        password = self.cleaned_data.get('password', '')
        re_password = self.cleaned_data.get('re_password')
        if password == re_password:
            md5 = hashlib.md5()
            md5.update(password.encode('utf-8'))

            self.cleaned_data['password'] = md5.hexdigest()
            return self.cleaned_data
        self.add_error('password', '两次密码不一致')
        raise ValidationError('两次密码不一致')


from multiselectfield.forms.fields import MultiSelectFormField


class BSForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if isinstance(field, (MultiSelectFormField, forms.BooleanField)):
                continue
            field.widget.attrs['class'] = 'form-control'


class CustomerForm(BSForm):
    class Meta:
        model = models.Customer
        fields = "__all__"  # ['qq','qq_name',]


class ConsultRecordForm(BSForm):
    class Meta:
        model = models.ConsultRecord
        fields = '__all__'

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['customer'].choices = models.Customer.objects.filter(consultant=request.user_obj).values_list('id',
                                                                                                                  'name')
        self.fields['consultant'].choices = [(request.user_obj.pk, request.user_obj)]


class EnrollmentForm(BSForm):
    class Meta:
        model = models.Enrollment
        fields = '__all__'

        labels = {
            'school': '校区'
        }

    def __init__(self, request, *args, **kwargs):
        super(EnrollmentForm, self).__init__(*args, **kwargs)
        # customer_obj = models.Customer.objects.get(pk=customer_id)
        # self.fields['customer'].choices = [(customer_id, customer_obj)]
        # self.fields['enrolment_class'].choices = [(i.pk, str(i)) for i in customer_obj.class_list.all()]

        # print(self.instance)
        # print(self.instance.customer)
        # print(self.instance.customer_id)
        if not self.instance.customer_id:
            self.fields['customer'].choices = [(i.pk, str(i)) for i in request.user_obj.customers.all()]
        else:
            self.fields['customer'].choices = [(self.instance.customer_id, self.instance.customer)]
            self.fields['enrolment_class'].choices = [(i.pk, str(i)) for i in self.instance.customer.class_list.all()]


class ClassListForm(BSForm):
    class Meta:
        model = models.ClassList
        fields = '__all__'


class CourseRecordForm(BSForm):
    class Meta:
        model = models.CourseRecord
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['re_class'].choices = [(self.instance.re_class_id, self.instance.re_class)]
        self.fields['recorder'].choices = [(self.instance.recorder_id, self.instance.recorder)]


class StudyRecordForm(BSForm):
    class Meta:
        model = models.StudyRecord
        fields = '__all__'