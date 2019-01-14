from django.db import models

# Create your models here.

class Blog(models.Model):
    name = models.CharField(max_length=120)
    tagline = models.TextField()

    def __str__(self):
        return self.name



class Author(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)


    def __str__(self):
        return self.name


class Entry(models.Model):
    blog        = models.ForeignKey(Blog, on_delete=models.CASCADE)
    headline    = models.CharField(max_length=255)
    body_text   = models.TextField()
    pub_date    = models.DateField()
    mod_date    = models.DateField()
    authors     = models.ManyToManyField(Author)
    n_comment   = models.IntegerField()
    n_pingbacks = models.IntegerField()
    ratings     = models.IntegerField()

    def __str__(self):
        return self.headline


class ThemeBlog(Blog):
    theme = models.CharField(max_length=120)