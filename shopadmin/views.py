from rest_framework import generics, viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404, render
from django_filters.rest_framework import DjangoFilterBackend

from utils.permissions import AdminsPermission
from shopadmin.serializers import (
    ProductCountRequestSerializer,
    UsersListModelSerializer,
    UserModelSerializer,
)
from shopadmin.models import User
from shopadmin.serializers import ProductSerializer, ShopSerializer
from shop.models import ChangeProductCountRequest, Product, Shop


class UsersListCreateView(generics.ListCreateAPIView):
    model = User
    queryset = User.objects.all()

    permission_classes = [AdminsPermission]
    serializer_class = UsersListModelSerializer
    filter_backends = [DjangoFilterBackend]


class UserDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    model = User
    queryset = User.objects.all()

    permission_classes = [AdminsPermission]
    serializer_class = UserModelSerializer


class AdminShopModelViewSet(viewsets.ModelViewSet):
    model = Shop
    permission_classes = [AdminsPermission]
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer


class AdminProductModelViewSet(viewsets.ModelViewSet):
    model = Product
    serializer_class = ProductSerializer
    permission_classes = [AdminsPermission]
    queryset = Product.objects.all()


class ChangeShopStatusAPIView(APIView):
    permission_classes = [AdminsPermission]

    def post(self, request, pk, action):
        shop = get_object_or_404(Shop, id=pk)

        if action == "activate" and shop.activate():
            return Response(
                {"detail": "Activated successfully"}, status=status.HTTP_200_OK
            )

        if action == "deactivate" and shop.deactivate():
            return Response(
                {"detail": "Deactivated successfully"}, status=status.HTTP_200_OK
            )


class ProductCountRequestsListAPIView(generics.ListAPIView):
    model = ChangeProductCountRequest
    permission_classes = [AdminsPermission]
    serializer_class = ProductCountRequestSerializer
    queryset = ChangeProductCountRequest.objects.all()


class ChangeProductCountRequestAPIView(APIView):
    permission_classes = [AdminsPermission]

    def post(self, request, pk, action):
        product_request = get_object_or_404(
            ChangeProductCountRequest, id=pk, status="INITIAL"
        )

        if action == "accept":
            product_request.change_status("accepted")
            product_request.product.set_amount(product_request.new_amount)

            return Response(
                {"detail": "Product amount is updated successfully"},
                status=status.HTTP_200_OK,
            )

        if action == "decline":
            product_request.change_status("declined")

        return Response(
            {"detail": "New product amount is declined"}, status=status.HTTP_200_OK
        )


class AddAdminToShopAPIView(APIView):
    permission_classes = [AdminsPermission]

    def post(self, request, shop, user):
        shop = get_object_or_404(Shop, pk=shop)
        user = get_object_or_404(User, pk=user, is_shop_owner=True)

        shop.add_admin(user)

        return Response(
            {"detail": "Added admin successfully"}, status=status.HTTP_200_OK
        )
