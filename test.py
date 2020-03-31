import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tf_crm.settings")
import django
django.setup()
from crm import models
from faker import Faker
import random
import hashlib


def md5(str):
    md5 = hashlib.md5()
    md5.update(str.encode('utf-8'))
    return md5.hexdigest()


faker = Faker(locale='zh-CN')
for i in range(30):
    # models.Customer.objects.create(username=faker.email(),
    #                                   password=md5('1234'),
    #                                   name=faker.name(),
    #                                   department_id=random.randint(1, 8),
    #                                   mobile=faker.phone_number(),
    #                                   memo='路飞学城',
    #                                   date_joined='2019-11-20 07:18:21.731350',
    #                                   is_active=random.randint(0, 1))

    models.Customer.objects.create(
        qq=faker.random_number(digits=9),
        name=faker.name(),
        qq_name=faker.word(),
        phone=faker.phone_number(),
        sex='男',
        source='qq',
        course='Python',
        class_type='fulltime',
        customer_note=faker.sentence(),
        status='signed',
        consultant_id=5,
        introduce_from_id=1)
