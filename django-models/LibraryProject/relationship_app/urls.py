from django.urls import path
from . import views
from .views import list_books, LibraryDetailView, list_book, loginAuth, logoutAuth, registerAuth


# template_name = 'relationship_app/list_books.html'

urlpatterns = [
    path('', list_book.as_view()),
    path('list/', list_books),
    path('login/', loginAuth.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', logoutAuth.as_view(), name='logout'),
    path('register/', registerAuth.as_view(template_name='relationship_app/register.html'), name='register'),
    path('<str:title>/', LibraryDetailView.as_view()),
]

# template_name='relationship_app/register.html'

# template_name='relationship_app/logout.html'