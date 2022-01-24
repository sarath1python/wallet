from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from wallet.test.factory import CustomerFactory
from wallet.models import Wallet


class EnableWalletTestCase(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.customer_saved = CustomerFactory.create()
        cls.client = APIClient()
        cls.wallet_enable_url = reverse('wallet-get-create')
        cls.signup_url = reverse('create-customer')

    def test_enable_wallet_for_existing_user(self):
        self.client.force_authenticate(user=self.customer_saved)
        # Make request
        response = self.client.post(self.wallet_enable_url)
        wallet = Wallet.objects.filter(owned_by=self.customer_saved.id).first()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['data']['owned_by'], self.customer_saved.id)
        self.assertEqual(bool(response.data['data']['status']), True)
        self.assertEqual(int(response.data['data']['balance']), 0)

    def test_400_raised_if_already_enabled(self):
        self.client.force_authenticate(user=self.customer_saved)
        # Make request to enable the wallet
        self.client.post(self.wallet_enable_url)
        
        # Trying to enable it again
        response = self.client.post(self.wallet_enable_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['data']['error'], 'Already enabled')
        self.assertEqual(response.data['status'], 'fail')

    def test_401_on_anonymous_user_attempt(self):
        # Make anonymous request to enable the wallet
        response = self.client.post(self.wallet_enable_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
