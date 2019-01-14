
from django.urls import path, include
from .views import BookListApiView, AuthorListApiView, BookViewSets
from .views import BookApiNew, BookApiUpdateView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'books', BookViewSets)
urlpatterns = [
    path('book/', BookListApiView.as_view()),
    path('author/', AuthorListApiView.as_view()),
    path('book/new/', BookApiNew.as_view()),
    path('book/<int:pk>/', BookApiUpdateView.as_view()),
    # path('book/view/', BookViewSets.as_view()),
]