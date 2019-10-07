from django import forms
from Books_manager import choices


class SearchBookForm(forms.Form):
    title = forms.CharField(max_length=64, label='Title', required=False,
                            help_text='(unresolved issues: unicode sensitive)')
    published_date = forms.CharField(label='Date of publication',
                                     help_text='(to get range, use pattern "data,data" ex.2000,2006)',
                                     required=False)
    language = forms.CharField(max_length=16, label='Language', required=False)
    authors = forms.CharField(label='Authors', required=False, help_text='(unresolved issues: unicode sensitive)')


class AddBookForm(forms.Form):
    title = forms.CharField(max_length=64, label='Title', required=True)
    published_date = forms.CharField(label='Date of publication', help_text='', required=True)
    page_count = forms.IntegerField(label='Amount of pages', required=True)
    language = forms.CharField(max_length=16, label='Language', required=True)
    authors = forms.CharField(label='Authors', required=True)


class AddIndustryIdentifiersForm(forms.Form):
    industry_identifiers_type = forms.CharField(max_length=32, label='Industry id type', required=True)
    industry_identifiers_id = forms.CharField(max_length=32, label='Industry id', required=True)


class AddImageLinksForm(forms.Form):
    small_thumbnail = forms.CharField(max_length=256, label='Link to small thumbnail', required=True)
    thumbnail = forms.CharField(max_length=256, label='Link to large thumbnail', required=True)


class FindGoogleBook(forms.Form):
    areas = forms.ChoiceField(label='Area to explore', choices=choices.AREAS, required=True)
    keyword = forms.CharField(label='Keyword', required=True)
