from django.db import models

# Passos
# Altere models (in models.py).

# Rode python manage.py makemigrations para criar a migração para as alerações

# Rode python manage.py migrate para aplicar as algerações no banco de dados

# Create your models here.
class Product(models.Model):
    # Variáveis representam o campo de banco de dados no model
    description = models.CharField(max_length=200)
    price = models.FloatField()

    def __str__ (self):
        return "Descr: {}\nPrice: R$ {}".format(self.description, self.price)
    

'''class User(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)'''
    