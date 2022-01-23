import uuid
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser


class ModelMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Customer(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=50, blank=True, null=True,
                                unique=True)
    email = models.EmailField(_('email address'), blank=True, null=True,
                              unique=True)
    native_name = models.CharField(max_length=5, blank=True, null=True)
    phone_no = models.CharField(max_length=10, blank=True, null=True)
    customer_xid = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = 'customer_xid'
    REQUIRED_FIELDS = []

    def __str__(self):
        return "{}".format(self.customer_xid)


class Wallet(ModelMixin):
    owned_by = models.OneToOneField(Customer, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    balance = models.BigIntegerField(default=0)
    enabled_at = models.DateTimeField(blank=True, null=True)
    disabled_at = models.DateTimeField(blank=True, null=True)


class Transactions(ModelMixin):
    TRANSACTION_TYPE = [
        ('D', 'debt'),
        ('C', 'cred')
    ]
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    transaction_type = models.CharField(max_length=1,
                                        choices=TRANSACTION_TYPE)
    amount = models.BigIntegerField(default=0)
    balance = models.BigIntegerField(default=0)
    reference_id = models.CharField(max_length=50, unique=True, blank=False,
                                    null=False)
    status = models.BooleanField(default=True)
