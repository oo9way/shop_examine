from rest_framework import serializers

from django.contrib.auth.hashers import make_password

from shop.models import Product, Shop, ChangeProductCountRequest
from shopadmin.models import User


class UsersListModelSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "is_admin",
            "is_shop_owner",
            "is_storekeeper",
        )

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            is_admin=validated_data["is_admin"],
            is_shop_owner=validated_data["is_shop_owner"],
            is_storekeeper=validated_data["is_storekeeper"],
        )

        user.set_password(validated_data["password"])
        user.save()

        return user


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "is_admin",
            "is_shop_owner",
            "is_storekeeper",
        )


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("title", "amount", "shop")


class ShopSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Shop
        fields = (
            "title",
            "image",
            "products",
            "owner",
            "shop_admins",
            "is_active",
        )


class ProductCountRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChangeProductCountRequest
        fields = ("product", "new_amount", "status")
