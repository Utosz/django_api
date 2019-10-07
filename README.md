# books_api

books_api is a recruitment task executed with Django and PostgreSQL (also perfect exercise)

## Version

This is early version which still need a lot of testing and probably  contains a lot of bugs\
Known issues:
- range on REST API View still isn't implemented
- REST API lacks of data from related models
- forms are Unicode sensitive
- queries uses 'contains' only


## List of features and views:
- importing desired titles from Google Books APIs via chosen keywords
- searching and filtering via titles, authors language and in range of publication dates
- adding new books to db via forms
- REST Api allows to get data in JSON format


### List of current views:

```python
    path('admin/', admin.site.urls),
    re_path(r'^list/', BooksView.as_view()),
    re_path(r'^add/', AddBooksView.as_view()),
    re_path(r'^find/', ImportBookView.as_view()),
    re_path(r'api/', RestApiBookView.as_view()),
```



## To do:
- REST Api view need range filters
- Unit tests have to be added!
- More advanced filters should be implemented
- DRY - some chunks of code need to be enclosed in functions
- optimization - lot of operation can be simplified
- Frontend
## Future
App will be treated as experimental area and constantly developed with new features and improvements
