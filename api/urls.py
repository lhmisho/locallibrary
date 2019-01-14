
from django.urls import path, include
from .views import BookListApiView, AuthorListApiView, BookViewSets
from rest_framework import routers

router = routers.DefaultRouter()
router.register('books', BookViewSets)
urlpatterns = [
    path('book/', BookListApiView.as_view()),
    path('author/', AuthorListApiView.as_view()),
    # path('book/view/', BookViewSets.as_view()),
]