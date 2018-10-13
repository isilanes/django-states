# Django libs:
from django import forms


# Forms:
class BookForm(forms.Form):
    pages_read = forms.IntegerField(label="Pages read", max_value=10000)
