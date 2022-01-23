from django.urls import path, include


urlpatterns = [
    path('v1/', include('wallet.v1.urls'), name='v1-wallet'),
]
