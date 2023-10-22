from django.db import models
from datetime import date
from django.contrib.auth.models import User

# Create your models here.
class Booking(models.Model):
    first_name = models.CharField(max_length=200)
    reservation_date = models.DateField(default=date.today)
    reservation_slot = models.SmallIntegerField(default=10)

    def __str__(self):
        return self.first_name


# Add code to create Menu model
class Menu(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Decimal field for accurate monetary values
    menu_item_description = models.TextField(max_length=1000, default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Menu Items"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    is_ordered = models.BooleanField(default=False)  # Indicates if the cart has been converted into an order
    order_date = models.DateTimeField(null=True, blank=True)  # Date and time when the order was placed

    def __str__(self):
        return f"{self.user.username}'s Cart Item: {self.menu_item.name}"



