from django.shortcuts import render
from rest_framework import generics, viewsets, permissions
# Create your views here.

from .serializers import BookSerializer, AuthorSerializer, AuthorHyperLinkSerializers
from catalog.models import Book, Author
from django.http import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt

class BookListApiView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class AuthorListApiView(generics.ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class BookViewSets(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookApiNew(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Book.objects.all().order_by('-id')[:1]
    serializer_class = BookSerializer

class BookApiUpdateView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class AuthorViewSetApi(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorHyperLinkSerializers

@csrf_exempt
def book(request):
    if request.method == 'GET':
        book = Book.objects.all()
        serializer = BookSerializer(book, many=True)
        return JsonResponse(serializer.data, safe=False)

    if request.method == 'POST':
        data_parser = JSONParser()
        data = data_parser.parse(request)
        serializer = BookSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def book_detail(request, id):

    try:
        instance = Book.objects.get(id=id)
    except Book.DoesNotExist as e:
        return JsonResponse({'error': 'given book instance not found'}, status=400)

    if request.method == 'GET':
        serializer = BookSerializer(instance)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data_parser = JSONParser()
        data = data_parser.parse(request)
        serializer = BookSerializer(instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        instance.delete()
        return HttpResponse(status=204)