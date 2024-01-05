from django.db import models
from shopadmin.models import User


class Shop(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(
        max_length=255, upload_to="images/", null=True, blank=True
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shops")
    shop_admins = models.ManyToManyField(User)
    is_active = models.BooleanField(default=False)

    def activate(self):
        self.is_active = True
        self.save()
        return True

    def deactivate(self):
        self.is_active = False
        self.save()
        return True

    def add_admin(self, user):
        self.shop_admins.add(user)
        self.save()
        return True


class Product(models.Model):
    title = models.CharField(max_length=255)
    amount = models.PositiveIntegerField()
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="products")

    def __str__(self):
        return self.title

    def set_amount(self, new_amount):
        self.amount = self.amount + new_amount
        self.save()
        return True


class ChangeProductCountRequest(models.Model):
    class RequestStatus(models.TextChoices):
        INITIAL = "INITIAL", "Initial"
        ACCEPTED = "ACCEPTED", "Accepted"
        DECLINED = "DECLINED", "Declined"

    base_status = RequestStatus.INITIAL

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    new_amount = models.PositiveIntegerField()
    status = models.CharField(
        max_length=16, choices=RequestStatus.choices, default=base_status
    )

    def change_status(self, new_status):
        self.status = new_status
        self.save()
        return True
