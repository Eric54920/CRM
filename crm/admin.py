from django.contrib import admin
from .models import Department,UserProfile,Customer, ClassList, Campuses, ConsultRecord, Enrollment, PaymentRecord, CourseRecord, StudyRecord
# Register your models here.
admin.site.register([Department,UserProfile,Customer, ClassList, Campuses, ConsultRecord, Enrollment, PaymentRecord, CourseRecord, StudyRecord])