import requests
#from Books_manager.models import BookModel


def is_num(data):
    try:
        int(data)
        return True
    except ValueError:
        return False


def data_gather(i, dictionary):
    temp = requests.POST.get(f'{i}')
    if temp:
        dictionary[f'{i}'] = temp
        return dictionary[f'{i}']


def connect(param):
    googleapikey = "AIzaSyBs6O9832V7DdVDyoLiRWqmBQw7KDN7qN0"
    parms = {"q": param, "key": googleapikey}
    r = requests.get(url="https://www.googleapis.com/books/v1/volumes", params=parms)
    return r


def parse_n_find(r, ):
    rj = r.json()
    dict_r = dict(rj)
    results = [i[key] for i in dict_r['items'] for key in i if key == 'volumeInfo']
    return results


find_keys = ['title', 'authors', 'publishedDate', 'industryIdentifiers', 'pageCount', 'imageLinks', 'language']
create_book = [find_keys[0], find_keys[2], find_keys[4], find_keys[6]]


def get_data(parsed_list, find_key):
    counter = 0
    d_result = {}
    for dictionary in parsed_list:
        counter += 1
        d_result[counter] = {key: dictionary[key] for key in dictionary if key in find_key}
        print(str(counter) + " " + str(d_result[counter]))
    return d_result


d_result = {1: {'title': 'Wieża Jaskółki', 'authors': ['Andrzej Sapkowski'], 'publishedDate': '1997',
                'industryIdentifiers': [{'type': 'ISBN_10', 'identifier': '8370541240'},
                                        {'type': 'ISBN_13', 'identifier': '9788370541248'}], 'pageCount': 428,
                'imageLinks': {
                    'smallThumbnail': 'http://books.google.com/books/content?id=YFhhAAAAMAAJ&printsec=frontcover&img=1&zoom=5&source=gbs_api',
                    'thumbnail': 'http://books.google.com/books/content?id=YFhhAAAAMAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api'},
                'language': 'pl'},
            2: {'title': 'Video Games Around the World', 'authors': ['Mark J. P. Wolf', 'Toru Iwatani'],
                'publishedDate': '2015-05-15',
                'industryIdentifiers': [{'type': 'ISBN_13', 'identifier': '9780262527163'},
                                        {'type': 'ISBN_10', 'identifier': '0262527162'}], 'pageCount': 720,
                'imageLinks': {
                    'smallThumbnail': 'http://books.google.com/books/content?id=pZb5CAAAQBAJ&printsec=frontcover&img=1&zoom=5&edge=curl&source=gbs_api',
                    'thumbnail': 'http://books.google.com/books/content?id=pZb5CAAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api'},
                'language': 'en'}
            }


# def get_n_create(d_result):
#     for num_key, value in d_result.items():
#         authors_list = []
#         industry_list = []
#         book_dict = {key: value[key] for key in value if key in create_book}
#         new_book = BookModel.objects.create(**book_dict)
#         [authors_list.extend(value[key]) for key in value if key =='authors']
#         for author in authors_list:
#             new_author = AuthorsModel.objects.get_or_create(author=author)
#             new_book.authors.add(new_author[0])
#         [industry_list.extend(value[key]) for key in value if key == 'industryIdentifiers']
#         for industry in industry_list:
#             new_industries = IndustryIdentifiersModel.objects.create(industry_identifiers_type=industry['type'],industry_identifiers_id['identifier'], book_id=new_book)
#         for key in value:
#             if key == 'imageLinks':
#                 new_links = ImageLinksModel.objects.create(**value[key], book_id=new_book)


# print(get_n_create(d_result))
