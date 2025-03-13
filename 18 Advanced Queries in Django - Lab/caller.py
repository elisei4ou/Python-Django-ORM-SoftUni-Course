import os
import django
from django.db.models import F, ExpressionWrapper

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
from main_app.models import Product, Category, Customer, Order, OrderProduct
from django.db.models.aggregates import Count, Sum


def product_quantity_ordered():
    all_orders = (Product.objects
                  .annotate(order_quantity=Sum('orderproduct__quantity'))
                  .order_by('-order_quantity')
                  .filter(order_quantity__gte=1))

    return '\n'.join(f'Quantity ordered of {o.name}: {o.order_quantity}' for o in all_orders)


def ordered_products_per_customer():
    all_orders = Order.objects.prefetch_related('orderproduct_set__product__category').order_by('id')

    result = []

    for order in all_orders:
        result.append(f"Order ID: {order.id}, Customer: {order.customer.username}")

        for orderd_product in order.orderproduct_set.all():
            result.append(f'- Product: {orderd_product.product.name}, Category: {orderd_product.product.category.name}')

    return '\n'.join(result)



def filter_products():
    products = Product.objects.filter(is_available=True, price__gt=3.00).order_by('-price', 'name')

    return '\n'.join(f"{p.name}: {p.price}lv." for p in products)



def give_discount():
    Product.objects.filter(is_available=True, price__gt=3.00).update(price=F('price') * 0.7)
    all_products = Product.objects.filter(is_available=True).order_by('-price', 'name')

    return '\n'.join(f"{p.name}: {p.price}lv." for p in all_products)







