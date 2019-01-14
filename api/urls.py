
from django.urls import path, include
from .views import BookListApiView, AuthorListApiView

urlpatterns = [
    path('book/', BookListApiView.as_view()),
    path('author/', AuthorListApiView.as_view()),
]