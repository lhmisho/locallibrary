"""locallibrary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views


app_name = 'catalog'

urlpatterns = [
    #Index
    path('', views.index, name='index'),
    #Books
    path('books/', views.BookListView.as_view(), name='book'),
    path('books/create/', views.BookCreateView.as_view(), name='book-create'),
    path('books/<int:pk>', views.BookDetialView.as_view(), name='book-detail'),
    path('books/<int:pk>/edit/', views.BookUpdateView.as_view(), name='book-edit'),
    path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book-delete'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('allbooks/', views.LoanedBooksByAdminListview.as_view(), name='all-borrowed'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
    #Author
    path('authors/', views.AuthorListView.as_view(), name='author'),
    path('authors/create/', views.AuthorCreateView.as_view(), name='author-create'),
    path('author/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    path('authors/<int:pk>/update/', views.AuthorUpdateView.as_view(), name='author-update'),
    path('authors/<int:pk>/delete/', views.AuthorDeleteView.as_view(), name='author-delete'),
    # path('book/<uuid:pk>/renew-model-form/', views.RegisterView, name='renew-modelform-book-librarian'),
    
]