from rest_framework import serializers

from catalog.models import Book, BookInstance, Author


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('__all__')
        # fields = ['id', 'title', 'author', 'isbn', 'summary']

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['first_name', 'last_name','date_of_birth']

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