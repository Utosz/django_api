from django.db import models


class BookModel(models.Model):
    title = models.CharField(max_length=64)
    published_date = models.SmallIntegerField()
    page_count = models.SmallIntegerField()
    language = models.TextField()


class IndustryIdentifiersModel(models.Model):
    book_id = models.ForeignKey(BookModel, on_delete=models.CASCADE, related_name='industry')
    industry_identifiers_type = models.CharField(max_length=16)
    industry_identifiers_id = models.IntegerField()


class ImageLinksModel(models.Model):
    book_id = models.ForeignKey(BookModel, on_delete=models.CASCADE, related_name='image')
    small_thumbnail = models.CharField(max_length=128)
    thumbnail = models.CharField(max_length=128)


class AuthorsModel(models.Model):
    author = models.TextField()
    authors = models.ManyToManyField(BookModel)
