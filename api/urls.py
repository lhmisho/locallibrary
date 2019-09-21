
from django.urls import path, include
from .views import BookListApiView, AuthorListApiView, BookViewSets
from .views import (BookApiNew, BookApiUpdateView, AuthorViewSetApi, book, book_detail,
                    BookApiView,snippet_detail, BookDetailView, UserViewSet, author, LoginView, LogoutView)
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'books', BookViewSets)
router.register('author_api', AuthorViewSetApi)
router.register('users', UserViewSet)

urlpatterns = [
    path('book/', BookListApiView.as_view()),
    path('book/<int:id>/', BookListApiView.as_view()),
    # path('books_func/', book),
    path('books_func/<int:id>/', BookDetailView.as_view()),
    path('books_func/', BookApiView.as_view()),
    path('books_func/<int:id>/', book_detail),
    # path('author/', AuthorListApiView.as_view()),
    # path('author/', author),
    path('book/new/', BookApiNew.as_view()),
    path('book/<int:pk>/', BookApiUpdateView.as_view()),
    path('snippet/<int:pk>/', snippet_detail),
    # path('rest-auth/', include('rest_auth.urls')),
    path('auth/login/', LoginView.as_view()),
    path('auth/logout/', LogoutView.as_view()),
    path(r'rest-auth/registration/', include('rest_auth.registration.urls')),
    # path('book/view/', BookViewSets.as_view()),

    path('', include(router.urls)),
]