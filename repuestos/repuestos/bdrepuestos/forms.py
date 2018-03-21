from django import forms
import psycopg2

class ContactForm(forms.Form):
    query = forms.CharField(
        max_length=1000,
        widget=forms.Textarea(),
        help_text='Escriba su query'
    )

    def clean(self):
        cleaned_data = super(ContactForm, self).clean()
        query = cleaned_data.get('query')
