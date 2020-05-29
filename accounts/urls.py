from django.urls import path
from accounts import views





urlpatterns = [

    path('',views.home, name ='home'),

    path('products',views.products, name ='products'),

    path('customer/<str:customer_pk>',views.customer, name ='customer'),

    path('create_order/<str:customer_pk>',views.createOrder, name = 'create_order'),

    path('update_order/<str:order_pk>', views.updateOrder, name= 'update_order'),

    path('delete_order/<str:order_pk>', views.deleteOrder, name = 'delete_order'),

    path ('register', views.registerUser, name = 'registration'),

    path('login', views.loginUser, name = 'login'),
    path('logout', views.logOut, name = 'logout'),
]
