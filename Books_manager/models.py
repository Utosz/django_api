from django.db import models


class AuthorsModel(models.Model):
    author = models.TextField()

    def __str__(self):
        return self.author


class BookModel(models.Model):
    title = models.CharField(max_length=256, verbose_name='Title')
    published_date = models.CharField(max_length=16, verbose_name='Date of publication', help_text='(max length 16')
    page_count = models.SmallIntegerField(verbose_name='Amount of pages', help_text='(only numbers)')
    language = models.TextField(max_length=16, verbose_name='Language')
    authors = models.ManyToManyField(AuthorsModel, verbose_name='Authors')

    def __str__(self):
        return self.title


class IndustryIdentifiersModel(models.Model):
    book_id = models.ForeignKey(BookModel, on_delete=models.CASCADE, related_name='industry', verbose_name='Book id')
    industry_identifiers_type = models.CharField(max_length=64, verbose_name='Industry id type')
    industry_identifiers_id = models.CharField(max_length=64, verbose_name='Industry id')

    def __str__(self):
        return self.industry_identifiers_type


class ImageLinksModel(models.Model):
    book_id = models.ForeignKey(BookModel, on_delete=models.CASCADE, related_name='image', verbose_name='Book id')
    small_thumbnail = models.CharField(max_length=256, verbose_name='Link to small thumbnail')
    thumbnail = models.CharField(max_length=256, verbose_name='Link to large thumbnail')

    def __str__(self):
        return self.thumbnail


