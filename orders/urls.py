from django.urls import path
from . import views

urlpatterns = [
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/update/<int:product_id>/", views.update_cart, name="update_cart"),
    path("cart/remove/<int:product_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("cart/", views.view_cart, name="cart"),
    path("cart/checkout/", views.checkout, name="checkout"),
    path("place-order/", views.place_order, name="place_order"),
    path("my-orders/", views.my_orders, name="my_orders"),
    path("my-orders/<int:order_id>", views.order_details, name="order_details"),
    path("cancel/<int:order_id>", views.cancel_order, name="cancel_order"),
]
