from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name='home'),
    path('products', views.products,name='products'),
    path('customer/<str:keyy>/', views.customer,name='customer'),
    path('create_order/<str:keyy>', views.create_order, name='create_order'),
    path('create_order/', views.create_order, name='create_order'),
    path('add_product', views.add_product,name='add_product'),
    path('add_customer', views.add_customer, name='add_customer'),
    path('update_customer/<str:pk>', views.update_customer, name='update_customer'),
    path('update_order/<str:pk>',views.update_order,name='update_order'),
    path('delete_order/<str:pk>',views.delete_order,name='delete_order'),
    path('register/', views.registerPage, name="register"),
   	path('login/', views.loginPage, name="login"),
   	path('logout/', views.logoutUser, name="logout"),
    path('user/', views.userPage, name="user-page"),
    path('account/', views.accountSettings, name="account_settings"),
    ]
