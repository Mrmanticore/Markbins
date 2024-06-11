
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'class': 'input1',
        'placeholder': 'Name'
    }))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={
        'class': 'input1',
        'placeholder': 'Email'
    }))
    subject = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'class': 'input1',
        'placeholder': 'Subject'
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'input1',
        'placeholder': 'Message'
    }), required=True)
