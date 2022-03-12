from multiprocessing import context
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from accounts.models import *


# Create your views here.

def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()

    totalCustomers = customers.count()
    totalOrders = orders.count()

    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {'orders':orders, 'customers':customers, 'totalOrders':totalOrders,
    'delivered':delivered, 'pending':pending}
    return render(request, 'accounts/dashboard.html',context)

def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html',{'products':products})

def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)
    orders = customer.order_set.all()
    total_orders = orders.count()
    context = {'customer':customer, 'orders':orders, 'total_orders':total_orders}

    return render(request, 'accounts/customer.html', context)          