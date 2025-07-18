from django.urls import path
from . import views
from .views import list_books, LibraryDetailView

urlpatterns = [
    path('', views.list_book.as_view()),
    path('list/', views.list_books),
    path('login/', views.loginAuth, name='login'),
    path('logout/', views.logoutAuth, name='logout'),
    path('register/', views.registerAuth, name='register'),
    path('<str:title>/', views.LibraryDetailView.as_view()),
]
