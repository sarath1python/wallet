from django.utils import timezone
from django.db.utils import IntegrityError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework import authentication, permissions
from wallet.v1.serializers import CustomerSerializer,\
    AccountCreateResponseSerializer, WalletAcivateResponseSerializer,\
    WalletDepositRequestSerializer, WalletDepositResponseSerializer,\
    WalletDeactivateResponseSerializer
from wallet.models import Customer, Transactions, Wallet
import short_codes as sc


class CustomerView(generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            token, created = Token.objects.get_or_create(
                user=serializer.instance)
            response = AccountCreateResponseSerializer(
                data={'token': str(token)})
            response.is_valid()

            return Response({
                "data": response.data,
                "status": sc.STATUS_SUCCESS
                }, status=status.HTTP_201_CREATED, headers=headers)

        except ValidationError:
            return Response({
                "data":
                    {
                        "errors": serializer.errors,
                    },
                "status": sc.STATUS_FAIL
                }, status=status.HTTP_400_BAD_REQUEST)


class WalletView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            wallet = Wallet.objects.get(owned_by=request.user, status=True)
            wallet_response = WalletAcivateResponseSerializer(wallet)

            return Response({
                "data": wallet_response.data,
                "status": sc.STATUS_SUCCESS
                }, status=status.HTTP_201_CREATED)

        except Wallet.DoesNotExist:
            return Response({
                "data": {
                    "error": sc.DISABLED
                },
                "status": sc.STATUS_FAIL
                }, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        try:
            wallet = Wallet.objects.filter(owned_by=request.user,
                                           status=False).first()
            if wallet:
                wallet.status = True
                wallet.enabled_at = timezone.now()
            else:
                wallet = Wallet(
                    owned_by=request.user,
                    enabled_at=timezone.now()
                )

            wallet.save()
            wallet_response = WalletAcivateResponseSerializer(wallet)

            return Response({
                "data": wallet_response.data,
                "status": sc.STATUS_SUCCESS
                }, status=status.HTTP_201_CREATED)

        except IntegrityError:
            return Response({
                "data": {
                    "error": sc.ALREADY_ENABLED
                },
                "status": sc.STATUS_FAIL
                }, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        try:
            wallet = Wallet.objects.get(owned_by=request.user, status=True)
            wallet.status = False
            wallet.disabled_at = timezone.now()
            wallet.save()
            wallet_response = WalletDeactivateResponseSerializer(wallet)

            return Response({
                "data": wallet_response.data,
                "status": sc.STATUS_SUCCESS
                }, status=status.HTTP_201_CREATED)

        except Wallet.DoesNotExist:
            return Response({
                "data": {
                    "error": sc.ALREADY_DISABLED
                },
                "status": sc.STATUS_FAIL
                }, status=status.HTTP_404_NOT_FOUND)


class WalletDepositView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            serialized_input = WalletDepositRequestSerializer(
                data=request.data)
            serialized_input.is_valid()
            wallet = Wallet.objects.get(owned_by=request.user, status=True)
            wallet_ineffect_balance = wallet.balance + int(
                serialized_input.data['amount'])

            transaction = Transactions.objects.create(
                customer=request.user,
                transaction_type='C',
                amount=serialized_input.data['amount'],
                balance=wallet_ineffect_balance,
                reference_id=serialized_input.data['reference_id'],
            )
            Wallet.objects.filter(id=wallet.id).update(
                balance=wallet_ineffect_balance)

            deposit_response = WalletDepositResponseSerializer(transaction)
            return Response({
                "data": {
                    "deposit": deposit_response.data,
                },
                "status": sc.STATUS_SUCCESS
                }, status=status.HTTP_201_CREATED)

        except IntegrityError:
            return Response({
                "data": {
                    "error": sc.TRANSACTION_ALREADY_DONE
                },
                "status": sc.STATUS_FAIL
                }, status=status.HTTP_400_BAD_REQUEST)


class WalletWithdrawalView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            serialized_input = WalletDepositRequestSerializer(data=request.data)
            serialized_input.is_valid()
            wallet = Wallet.objects.get(owned_by=request.user, status=True)
            if int(serialized_input.data['amount']) > wallet.balance:
                raise ValidationError('Withdrawal more than balance')
            wallet_ineffect_balance = wallet.balance - int(
                serialized_input.data['amount'])

            transaction = Transactions.objects.create(
                customer=request.user,
                transaction_type='C',
                amount=serialized_input.data['amount'],
                balance=wallet_ineffect_balance,
                reference_id=serialized_input.data['reference_id'],
            )
            Wallet.objects.filter(id=wallet.id).update(
                balance=wallet_ineffect_balance)

            deposit_response = WalletDepositResponseSerializer(transaction)
            return Response({
                "data": {
                    "withdrawal": deposit_response.data,
                },
                "status": sc.STATUS_SUCCESS
                }, status=status.HTTP_201_CREATED)

        except Exception as e:
            error_message = sc.TRANSACTION_ALREADY_DONE if e.__class__ == \
                IntegrityError else sc.WITHDRAWAL_MORE_THAN_WALLET

            return Response({
                "data": {
                    "error": error_message
                },
                "status": sc.STATUS_FAIL
                }, status=status.HTTP_400_BAD_REQUEST)
