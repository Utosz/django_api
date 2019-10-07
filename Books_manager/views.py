from django.shortcuts import render
from django.http import HttpResponse
from Books_manager.models import BookModel, AuthorsModel, IndustryIdentifiersModel, ImageLinksModel
from Books_manager import additional_functions as addons
from django.views import View
from .forms import SearchBookForm, AddBookForm, AddImageLinksForm, AddIndustryIdentifiersForm, FindGoogleBook


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
            query_dict = {}
            title = forms.cleaned_data.get('title')
            query_dict['title__icontains'] = title
            author = forms.cleaned_data.get('authors')
            if author:
                authors_query = AuthorsModel.objects.filter(author__icontains=author).all()
                if authors_query:
                    query_dict['authors'] = authors_query[0]
            language = forms.cleaned_data.get('language')
            query_dict['language__icontains'] = language
            published_date = forms.cleaned_data.get('published_date')
            query_dict['published_date__icontains'] = published_date
            cleaned_dict = {key: query_dict[key] for key in query_dict if
                            query_dict[key] is not None and query_dict[key] != ''}
            all_books_query = BookModel.objects.filter(**cleaned_dict).all()
            if not all_books_query or not (title or author or language or published_date):
                return render(request, 'fail.html')
            all_books = {'all_books': all_books_query,
                         'forms': forms,
                         # 'a': authors_query,
                         'q': cleaned_dict,
                         'au': author}
            return render(request, 'list.html', all_books)


class AddBooksView(View):

    def get(self, request):
        # all_books_query = BookModel.objects.all()
        forms_book = AddBookForm()
        forms_industry = AddIndustryIdentifiersForm()
        forms_image = AddImageLinksForm()
        all_books = {  # 'all_books': all_books_query,
            'forms_book': forms_book,
            'forms_industry': forms_industry,
            'forms_image': forms_image
        }
        return render(request, 'add.html', all_books)

    def post(self, request):
        forms_book = AddBookForm(request.POST)
        forms_industry = AddIndustryIdentifiersForm(request.POST)
        forms_image = AddImageLinksForm(request.POST)
        if forms_book.is_valid():
            query_dict = {}
            industry_dict = {}
            image_dict = {}
            title = forms_book.cleaned_data.get('title')
            query_dict['title'] = title
            page_count = forms_book.cleaned_data.get('page_count')
            query_dict['page_count'] = page_count
            language = forms_book.cleaned_data.get('language')
            query_dict['language'] = language
            published_date = forms_book.cleaned_data.get('published_date')
            query_dict['published_date'] = published_date
            cleaned_dict = {key: query_dict[key] for key in query_dict if
                            query_dict[key] is not None and query_dict[key] != ''}

            new_book = BookModel.objects.create(**cleaned_dict)
            author = forms_book.cleaned_data.get('authors')
            new_author = AuthorsModel.objects.get_or_create(author=author)
            new_book.authors.add(new_author[0])
            authors_query = AuthorsModel.objects.filter(author=author).values_list('pk', flat=True)
            if authors_query:
                query_dict['authors'] = authors_query[0]
        if forms_industry.is_valid():
            industry_identifiers_type = forms_industry.cleaned_data.get('industry_identifiers_type')
            industry_dict['industry_identifiers_type'] = industry_identifiers_type
            industry_identifiers_id = forms_industry.cleaned_data.get('industry_identifiers_id')
            industry_dict['industry_identifiers_id'] = industry_identifiers_id
            new_industries = IndustryIdentifiersModel.objects.create(**industry_dict, book_id=new_book)
        if forms_image.is_valid():
            small_thumbnail = forms_image.cleaned_data.get('small_thumbnail')
            image_dict['small_thumbnail'] = small_thumbnail
            thumbnail = forms_image.cleaned_data.get('thumbnail')
            image_dict['thumbnail'] = thumbnail
            new_links = ImageLinksModel.objects.create(**image_dict, book_id=new_book)

            all_books_query = BookModel.objects.filter(**cleaned_dict).all()
            all_books = {
                'add_book': all_books_query,
            }
            return render(request, 'success.html', all_books)


class ImportBookView(View):
    """
    stwórz widok który pozwoli na import książek według słów kluczowych z API: https://developers.google.com/books/docs/v1/using#WorkingVolumes
wpisy tych książek muszą znaleźć się w bazie danych która została stworzona w pierwszej części tego zadania
    """

    def get(self, request):
        forms = FindGoogleBook()
        all_books = {
            'forms': forms
        }
        return render(request, 'find.html', all_books)

    def post(self, request):
        forms = FindGoogleBook(request.POST)
        find_keys = ['title', 'authors', 'publishedDate', 'industryIdentifiers', 'pageCount', 'imageLinks', 'language']
        create_book = [find_keys[0], find_keys[2], find_keys[4], find_keys[6]]

        if forms.is_valid():
            search = ''
            keyword = forms.cleaned_data.get('keyword')
            search += str(keyword)
            areas = forms.cleaned_data.get('areas')
            search += f'+{str(areas)}'
            r = addons.connect(search)
            search_result = addons.parse_n_find(r)
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
            all_books = {
                'imported': result
            }
            return render(request, 'import.html', all_books)
