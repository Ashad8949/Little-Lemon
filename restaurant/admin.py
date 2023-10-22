from django.contrib import admin
from .models import Menu, Booking, Cart
# Register your models here.
admin.site.register(Booking)
admin.site.register(Menu)
admin.site.register(Cart)