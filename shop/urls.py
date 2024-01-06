from shop import views
from django.urls import path
from rest_framework.routers import DefaultRouter
from shop import views


urlpatterns = [
    path(
        "shops/<int:shop_id>/products/add/",
        views.AddNewProductToShop.as_view(),
        name="create-product",
    ),
    path("shops/<int:shop_id>/products/", views.ShopProducts.as_view()),
]


router = DefaultRouter()
router.register("shops", views.ShopModelViewSet)
urlpatterns += router.urls
