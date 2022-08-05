from xml.parsers.expat import model
from django.db import models

# Create your models here.
class Customer(models.Model):
    customer_username = models.CharField(max_length=254)
    customer_name_surname = models.CharField(max_length=128)
    customer_email = models.EmailField(max_length=254)
    customer_password = models.CharField(max_length=120)

    def __str__(self) -> str:
        return self.customer_email

class Foods(models.Model):
    food_name = models.CharField(max_length=128)
    food_description = models.CharField(max_length=512)
    food_price = models.FloatField()

    def __str__(self) -> str:
        return self.food_name

class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Delivery is taken', 'Delivery is taken'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
        )
    customer_id = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    order_recieved_date = models.DateTimeField()
    order_status = models.CharField(max_length=64, choices=STATUS)

class OrderFoods(models.Model):
    order_id = models.ForeignKey(Order,on_delete=models.CASCADE)
    food_id = models.ForeignKey(Foods,on_delete=models.DO_NOTHING)