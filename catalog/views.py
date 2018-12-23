import datetime

from django.shortcuts import render
from django.views import generic
from catalog.models import BookInstance, Book, Author,Genre
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import permission_required
from .forms import RenueBooksForm
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


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    Model = BookInstance
    template_name = 'catalog/bookinstance_borrowed_list_user_view.html'
    paginate_by = 2

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class MyPermissionView(PermissionRequiredMixin):
    permission_required = 'catalog.can_mark_returned'

@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class LoanedBooksByAdminListview(generic.ListView):
    """ Generic class-based view listing books on loan to current user """
    Model = BookInstance
    template_name   = 'catalog/bookinstance_borrowed_list_user_view.html'
    # paginate_by     = 4

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


# def renew_book_librarian(request, pk):
#     book_instance = get_list_or_404(BookInstance, pk=pk)
#
#     # If this is a POST request then process the Form data
#     if request.method == 'POST':
#         form = RenueBooksForm(request.POST)
#
#         if form.is_valid():
#             book_instance.due_back = form.cleaned_data['renewal_date']
#             book_instance.save()
#
#             return HttpResponseRedirect(reverse('catalog:all-borrowed'))
#
#     else:
#         proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
#         form = RenueBooksForm(initial={'renewal_date' : proposed_renewal_date })
#
#
#     context = {
#         'form' : form,
#         'book_instance' : book_instance
#     }
#
#     return render(request, 'catalog/book_renew_librarian.html', context)

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)
    if request.method == 'POST':
        form = RenueBooksForm(request.POST)

        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()
            return HttpResponseRedirect(reverse('catalog:all-borrowed'))

    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenueBooksForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form' : form,
        'book_instance' : book_instance
    }
    return render(request, 'catalog/book_renew_librarian.html', context)



