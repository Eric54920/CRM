from django.shortcuts import render, HttpResponse, redirect, reverse
from app import models
import hashlib
from app.forms import ClassListForm, CourseRecordForm, StudyRecordForm
from django.db import transaction
from .base import ShowList
from utils.pagination import Pagination


class ClassList(ShowList):

    def get(self, request, *args, **kwargs):
        all_classes = models.ClassList.objects.all()
        page = Pagination(request.GET.get('page', 1), all_classes.count(), request.GET.copy(), )
        return render(request, 'teacher/class_list.html', {
            'all_classes': all_classes[page.start:page.end],
            'page_html': page.page_html,
        })


def class_change(request, pk=None):
    obj = models.ClassList.objects.filter(pk=pk).first()
    form_obj = ClassListForm(instance=obj)
    if request.method == 'POST':
        form_obj = ClassListForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            path = request.GET.get('path')
            return redirect(path)

    title = '编辑班级' if pk else '新增班级'
    return render(request, 'form.html', {'form_obj': form_obj, 'title': title})


class CourseRecordList(ShowList):

    def get(self, request, class_id):
        all_course_records = models.CourseRecord.objects.filter(re_class_id=class_id)
        page = Pagination(request.GET.get('page', 1), all_course_records.count(), request.GET.copy(), )
        return render(request, 'teacher/course_records_list.html', {
            'all_course_records': all_course_records[page.start:page.end],
            'page_html': page.page_html,
            'class_id': class_id
        })

    def multi_init(self):
        # 批量初始化学习记录
        pk_list = self.request.POST.getlist('pk')

        # for course_record_id in pk_list:
        #     # 根据一个课程记录生成学习记录
        #     students = models.CourseRecord.objects.get(pk=course_record_id).re_class.customer_set.filter(status='studying')
        #     for student in students:
        #         models.StudyRecord.objects.get_or_create(course_record_id=course_record_id,student=student)

        for course_record_id in pk_list:
            # 根据一个课程记录生成学习记录
            students = models.CourseRecord.objects.get(pk=course_record_id).re_class.customer_set.filter(
                status='studying')

            study_record_list = []
            for student in students:
                if not models.StudyRecord.objects.filter(course_record_id=course_record_id, student=student).exists():
                    study_record_list.append(models.StudyRecord(course_record_id=course_record_id, student=student))
            # 批量插入
            models.StudyRecord.objects.bulk_create(study_record_list)


def course_record_change(request, class_id=None, pk=None):
    obj = models.CourseRecord(re_class_id=class_id,
                              recorder=request.user_obj) if class_id else models.CourseRecord.objects.filter(
        pk=pk).first()
    form_obj = CourseRecordForm(instance=obj)
    if request.method == 'POST':
        form_obj = CourseRecordForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            path = request.GET.get('path')
            return redirect(path)

    title = '编辑课程记录' if pk else '新增课程记录'
    return render(request, 'form.html', {'form_obj': form_obj, 'title': title})


from django.forms import modelformset_factory


def study_record_list(request, course_record_id):
    ModelFormSet = modelformset_factory(models.StudyRecord, StudyRecordForm, extra=0)
    queryset = models.StudyRecord.objects.filter(course_record_id=course_record_id)
    form_set = ModelFormSet(queryset=queryset)

    if request.method == 'POST':
        form_set = ModelFormSet(data=request.POST)
        if form_set.is_valid():
            form_set.save()

    return render(request, 'teacher/study_record_list.html', {'form_set': form_set})
