from multiprocessing import context
from django.shortcuts import redirect, render
from django.http import HttpResponse
from accounts.models import *
from .forms import OrderForm


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

def createOrder(request):
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request, 'accounts/order_form.html', context)   

def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request, 'accounts/order_form.html', context)           

def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    order = Order.objects.get(id=pk)
    context = {'item':order}
    return render(request, 'accounts/delete.html', context)
