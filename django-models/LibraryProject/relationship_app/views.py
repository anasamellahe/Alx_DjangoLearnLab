# from django.shortcuts import render, redirect
# from django.views.generic import View, ListView
# from django.views.generic.detail import DetailView
# from django.contrib.auth import login
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib import messages
# from .models import Library
# from .models import Book 
# from django.http import HttpResponse

# def list_books(request):
#     return render(request, 'relationship_app/list_books.html', {'books': Book.objects.all()})

# class list_book(ListView):
#     model = Book
#     template_name = 'relationship_app/list_books.html'
#     context_object_name = 'books'

# class LibraryDetailView(DetailView):
#     model = Library
#     template_name = 'relationship_app/library_detail.html'
#     context_object_name = 'library'
#     slug_field = 'name'
#     slug_url_kwarg = 'title'

# # Function-based register view (replaces registerAuth class)
# def register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             username = form.cleaned_data.get('username')
#             login(request, user)
#             messages.success(request, f'Account created successfully for {username}!')
#             return redirect('book_list')
#         else:
#             messages.error(request, 'Please correct the errors below.')
#     else:
#         form = UserCreationForm()
    
#     return render(request, 'relationship_app/register.html', {'form': form})


from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from .models import Book, Library

# Existing views
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

class list_book(DetailView):
    model = Book
    template_name = 'relationship_app/list_books.html'
    context_object_name = 'books'
    
    def get_queryset(self):
        return Book.objects.all()

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
    slug_field = 'name'
    slug_url_kwarg = 'title'

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('book_list')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

# Role checking functions
def is_admin(user):
    """Check if user has Admin role"""
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'Admin'

def is_librarian(user):
    """Check if user has Librarian role"""
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'Librarian'

def is_member(user):
    """Check if user has Member role"""
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'Member'

# Role-based views
@user_passes_test(is_admin, login_url='/login/')
def admin_view(request):
    """Admin view - only accessible to Admin users"""
    context = {
        'user': request.user,
        'role': request.user.profile.role,
        'message': 'Welcome to the Admin Dashboard!'
    }
    return render(request, 'relationship_app/admin_view.html', context)

@user_passes_test(is_librarian, login_url='/login/')
def librarian_view(request):
    """Librarian view - only accessible to Librarian users"""
    context = {
        'user': request.user,
        'role': request.user.profile.role,
        'message': 'Welcome to the Librarian Dashboard!',
        'books': Book.objects.all()
    }
    return render(request, 'relationship_app/librarian_view.html', context)

@user_passes_test(is_member, login_url='/login/')
def member_view(request):
    """Member view - only accessible to Member users"""
    context = {
        'user': request.user,
        'role': request.user.profile.role,
        'message': 'Welcome to the Member Dashboard!',
        'books': Book.objects.all()[:5]  # Show only 5 books for members
    }
    return render(request, 'relationship_app/member_view.html', context)


# class  loginAuth(View):

#     def get(self, request):
#         form = AuthenticationForm()
#         return render(request, 'relationship_app/login.html', {'form': form})
    
#     def post(self, request):
#         form = AuthenticationForm(request , data=request.POST)
#         if (form.is_valid()):
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return HttpResponse("hello user")
#             else:
#                 return HttpResponse("invalid user")
#         else:
#             return HttpResponse("invalid form")



# class  registerAuth(View):

#     def get(self, request):
#         form = UserCreationForm()
#         return render(request, 'relationship_app/register.html', {'form': form})
    
#     def post(self, request):
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             username = form.cleaned_data.get('username')
#             login(request, user)
#             messages.success(request, f'Account created successfully for {username}!')
#             return HttpResponse('Account created successfully for')  # Redirect to a success page
#         else:
#             messages.error(request, 'Please correct the errors below.')
#             return render(request, 'relationship_app/register.html', {'form': form})
