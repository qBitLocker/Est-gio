from django.db import models
from django.utils import timezone
import datetime

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
    
# Classes do tutorial da documentação
class Question (models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return self.question_text
    
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text