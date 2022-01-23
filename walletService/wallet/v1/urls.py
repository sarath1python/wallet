from django.urls import path
from wallet.v1 import views as v1_views


urlpatterns = [
    path('init', v1_views.CustomerView.as_view(), name='create-customer'),
    path('wallet/deposits', v1_views.WalletDepositView.as_view(),
         name='wallet-deposit'),
    path('wallet/withdrawals', v1_views.WalletWithdrawalView.as_view(),
         name='wallet-withdrawal'),
    path('wallet', v1_views.WalletView.as_view(), name='wallet-get-create'),
]
