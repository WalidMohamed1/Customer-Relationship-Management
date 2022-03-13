from dataclasses import field
import imp
from operator import iconcat
from sqlite3 import Date


import django_filters
from django_filters import DateFilter, CharFilter

from .models import *

class OrderFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name= "date_create", lookup_expr='gte')
    end_date = DateFilter(field_name= "date_create", lookup_expr='lte')
    note = CharFilter(field_name='note', lookup_expr='icontains')
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['customer', 'date_created']