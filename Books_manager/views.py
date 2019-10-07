from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from Books_manager.models import BookModel, AuthorsModel, IndustryIdentifiersModel, ImageLinksModel
from Books_manager import additional_functions as addons
from django.views import View
from .forms import SearchBookForm, AddBookForm, AddImageLinksForm, AddIndustryIdentifiersForm, FindGoogleBook
from .serializers import BookModelSerializer


class BooksView(View):

    def get(self, request):
        all_books_query = BookModel.objects.all()
        forms = SearchBookForm()
        all_books = {'all_books': all_books_query,
                     'forms': forms}
        return render(request, 'list.html', all_books)

    def post(self, request):
        forms = SearchBookForm(request.POST)
        if forms.is_valid():
            query_dict = {'title__icontains': forms.cleaned_data.get('title'),
                          'authors__author__icontains': forms.cleaned_data.get('authors'),
                          'language__icontains': forms.cleaned_data.get('language'),
                          }
            published_date = forms.cleaned_data.get('published_date')
            if published_date:
                published_date = published_date.split(',')
                if len(published_date) > 1:
                    published_date = published_date[0:2]
                    published_date.sort()
                    query_dict['published_date__gte'] = published_date[0].strip()
                    query_dict['published_date__lte'] = published_date[1].strip()
                else:
                    query_dict['published_date__icontains'] = published_date[0].strip()
            cleaned_dict = {key: query_dict[key] for key in query_dict if
                            query_dict[key] is not None and query_dict[key] != ''}
            all_books_query = BookModel.objects.filter(**cleaned_dict).all()
            if not all_books_query or not (query_dict or published_date):
                return render(request, 'fail.html')
            return render(request, 'list.html', {'all_books': all_books_query, 'forms': forms})


class AddBooksView(View):

    def get(self, request):
        forms_book = AddBookForm()
        forms_industry = AddIndustryIdentifiersForm()
        forms_image = AddImageLinksForm()
        return render(request, 'add.html',
                      {'forms_book': forms_book, 'forms_industry': forms_industry, 'forms_image': forms_image})

    def post(self, request):
        forms_book = AddBookForm(request.POST)
        forms_industry = AddIndustryIdentifiersForm(request.POST)
        forms_image = AddImageLinksForm(request.POST)
        if forms_book.is_valid() and forms_industry.is_valid() and forms_image.is_valid():
            query_dict = {
                'title': forms_book.cleaned_data.get('title'),
                'page_count': forms_book.cleaned_data.get('page_count'),
                'language': forms_book.cleaned_data.get('language'),
                'published_date': forms_book.cleaned_data.get('published_date'),
            }
            new_book = BookModel.objects.create(**query_dict)
            author = forms_book.cleaned_data.get('authors')
            new_author = AuthorsModel.objects.get_or_create(author=author)
            new_book.authors.add(new_author[0])
            query_dict['authors__author'] = AuthorsModel.objects.filter(author=author).values_list('pk', flat=True)[0]
            industry_dict = {
                'industry_identifiers_type': forms_industry.cleaned_data.get('industry_identifiers_type'),
                'industry_identifiers_id': forms_industry.cleaned_data.get('industry_identifiers_id')
            }
            new_industries = IndustryIdentifiersModel.objects.create(**industry_dict, book_id=new_book)
            image_dict = {
                'small_thumbnail': forms_image.cleaned_data.get('small_thumbnail'),
                'thumbnail': forms_image.cleaned_data.get('thumbnail')
            }
            new_links = ImageLinksModel.objects.create(**image_dict, book_id=new_book)
            all_books_query = BookModel.objects.filter(**query_dict).all()
            return render(request, 'success.html', {'add_book': all_books_query})


class ImportBookView(View):

    def get(self, request):
        forms = FindGoogleBook()
        return render(request, 'find.html', {'forms': forms})

    def post(self, request):
        forms = FindGoogleBook(request.POST)
        find_keys = ['title', 'authors', 'publishedDate', 'industryIdentifiers', 'pageCount', 'imageLinks', 'language']
        create_book = [find_keys[0], find_keys[2], find_keys[4], find_keys[6]]

        if forms.is_valid():
            search = f"{str(forms.cleaned_data.get('keyword'))}+{str(forms.cleaned_data.get('areas'))}"
            r = addons.connect(search)
            if not r:
                return render(request, 'cn_problem.html')
            search_result = addons.parse_n_find(r)
            if not search_result:
                return render(request, 'no_results.html')
            result = addons.get_data(search_result, find_keys)

            # create objects in db
            for num_key, value in result.items():
                authors_list = []
                industry_list = []
                book_dict = {key: value[key] for key in value if key in create_book}
                if 'title' not in book_dict:
                    book_dict['title'] = 'None'
                if 'publishedDate' not in book_dict:
                    book_dict['publishedDate'] = 'None'
                if 'pageCount' not in book_dict:
                    book_dict['pageCount'] = 0
                if 'language' not in book_dict:
                    book_dict['language'] = 'None'
                new_book = BookModel.objects.create(title=book_dict['title'],
                                                    published_date=book_dict['publishedDate'],
                                                    page_count=book_dict['pageCount'], language=book_dict['language'])
                [authors_list.extend(value[key]) for key in value if key == 'authors']
                for author in authors_list:
                    new_author = AuthorsModel.objects.get_or_create(author=author)
                    new_book.authors.add(new_author[0])
                [industry_list.extend(value[key]) for key in value if key == 'industryIdentifiers']
                for industry in industry_list:
                    new_industries = IndustryIdentifiersModel.objects.create(industry_identifiers_type=industry['type'],
                                                                             industry_identifiers_id=industry[
                                                                                 'identifier'],
                                                                             book_id=new_book)
                for key in value:
                    if key == 'imageLinks':
                        new_links = ImageLinksModel.objects.create(thumbnail=value[key]['thumbnail'],
                                                                   small_thumbnail=value[key]['smallThumbnail'],
                                                                   book_id=new_book)

            return render(request, 'import.html',{'imported': result})


class RestApiBookView(generics.ListAPIView):
    queryset = BookModel.objects.all()
    serializer_class = BookModelSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'authors', 'language', 'published_date']
