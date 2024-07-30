from django.urls import path
from newapp import views
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    #path('place_order/', views.place_order, name='place_order'),
    path('customers/', views.customers, name='customers'),
     path('user-profile/', views.user_profile_view, name='user_profile_view'),
     path('update/<int:customer_id>/', views.customer_update, name='customer_update'),
    path('delete/<int:customer_id>/', views.customer_delete, name='customer_delete'),
    path('place_order', views.place_order, name='place_order'),
    path('update_order_status/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path('remove_order/<int:order_id>/', views.remove_order, name='remove_order'),
     path('order_list/', views.order_list, name='order_list'),  # Add this line
    
]

