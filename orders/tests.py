from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Cart, CartItem
from products.models import Product


class CartItemManagementTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="customer",
            password="test-password",
        )
        self.product = Product.objects.create(
            name="Classic Tee",
            category="T-Shirts",
            price="25.00",
            size="M",
            color="Black",
            sku="CLASSIC-TEE",
            stock=5,
        )
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=1,
        )
        self.client.force_login(self.user)

    def test_update_cart_changes_quantity(self):
        response = self.client.post(
            reverse("update_cart", args=[self.product.pk]),
            {"quantity": 3},
        )

        self.assertRedirects(response, reverse("cart"))
        self.cart_item.refresh_from_db()
        self.assertEqual(self.cart_item.quantity, 3)

    def test_cart_page_shows_item_management_controls(self):
        response = self.client.get(reverse("cart"))

        self.assertContains(response, 'name="quantity"')
        self.assertContains(
            response,
            f'action="{reverse("update_cart", args=[self.product.pk])}"',
        )
        self.assertContains(
            response,
            f'action="{reverse("remove_from_cart", args=[self.product.pk])}"',
        )

    def test_update_cart_rejects_quantity_above_stock(self):
        response = self.client.post(
            reverse("update_cart", args=[self.product.pk]),
            {"quantity": 6},
        )

        self.assertRedirects(response, reverse("cart"))
        self.cart_item.refresh_from_db()
        self.assertEqual(self.cart_item.quantity, 1)

    def test_remove_from_cart_deletes_item(self):
        response = self.client.post(
            reverse("remove_from_cart", args=[self.product.pk]),
        )

        self.assertRedirects(response, reverse("cart"))
        self.assertFalse(CartItem.objects.filter(pk=self.cart_item.pk).exists())
