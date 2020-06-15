from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse
import json
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime
from django.contrib import messages


def product(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        cartItems = order.get_cart_items

    else:
        order = {"get_cart_total": 0, "get_cart_items": 0}
        cartItems = order['get_cart_items']

    products = Product.objects.all().order_by('-id')
    context = {
        "title": "Home",
        "products": products,
        "cartItems": cartItems
    }
    return render(request, "product/products.html", context)


def technology(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        cartItems = order.get_cart_items
    else:
        order = {"get_cart_total": 0, "get_cart_items": 0}
        cartItems = order['get_cart_items']

    technology = Product.objects.filter(category="technology").order_by('-id')
    context = {
        "title": "Technology",
        "products": technology,
        "cartItems": cartItems
    }
    return render(request, "product/products.html", context)


def clothes(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        cartItems = order.get_cart_items
    else:
        order = {"get_cart_total": 0, "get_cart_items": 0}
        cartItems = order['get_cart_items']

    clothes = Product.objects.filter(category="clothes").order_by('-id')
    context = {
        "title": "Clothes",
        "products": clothes,
        "cartItems": cartItems
    }
    return render(request, "product/products.html", context)


def product_view(request, pk):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        cartItems = order.get_cart_items
    else:
        order = {"get_cart_total": 0, "get_cart_items": 0}
        cartItems = order['get_cart_items']

    product = Product.objects.get(id=pk)
    context = {
        "title": product.name,
        "product": product,
        "cartItems": cartItems
    }
    return render(request, 'product/product_detail.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {"get_cart_total": 0, "get_cart_items": 0}
        cartItems = order['get_cart_items']

    context = {
        "title": "Cart",
        "items": items,
        "order": order,
        "cartItems": cartItems
    }
    return render(request, "product/cart.html", context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {"get_cart_total": 0, "get_cart_items": 0}
        cartItems = order['get_cart_items']
    myProductList = []
    for item in items:
        myProductList.append(
            f"Product Name: {item.product.name}\nProduct Price: ${item.product.price}\nProduct Quantity: x{item.quantity}\n-----------------\n"
        )

    customerProducts = "".join(myProductList)

    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        country = request.POST['country']
        city = request.POST['city']
        region = request.POST['region']
        address = request.POST['address']
        phone = request.POST['phone']

        if first_name and last_name and email and country and city and region and address and phone:
            send_mail(f"{first_name} {last_name}: {datetime.now()}",
                      f'Request Customer:\nUsername: {request.user.username}\nFull Name: {request.user.first_name} {request.user.last_name}\nEmail: {request.user.email}\n\nForm Customer:\nFirst name:  {first_name}\nLast Name: {last_name}\nEmail: {email}\nCountry: {country}\nCity: {city}\nRegion: {region}\nAddress: {address}\nPhone Number: {phone}\n\nProducts: \n-----------------\n{customerProducts}\nItems: {order.get_cart_items}\nTotal: ${order.get_cart_total}',
                      settings.EMAIL_HOST_USER,
                      ['Email Name'],
                      fail_silently=False)
            return redirect('home')
        else:
            messages.warning(request,"Fill Out The Form")

    context = {
        "title": "Checkout",
        "items": items,
        "order": order,
        "cartItems": cartItems
    }
    return render(request, "product/checkout.html", context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print(f"ProductId: {productId}\nAction: {action}")

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)

    if action == "add":
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == "remove":
        orderItem.quantity = (orderItem.quantity - 1)
    elif action == "set_null":
        orderItem.quantity = (orderItem.quantity - orderItem.quantity)
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse("Ma`lumotlar ishlamoqda", safe=False)
