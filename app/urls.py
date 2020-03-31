from django.conf.urls import url
from app.views import consultant,teacher

urlpatterns = [
    url(r'^login/$', consultant.login, name='login'),
    url(r'^register/$', consultant.register, name='register'),
    url(r'^customer/$', consultant.Customer.as_view(), name='customer'),
    url(r'^my_customer/$', consultant.Customer.as_view(), name='my_customer'),
    # url(r'^customer_add/$', views.customer_add, name='customer_add'),
    # url(r'^customer_edit/(\d+)/$', views.customer_edit, name='customer_edit'),
    url(r'^customer_add/$', consultant.customer_change, name='customer_add'),
    url(r'^customer_edit/(\d+)/$', consultant.customer_change, name='customer_edit'),
    #  展示某个销售的所有的跟进记录
    url(r'^consult_record/$', consultant.ConsultRecordList.as_view(), name='consult_record'),
    #  展示某个客户的所有的跟进记录
    url(r'^consult_record/(?P<customer_id>\d+)/$', consultant.ConsultRecordList.as_view(), name='one_consult_record'),

    url(r'^consult_record_add/$', consultant.consult_record_change, name='consult_record_add'),
    url(r'^consult_record_edit/(\d+)/$', consultant.consult_record_change, name='consult_record_edit'),

    url(r'^enrollment_list/$', consultant.EnrollmentList.as_view(), name='enrollment_list'),
    url(r'^enrollment_list/(?P<customer_id>\d+)/$', consultant.EnrollmentList.as_view(), name='one_enrollment_list'),

    url(r'^enrollment_add/(?P<customer_id>\d+)$', consultant.enrollment_change, name='enrollment_add'),
    url(r'^enrollment_add/$', consultant.enrollment_change, name='enrollment_add2'),
    url(r'^enrollment_edit/(?P<pk>\d+)$', consultant.enrollment_change, name='enrollment_edit'),

    url(r'^class_list/$', teacher.ClassList.as_view(), name='class_list'),
    url(r'^class_add/$', teacher.class_change, name='class_add'),
    url(r'^class_edit/(\d+)/$', teacher.class_change, name='class_edit'),

    url(r'^course_record_list/(?P<class_id>\d+)/$', teacher.CourseRecordList.as_view(), name='course_record_list'),

    url(r'^course_record_add/(?P<class_id>\d+)/$', teacher.course_record_change, name='course_record_add'),
    url(r'^course_record_edit/(?P<pk>\d+)/$', teacher.course_record_change, name='course_record_add_edit'),

    url(r'^study_record_list/(?P<course_record_id>\d+)/$', teacher.study_record_list, name='study_record_list'),

]
