# from django.urls import path
# from django.contrib.auth.views import LoginView, LogoutView
# from . import views
# from .views import list_books, LibraryDetailView, list_book

# urlpatterns = [
#     path('', list_book.as_view(), name='book_list'),
#     path('list/', list_books, name='book_list_func'),
#     path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
#     path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
#     path('register/', views.register, name='register'),
#     path('<str:title>/', LibraryDetailView.as_view(), name='library_detail'),
# ]


from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import list_books, LibraryDetailView, list_book

urlpatterns = [
    path('', list_book.as_view(), name='book_list'),
    path('list/', list_books, name='book_list_func'),
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('<str:title>/', LibraryDetailView.as_view(), name='library_detail'),
    
    # Role-based view URLs
    path('admin/', views.admin_view, name='admin_view'),
    path('librarian/', views.librarian_view, name='librarian_view'),
    path('member/', views.member_view, name='member_view'),
    
    # Book management URLs
    path('books/', views.list_books, name='book_list'),
    path('library/<str:title>/', views.LibraryDetailView.as_view(), name='library_detail'),
]