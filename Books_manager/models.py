from django.db import models


class AuthorsModel(models.Model):
    author = models.TextField()

    def __str__(self):
        return self.author


class BookModel(models.Model):
    title = models.CharField(max_length=256)
    published_date = models.CharField(max_length=16, help_text='(max length = 16)')
    page_count = models.SmallIntegerField(help_text='(only numbers)')
    language = models.TextField(max_length=16)
    authors = models.ManyToManyField(AuthorsModel)

    def __str__(self):
        return self.title


class IndustryIdentifiersModel(models.Model):
    book_id = models.ForeignKey(BookModel, on_delete=models.CASCADE, related_name='industry')
    industry_identifiers_type = models.CharField(max_length=64)
    industry_identifiers_id = models.CharField(max_length=64)

    def __str__(self):
        return self.industry_identifiers_type


class ImageLinksModel(models.Model):
    book_id = models.ForeignKey(BookModel, on_delete=models.CASCADE, related_name='image')
    small_thumbnail = models.CharField(max_length=256)
    thumbnail = models.CharField(max_length=256)

    def __str__(self):
        return self.thumbnail


