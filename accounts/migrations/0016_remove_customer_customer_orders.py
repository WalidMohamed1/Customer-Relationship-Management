# Generated by Django 3.2.12 on 2022-03-18 18:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_remove_customer_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='customer_orders',
        ),
    ]
