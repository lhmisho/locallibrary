import datetime

from django.contrib.auth.decorators import (permission_required,
                                            user_passes_test)
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.generic import edit as editViews

from catalog.models import Author, Book, BookInstance, Genre

from .forms import RenewBookModelForm, RenueBooksForm

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


# class RegisterView(editViews.FormView):
#
#     form_class = RenewBookModelForm
#     template_name= 'catalog/book_renew_librarian.html'
#
#     def get_context_data(self, pk, **kwargs):
#         context = super(RegisterView, self).get_context_data(**kwargs)
#         import pdb;pdb.set_trace()
#         context['book_instance'] = BookInstance.objects.filter(id=pk)
#         return context
#
#     def form_valid(self, form):
#         request = self.request
#         form.save()
#         return render(self.request, 'register/thank_you.html')


class AuthorCreateView(editViews.CreateView):
    model = Author
    fields = '__all__'
    initial = { 'date_of_death' : '05/01/2018' }

class AuthorUpdateView(editViews.UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death', ]

class AuthorDeleteView(editViews.DeleteView):
    model = Author
    success_url = reverse_lazy('catalog:author')




