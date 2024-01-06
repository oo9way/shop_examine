from rest_framework import serializers
from shop.models import Product, Shop


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("title", "amount")


class ShopSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    is_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = Shop
        fields = (
            "title",
            "image",
            "products",
            "shop_admins",
            "is_active",
        )
