from django.db import models

# Create your models here.
class Question(models.Model):
    name = models.fields.CharField(max_length=100) 
    category = models.fields.CharField(max_length=50) 
    country = models.fields.CharField(max_length=50) 
    question = models.fields.CharField(max_length=200)
    def __str__(self):
        return self.question