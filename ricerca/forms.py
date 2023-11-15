from django import forms

class RicercaForm(forms.Form):
    titolo = forms.CharField(label='Titolo', max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    autore = forms.CharField(label='Autore', max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    contributore = forms.CharField(label='Contributore', max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    tag = forms.CharField(label='Tag', max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    data_da = forms.DateField(label='Da', required=False, widget=forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'}))
    data_a = forms.DateField(label='A', required=False, widget=forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'}))