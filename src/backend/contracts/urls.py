from django.urls import path

from backend.contracts.views import ContractAPIView, ContractView, IndexView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("contracts/<str:address>/", ContractView.as_view(), name="contract"),
    path("api/contracts/<str:address>/", ContractAPIView.as_view(), name="contract_api"),
]
