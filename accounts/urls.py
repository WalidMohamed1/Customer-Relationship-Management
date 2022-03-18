from re import template
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),


    path('', views.home, name='home'), #Base URL
    path('user/', views.userPage, name='user-page'),
    path('account/', views.accountSettings, name='account'),
    path('products/', views.products, name='products'),
    path('customer/<str:pk_test>/', views.customer, name='customer'),

    path("make_order/", views.MakeOrder, name="make_order"),

    path('create_order/<str:pk>/', views.createOrder, name='create_order'),
    path('update_order/<str:pk>/', views.updateOrder, name='update_order'),
    path('delete_order/<str:pk>/', views.deleteOrder, name='delete_order'),

    path('create_product/', views.createProduct, name ='create_product'),

    path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
      name="reset_password"),

    path('reset_password_sent/',
     auth_views.PasswordResetDoneView.as_view(template_name="accounts/passowrd_reset_sent.html"),
      name="password_reset_done"),

    path('reset<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="accounts/passowrd_reset_form.html"),
      name="password_reset_confirm"),

    path('reset_password_complete/',
     auth_views.PasswordResetCompleteView.as_view(template_name="accounts/passowrd_reset_done.html"),
      name="password_reset_complete"),



]