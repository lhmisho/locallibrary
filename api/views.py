from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from rest_framework import generics, permissions, viewsets
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics

from catalog.models import Author, Book, Snippet

from .serializers import (AuthorHyperLinkSerializers, AuthorSerializer,
                          BookSerializer, SnippetSerializer, UserSerializer)
from django.contrib.auth.models import User


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class BookApiView(APIView):
    def get(self, request):
        book = Book.objects.all()
        serializer = BookSerializer(book, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        data = request.data
        serializer = BookSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

class BookDetailView(APIView):
    def get_object(self, id):
        try:
            return Book.objects.get(id=id)
        except Book.DoesNotExist as e:
            return Response({'error': 'given book instance not found'}, status=400)

    def get(self, request, id=None):
        instance = self.get_object(id)
        serializer = BookSerializer(instance)
        return Response(serializer.data)

    def put(self, request, id=None):
        instance = self.get_object(id)
        data = request.data
        serializer = BookSerializer(instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def delete(self, request, id=None):
        instance = self.get_object(id)
        instance.delete()
        return HttpResponse(status=204)

class BookListApiView(generics.GenericAPIView, 
            mixins.ListModelMixin, mixins.CreateModelMixin, 
            mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    lookup_field = 'id'

    def get(self, request, id=None):
        if id:
            return self.retrieve(request, id)
        else:
            return self.list(request)

    def post(self, request):
        return self.create(request)

    def perform_create(self, serializer):
        serializer.save()

    def put(self, request, id=None):
        return self.update(request, id)
    
    def perform_update(self, serializer):
        return serializer.save()

    def delete(self, request, id=None):
        return self.destroy(request, id)

# class BookListApiView(generics.ListAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer

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


@csrf_exempt
def snippet_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializers = SnippetSerializer(snippets, many=True)
        return JsonResponse(serializers, safe=False)
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializers = SnippetSerializer(data=data)
        if serializers.is_valid():
            serializers.save()
            return JsonResponse(serializers.data, status=200)
        return JsonResponse(serializers.errors, status = 400)


@csrf_exempt
def snippet_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)








