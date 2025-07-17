from django.urls import path
from . import views
from .views import list_books, LibraryDetailView

urlpatterns = [
    path('', views.list_book.as_view()),
    path('list/', views.list_books),
    path('<str:title>/', views.LibraryDetailView.as_view()),
]
