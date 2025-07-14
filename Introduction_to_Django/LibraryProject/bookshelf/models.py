from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200) #with a maximum length of 200 characters.
    author = models.CharField(max_length=100) # CharField with a maximum length of 100 characters.
    publication_year = models.IntegerField() 
