from django.contrib import admin
from .models import Customer, Foods, Order, OrderFoods
# Register your models here.

admin.site.register([Customer, Foods, Order,OrderFoods])
