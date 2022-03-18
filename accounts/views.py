from multiprocessing import context
from django.shortcuts import redirect, render
from django.forms import formset_factory, inlineformset_factory, modelformset_factory
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models import F

# Create your views here.
from .models import *
from .forms import *
from .filter import *
from .decorators import *


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():

            my_group = Group.objects.filter(name='customer').count()
            print(my_group)

            username = form.cleaned_data.get('username')

            if my_group == 0:
                my_group = Group.objects.create(name='customer')
            else:
                my_group = Group.objects.get(name='customer')

            user = form.save()
            user = User.objects.get(username=username)
            user.groups.add(my_group) #Add this user to customers group
            messages.success(request, 'Account is created successfully for '+ username)
            return redirect('login')
 
    context = {'form' : form}

    return render(request, 'accounts/register.html', context)


@unauthenticated_user
def loginPage(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')
		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'accounts/login.html', context)


def logoutUser(request):
	logout(request)
	return redirect('login')


@login_required(login_url='login')      
@admin_only
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    #last_orders = Order.objects.all().order_by('-date_created')[0:5]
    # To reduces the redundant columns in the original object
    last_orders = Order.objects.select_related('customer__user', 'product').prefetch_related('product__tags').all().order_by('-date_created')[0:5]

    totalOrders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {
        'orders':orders,
        'customers':customers,
        'last_orders': last_orders,
        'totalOrders':totalOrders,
        'delivered':delivered,
        'pending':pending
        }
    return render(request, 'accounts/dashboard.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer']) 
def userPage(request):
    orders = request.user.customer.order_set.all()

    totalOrders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
     
    context = {'orders':orders, 'totalOrders':totalOrders,
    'delivered':delivered, 'pending':pending}
    return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer']) 
def updateCustomer(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context = {'form':form}
    return render(request, 'accounts/account_settings.html', context)   


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin']) 
def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html',{'products':products})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin']) 
def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)
    orders = customer.order_set.all()
    total_orders = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'customer':customer, 'orders':orders, 'total_orders':total_orders, 'myFilter':myFilter}

    return render(request, 'accounts/customer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createProduct(request):
    ProductFormSet = modelformset_factory(Product, form=CreateProductForm, extra=5)
    formset = ProductFormSet(queryset=Order.objects.none())
    if request.method == 'POST':
        formset = ProductFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('products')
    
    context = {'formset':formset}
    return render(request, 'accounts/create_product.html', context)          


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def MakeOrder(request):
    customer = request.user.customer
    form = MakeOrderForm()
    if request.method == 'POST':
        form = MakeOrderForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            order = form.save(commit=False)
            order.customer = customer
            for product in range(quantity):
                order.save()
                order.pk += 1
            Customer.objects.filter(pk=customer.id).update(customer_orders = F('customer_orders')+quantity)
            return redirect('user-page')
      
        
    context = {'form' : form}
    return render(request, 'accounts/make_order.html', context)


@login_required(login_url='login')  
@allowed_users(allowed_roles=['admin']) 
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
        return redirect('customer',customer.id)

    context = {'formset':formset}
    return render(request, 'accounts/place_order.html', context)   


@login_required(login_url='login') 
@allowed_users(allowed_roles=['admin']) 
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request, 'accounts/update_order.html', context)           


@login_required(login_url='login')  
@allowed_users(allowed_roles=['admin']) 
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    order = Order.objects.get(id=pk)
    context = {'item':order}
    return render(request, 'accounts/delete_order.html', context)


@login_required(login_url='login')  
@allowed_users(allowed_roles=['admin']) 
def deleteCustomerOrder(request, id):
    order = Order.objects.get(id=id)
    
    if request.method == 'POST':
        order.delete()
        return redirect('customer', order.customer.id)

    context = {'order':order}
    return render(request, 'accounts/delete_customer_order.html', context)    


