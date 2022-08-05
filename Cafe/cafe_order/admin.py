from django.contrib import admin
from .models import Customer, Foods
# Register your models here.

admin.site.register([Customer, Foods])
