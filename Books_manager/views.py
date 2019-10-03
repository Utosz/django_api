from django.shortcuts import render
from django.http import HttpResponse


def books_list():
    """
    widok spis (lista) książek - z możliwością wyszukiwania po `title`, `authors` i `language` oraz zakresie `publishedDate`, lista ma zawierać wszystkie informacje z modelu
    """
    answer = """
             <html>
              <body>
               <p>List of books</p>
              </body>
             </html>
             """
    return HttpResponse(answer)


def add_book():
    """
    widok z formularzem pozwalający na ręczne dodawanie książek
    """
    answer = """
             <html>
              <body>
               <p>Add a book</p>
              </body>
             </html>
             """
    return HttpResponse(answer)


def import_book():
    """
    stwórz widok który pozwoli na import książek według słów kluczowych z API: https://developers.google.com/books/docs/v1/using#WorkingVolumes
wpisy tych książek muszą znaleźć się w bazie danych która została stworzona w pierwszej części tego zadania
    """
    answer = """
             <html>
              <body>
               <p>Find book to import</p>
              </body>
             </html>
             """
    return HttpResponse(answer)
