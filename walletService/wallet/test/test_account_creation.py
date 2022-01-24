from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from wallet.test.factory import CustomerFactory
from wallet.models import Customer


class CustomerAccountTestCase(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.customer_object = CustomerFactory.build()
        cls.customer_saved = CustomerFactory.create()
        cls.client = APIClient()
        cls.signup_url = reverse('create-customer')

    def test_customer_creation_on_valid_data(self):
        # Prepare data
        signup_dict = {
            'customer_xid': self.customer_object.customer_xid,
        }
        # Make request
        response = self.client.post(self.signup_url, signup_dict)
        # Check status response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 2)
        # Check database
        new_customer = Customer.objects.filter(
            customer_xid=self.customer_object.customer_xid)
        assert new_customer[0]

    def test_cancel_account_creation_if_customer_exist(self):
        # Prepare data with already saved customer
        signup_dict = {
            'customer_xid': self.customer_saved.customer_xid
        }
        # Make request
        response = self.client.post(self.signup_url, signup_dict)
        # Check status response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            str(response.data['data']['error']['customer_xid'][0]),
            'user with this customer xid already exists.',
        )
        self.assertEqual(
            str(response.data['status']),
            'fail',
        )
        # Check database
        # Check that there is only one customer with the saved customer_xid
        customers_queryset = Customer.objects.filter(
            customer_xid=self.customer_saved.customer_xid)
        self.assertEqual(customers_queryset.count(), 1)
