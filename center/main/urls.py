from django.urls import path
from .views import *

#задаю локальный пути(ссулки)
urlpatterns = [
    path('', index, name='index_url'),
    path('seller/', CreateSeller.as_view(), name='create_seller_url'),
    path('buyer/', CreateBuyer.as_view(), name='create_buyer_url'),
    path('flat/', AddFlat.as_view(), name='add_flat_url'),
    path('contract/', CreateContract.as_view(), name='create_contract_url'),
    path('seller_view/', SellerView.as_view(), name='view_seller_url'),
    path('buyer_view/', BuyerView.as_view(), name='view_buyer_url'),
    path('contract_view/', ContractView.as_view(), name='view_contract_url'),
    path('flat_view/', FlatView.as_view(), name='view_flat_url'),

]
