from django.shortcuts import render
from rest_framework import generics, viewsets
# Create your views here.

from .serializers import BookSerializer, AuthorSerializer
from catalog.models import Book, Author


class BookListApiView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class AuthorListApiView(generics.ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class BookViewSets(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer