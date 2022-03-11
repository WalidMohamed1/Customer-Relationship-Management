from django.urls import path
from . import views

urlpatterns = [
    path('', views.home), #Base URL
    path('products/', views.products),
    path('customer/', views.customer),

]