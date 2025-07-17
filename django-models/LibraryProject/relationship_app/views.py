from django.shortcuts import render
from django.views.generic import View, ListView 
from django.views.generic.detail import DeleteView
from .models import Library
from .models import Book 
from django.http import HttpResponse



def list_books(request):
    return render(request, 'relationship_app/list_books.html', {'books':Book.objects.all()})

class list_book(ListView):
    model = Book
    template_name = 'relationship_app/list_books.html'
    context_object_name = 'books'

class library_detail(DeleteView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
    slug_field = 'name'
    slug_url_kwarg = 'title'

# Create your views here.

