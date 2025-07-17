from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_book.as_view()),
    path('list/', views.list_books),
    path('<str:title>/', views.library_detail.as_view()),
]
