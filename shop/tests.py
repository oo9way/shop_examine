# tests.py

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import (
    Token,
)  # Import Token model if you're using Token authentication
from .models import Product, Shop
from .serializers import ProductSerializer
from shopadmin.models import User


class ProductCreateAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create a user for authentication
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

        self.shop = Shop.objects.create(title="Test shop", owner=self.user)

        self.create_url = reverse("create-product", args=[self.shop.id])

    def test_create_product(self):
        # Define the data you want to send in the request
        product_data = {
            "title": "Test Product",
            "amount": 19,
        }

        self.client.force_authenticate(user=self.user)

        # Send a POST request to the create URL with the product data
        response = self.client.post(self.create_url, product_data, format="json")
        print(response.data)

        # Check if the response status code is 201 (created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
