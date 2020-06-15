from django.urls import path
from . import views

urlpatterns = [
    path("", views.product,name="home"),
    path("technology/",views.technology,name="technology"),
    path("clothes/",views.clothes,name="clothes"),
    path("product/<str:pk>/",views.product_view,name="product-view"),
    path("cart/",views.cart,name="cart"),
    path("checkout/",views.checkout,name="checkout"),
    path("update_item/",views.updateItem,name="update_item"),
]
