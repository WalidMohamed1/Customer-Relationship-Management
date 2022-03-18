from pyexpat import model
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Customer, Order, Product

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__' #All fields in Order class
        exclude = ['user']

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

class MakeOrderForm(ModelForm):
    quantity = forms.IntegerField()
    class Meta:
        model = Order
        fields = ['product']        

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class CreateProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['description','date_created','tags']

