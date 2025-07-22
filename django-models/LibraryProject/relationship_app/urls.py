from django.urls import path
from . import views
from .views import list_books, LibraryDetailView, list_book, loginAuth, logoutAuth, registerAuth


urlpatterns = [
    path('', list_book.as_view()),
    path('list/', list_books),
    path('login/', loginAuth.as_view(), name='login'),
    path('logout/', logoutAuth.as_view(), name='logout'),
    path('register/', registerAuth.as_view(), name='register'),
    path('<str:title>/', LibraryDetailView.as_view()),
]

