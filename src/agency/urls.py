# from agency.views import ClientDeleteView
# from agency.views import ClientUpdateView
# from agency.views import ClientDetailView
# from agency.views import ClientCreateView
# from agency.views import ClientListView
from .views import index
# from agency.views import HotelDeleteView
# from agency.views import HotelUpdateView
# from agency.views import HotelDetailView
# from agency.views import HotelCreateView
# from agency.views import HotelListView
# from agency.views import OrderDeleteView
# from agency.views import OrderUpdateView
# from agency.views import OrderDetailView
# from agency.views import OrderCreateView
# from agency.views import OrderListView
from django.urls import path


urlpatterns = [
    # path('order/list/', OrderListView.as_view(), name='order_list'),
    # path('order/create/', OrderCreateView.as_view(), name='order_create'),
    # path('order/detail/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    # path('order/update/<int:pk>/', OrderUpdateView.as_view(), name='order_update'),
    # path('order/delete/<int:pk>/', OrderDeleteView.as_view(), name='order_delete'),

    # path('hotel/list/', HotelListView.as_view(), name='hotel_list'),
    # path('hotel/create/', HotelCreateView.as_view(), name='hotel_create'),
    # path('hotel/detail/<int:pk>/', HotelDetailView.as_view(), name='hotel_detail'),
    # path('hotel/update/<int:pk>/', HotelUpdateView.as_view(), name='hotel_update'),
    # path('hotel/delete/<int:pk>/', HotelDeleteView.as_view(), name='hotel_delete'),

    # path('client/list/', ClientListView.as_view(), name='client_list'),
    # path('client/create/', ClientCreateView.as_view(), name='client_create'),
    # path('client/detail/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    # path('client/update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    # path('client/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),

    path('', index, name='index'),
]




