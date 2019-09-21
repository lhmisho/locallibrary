from rest_framework import serializers

from catalog.models import Book, BookInstance, Author, Snippet
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import exceptions

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'url')


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'price']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['first_name', 'last_name', 'date_of_birth']

    # def create(self, validated_data):
    #     pass


class AuthorHyperLinkSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = (
            'id',
            'first_name',
            'last_name',
            'date_of_birth',
            'url'
        )


class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ('id', 'title', 'code')


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get("username", "")
        password = data.get("password", "")

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    data["user"] = user
                else:
                    msg = "User is deactivated"
                    raise exceptions.ValidationError(msg)
            else:
                msg = "Unable to login with given cradentials"
                raise exceptions.ValidationError(msg)
        else:
            msg = "Must provide username and password both"
            raise exceptions.ValidationError(msg)
        return data

# class SnippetSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(required=False, allow_blank=True, max_length=100)
#     code = serializers.CharField(style={'base_template': 'textarea.html'})

#     def create(self, validated_data):
#         """
#         Create and return a new `Snippet` instance, given the validated data.
#         """
#         return Snippet.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `Snippet` instance, given the validated data.
#         """
#         instance.title = validated_data.get('title', instance.title)
#         instance.code  = validated_data.get('code', instance.code)
#         instance.save()
#         return instance
