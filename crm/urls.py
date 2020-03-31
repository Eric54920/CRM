from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/', views.Login.as_view(), name="login"),
    url(r'^regist/', views.Regist.as_view(), name="regist"),

    url(r'^customer/', views.Customer.as_view(), name="customer"),
    url(r'^my_customer/', views.Customer.as_view(), name="my_customer"),
    url(r'^add_customers/', views.AddCustomer.as_view(), name="add_customers"),
    url(r'^edit_custom/', views.EditCustomer.as_view(), name="edit_custom"),
    url(r'^custom_transfer/', views.CustomTransfer.as_view(), name="custom_transfer"),

    url(r'^class_list/', views.Class.as_view(), name="class_list"),
    url(r'^add_class/', views.AddClass.as_view(), name="add_class"),
    url(r'^edit_class/', views.EditClass.as_view(), name="edit_class"),

    url(r'^consult/', views.ConsultRecord.as_view(), name="consult"),
    url(r'^one_customer/(?P<customer_id>[0-9]+)', views.ConsultRecord.as_view(), name="one_customer"),
    url(r'^add_consult/', views.AddConsultRecord.as_view(), name="add_consult"),
    url(r'^edit_consult/', views.EditConsultRecord.as_view(), name="edit_consult"),

    url(r'^enrollments/', views.Enrollments.as_view(), name="enrollments"),
    url(r'^add_enrollment/(?P<enrollment_id>\d+)', views.AddEnrollments.as_view(), name="add_enrollment"),
    url(r'^edit_enrollment/', views.EditEnrollments.as_view(), name="edit_enrollment"),

    url(r'^paymentrecord/', views.PaymentRecords.as_view(), name="paymentrecord"),
    url(r'^add_paymentrecord/', views.AddPaymentRecords.as_view(), name="add_paymentrecord"),
    url(r'^edit_paymentRecord/', views.EditPaymentRecords.as_view(), name="edit_paymentRecord"),

    url(r'^courserecord/', views.CourseRecord.as_view(), name="courserecord"),
    url(r'^add_courserecord/\d+', views.AddCourseRecord.as_view(), name="add_courserecord"),
    url(r'^edit_courserecord/', views.EditCourseRecord.as_view(), name="edit_courserecord"),

    url(r'^studyrecord/(?P<course_id>\d+)', views.StudyRecords.as_view(), name="studyrecord"),
    url(r'^operate_all/', views.AddStudyRecords.as_view(), name="operate_all"),

    url(r'^user_list/', views.UserList.as_view(), name="user_list"),

    url(r'^del_([a-z]+)/([0-9]+)', views.Delete_obj.as_view(), name="delete_obj"),
] 