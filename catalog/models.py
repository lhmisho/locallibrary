from django.db import models
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User

from datetime import date
import  uuid
# Create your models here.


class Genre(models.Model):
    """Model representing a book genre"""

    name = models.CharField(help_text='Enter a book genre (e.g. Science Fiction)', max_length=120, blank=True, null= True)

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'


class Book(models.Model):
    """ Model representing books """
    title   = models.CharField(max_length=120)
    author  = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField()
    isbn    = models.CharField('ISBN', max_length=13,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre   = models.ManyToManyField(Genre, help_text='Select a genre for this book')
    price   = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, default=None, blank=True, null=True, on_delete=models.CASCADE)
    edit_by = models.ForeignKey(User, default=None, null=True, blank=True, on_delete=models.CASCADE, related_name='editor')

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('catalog:book-detail', args=[str(self.id)])


class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
    id      = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book across whole library')
    book    = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=120)
    due_back = models.DateField(null=True, blank = True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('m','Maintenace'),
        ('o','On loan'),
        ('a','Available'),
        ('r','Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Book availability')

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned","Set a book as returned"),)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    def __str__(self):
        return f'{self.id}({self.book.title})' # '{0} ({1})'.format(self.id,self.book.title)).


class Author(models.Model):
    """Model representing an author."""
    first_name  = models.CharField(max_length=120)
    last_name   = models.CharField(max_length=120)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('catalog:author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.first_name} {self.last_name}'


class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()

    def __str__(self):
        return self.title
