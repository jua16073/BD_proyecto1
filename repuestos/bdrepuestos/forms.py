from django import forms
import psycopg2

class ContactForm(forms.Form):
    query = forms.CharField(
        max_length=100
    )

    def clean(self):
        cleaned_data = super(ContactForm, self).clean()
        query = cleaned_data.get('query')
