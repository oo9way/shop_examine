from shopadmin import views
from django.urls import path
from rest_framework.routers import DefaultRouter


urlpatterns = [
    # Users
    path("users/", views.UsersListCreateView.as_view()),
    path("users/<int:pk>/", views.UserDetailUpdateDeleteView.as_view()),
    # Shops
    path("shops/<int:pk>/<str:action>/", views.ChangeShopStatusAPIView.as_view()),
    path(
        "shops/<int:shop>/add-admin/<int:user>/",
        views.AddAdminToShopAPIView.as_view(),
    ),
    path(
        "shops/<int:shop>/remove-admin/<int:user>/",
        views.RemoveAdminFromShopAPIView.as_view(),
    ),
    # Products
    path(
        "products/requests/",
        views.ProductCountRequestsListAPIView.as_view(),
    ),
    path(
        "products/requests/<int:pk>/<str:action>/",
        views.ChangeProductCountRequestAPIView.as_view(),
    ),
]


router = DefaultRouter()
router.register("shops", views.AdminShopModelViewSet)
router.register("products", views.AdminProductModelViewSet)
urlpatterns += router.urls
