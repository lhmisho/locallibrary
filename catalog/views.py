from django.shortcuts import render
from django.views import generic
from catalog.models import BookInstance, Book, Author,Genre
# Create your views here.


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instance = BookInstance.objects.all().count()

    num_instance_available = BookInstance.objects.filter(status__iexact='a').count() # Available books (status = 'a')
    num_author = Author.objects.all().count()  # number of author
    num_genre = Genre.objects.all().count()     # number of genre
    num_of_insensetive_books = Book.objects.filter(title__icontains='b')  # num of books in case insensitive
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books' : num_books,
        'num_instance' : num_instance,
        'num_instance_available': num_instance_available,
        'num_author' : num_author,
        'num_genre'  : num_genre,
        'num_of_insensetive_books' : num_of_insensetive_books,
        'num_visits' : num_visits,
    }

    return render(request, 'index.html', context)

class BookListView(generic.ListView):
    model = Book
    queryset = Book.objects.filter(title__icontains='book')[:5]
    template_name = 'catalog/book_list.html'
    paginate_by = 4

class BookDetialView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author
    queryset = Author.objects.all()

class AuthorDetailView(generic.DetailView):
    model = Author