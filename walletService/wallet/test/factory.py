# factory.py inside customer/test
from faker import Faker as FakerClass
from typing import Any, Sequence
from factory import django, Faker

from wallet.models import Customer


class CustomerFactory(django.DjangoModelFactory):

    class Meta:
        model = Customer

    customer_xid = Faker('user_name')
    phone_no = Faker('phone_number')
