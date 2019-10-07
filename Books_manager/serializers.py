from rest_framework import serializers
from Books_manager.models import BookModel


class BookModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookModel
        fields = ['title', 'published_date', 'language', 'authors']
