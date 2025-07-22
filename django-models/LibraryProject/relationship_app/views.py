from django.shortcuts import render, redirect
from django.views.generic import View, ListView 
from django.views.generic.detail import DetailView
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from .models import Library
from .models import Book 
from django.http import HttpResponse



def list_books(request):
    return render(request, 'relationship_app/list_books.html', {'books':Book.objects.all()})

class list_book(ListView):
    model = Book
    template_name = 'relationship_app/list_books.html'
    context_object_name = 'books'

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
    slug_field = 'name'
    slug_url_kwarg = 'title'



class  loginAuth(View):

    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'relationship_app/login.html', {'form': form})
    
    def post(self, request):
        form = AuthenticationForm(request , data=request.POST)
        if (form.is_valid()):
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponse("hello user")
            else:
                return HttpResponse("invalid user")
        else:
            return HttpResponse("invalid form")

class logoutAuth(View):

    def get(self, request):
        return render(request, 'relationship_app/logout.html', {})
    def post(self, request):
        logout(request)
        return render(request, 'relationship_app/logout.html', {})
  


class  registerAuth(View):

    def get(self, request):
        form = UserCreationForm()
        return render(request, 'relationship_app/register.html', {'form': form})
    
    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            login(request, user)
            messages.success(request, f'Account created successfully for {username}!')
            return HttpResponse('Account created successfully for')  # Redirect to a success page
        else:
            messages.error(request, 'Please correct the errors below.')
            return render(request, 'relationship_app/register.html', {'form': form})


