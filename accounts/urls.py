# created 
# from django.contrib import admin
from django.urls import path

# importing views
from . import views



urlpatterns = [
    path('register/',views.registerPage,name="register"),
    path('',views.loginPage,name="login"),
    path('logout/',views.logotUser,name="logout"),
    path('home/',views.home,name='home'),
    path('products/',views.products,name='product'),
    path('customers/<str:pk>',views.customers,name='customers'),
    path('create_order/<str:pk>/',views.createOrder,name='create_order'), 
    path('updateorder_form/<str:pk>/',views.updateOrder,name='update_form'),
    path('deleteorder/<str:pk>/',views.deleteOrder,name='delete_order'),
    path('create_cus',views.createCus,name='create_cust'),
    path('create_products',views.createPro,name='create_products'),
    path('update_customer/<str:pk>/',views.updateCus,name='updatecus'),
    path('users/',views.userPage,name='user')


]