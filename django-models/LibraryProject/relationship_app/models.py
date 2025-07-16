from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=30)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='Authors')
    def __str__(self):
        return self.title

class Library(models.Model):
    name =  models.CharField(max_length=30)
    books = models.ManyToManyField(Book)
    def __str__(self):
        return self.name

class Librarian(models.Model):
    name =  models.CharField(max_length=30)
    Library = models.OneToOneField(Library,  on_delete=models.CASCADE,  related_name='library')
    def __str__(self):
        return self.name
# Create your models here.




