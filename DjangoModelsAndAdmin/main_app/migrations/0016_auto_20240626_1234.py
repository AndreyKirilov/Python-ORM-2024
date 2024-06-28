# Generated by Django 5.0.4 on 2024-06-26 09:34

from django.db import migrations
from django.utils import timezone


def modify_delivery_and_warranty(apps, schema_editor):
    order_model = apps.get_model('main_app', 'Order')
    all_orders = order_model.objects.all()

    for order in all_orders:
        if order.status == 'Pending':
            order.delivery = order.order_date + timezone.timedelta(days=3)

        elif order.status == 'Completed':
            order.warranty = '24 months'

        elif order.status == 'Cancelled':
            order.delete()


def reverse_delivery_and_warranty(apps, schema_editor):
    order_model = apps.get_model('main_app', 'Order')
    all_orders = order_model.objects.all()

    for order in all_orders:
        if order.status == 'Pending':
            order.delivery = None

        elif order.status == 'Completed':
            order.warranty = order_model._meta.get_field('warranty').default

        order.save()


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0015_order'),
    ]

    operations = [migrations.RunPython(modify_delivery_and_warranty, reverse_delivery_and_warranty)]
