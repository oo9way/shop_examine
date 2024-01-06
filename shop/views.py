from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets, generics, views, exceptions, status
from rest_framework.response import Response
from shop.models import Product, Shop
from shop.serializers import ProductSerializer, ShopSerializer
from utils.permissions import HasAccessProduct, HasAccessShop, IsActiveShop
from rest_framework.permissions import IsAuthenticated


class ShopModelViewSet(viewsets.ModelViewSet):
    model = Shop
    permission_classes = [IsAuthenticated, HasAccessShop]
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_admin:
            queryset = queryset.filter(owner=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ShopProducts(generics.ListAPIView):
    model = Product
    permission_classes = [IsAuthenticated, HasAccessShop]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_object(self, shop_id):
        try:
            return Shop.objects.get(pk=shop_id, owner=self.request.user)
        except Shop.DoesNotExist:
            raise exceptions.NotFound

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_admin:
            queryset = queryset.filter(shop__in=self.request.user.shops.all())
        return queryset


class AddNewProductToShop(views.APIView):
    permission_classes = [IsAuthenticated, IsActiveShop]
    serializer_class = ProductSerializer

    def get_object(self, shop_id):
        try:
            return Shop.objects.get(pk=shop_id)
        except Shop.DoesNotExist:
            raise exceptions.NotFound

    def post(self, request, shop_id, *args, **kwargs):
        shop = self.get_object(shop_id)
        data = request.data

        title = data["title"]
        amount = data["amount"]

        product = {
            "title": title,
            "amount": amount,
        }

        if shop.add_product(product):
            return Response(
                {"details": "Product is added successfully"}, status=status.HTTP_200_OK
            )

        return Response(
            {"details": "Product isn't added"}, status=status.HTTP_400_BAD_REQUEST
        )
