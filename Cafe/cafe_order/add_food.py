from models import Foods

hamburger = models.Foods(food_name = 'Hamburger',food_description = "Delicious Hamburger with caremalized onion",food_price = 20.99)

pizza = models.Foods(food_name = 'Pizza',food_description = "The pizza makes you happy",food_price = 30.99)

hamburger.save()
pizza.save()