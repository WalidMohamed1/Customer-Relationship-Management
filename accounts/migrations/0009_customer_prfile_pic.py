# Generated by Django 3.2.12 on 2022-03-14 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_customer_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='prfile_pic',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
