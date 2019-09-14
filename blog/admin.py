from django.contrib import admin
from .models import Author, Blog, Entry, Category
# Register your models here.


admin.site.register(Author)
admin.site.register(Blog)
admin.site.register(Entry)
admin.site.register(Category)