from django.contrib import admin
from shop.models import Shop, ChangeProductCountRequest, Product

# Register your models here.
admin.site.register([Shop, ChangeProductCountRequest, Product])
