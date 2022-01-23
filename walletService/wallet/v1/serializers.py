from datetime import datetime
from rest_framework import serializers
from wallet.models import Customer, Transactions, Wallet


class WalletDepositRequestSerializer(serializers.Serializer):
    amount = serializers.IntegerField(required=True)
    reference_id = serializers.CharField(max_length=50)


class WalletDepositResponseSerializer(serializers.ModelSerializer):
    deposited_by = serializers.CharField(source='customer')
    deposited_at = serializers.DateTimeField(source='created_at')

    class Meta:
        model = Transactions
        fields = ["id", "deposited_by", "status", "deposited_at",
                  "amount", "reference_id"]


class WalletWithdrawalResponseSerializer(serializers.ModelSerializer):
    withdrawn_by = serializers.CharField(source='customer')
    withdrawn_at = serializers.DateTimeField(source='created_at')

    class Meta:
        model = Transactions
        fields = ["id", "deposited_by", "status", "deposited_at",
                  "amount", "reference_id"]


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["customer_xid"]


class WalletActivateSerializer(serializers.ModelSerializer):
    owned_by = CustomerSerializer(many=False, required=False)
    status = serializers.BooleanField(default=True, required=False)
    balance = serializers.IntegerField(default=0, required=False)
    enabled_at = serializers.DateTimeField(default=datetime.now(),
                                           required=False)

    class Meta:
        model = Wallet
        fields = ["id", "owned_by", "status", "enabled_at", "balance"]


class WalletAcivateResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ["id", "owned_by", "status", "enabled_at", "balance"]


class WalletDeactivateResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ["id", "owned_by", "status", "disabled_at", "balance"]


class AccountCreateResponseSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=50)
