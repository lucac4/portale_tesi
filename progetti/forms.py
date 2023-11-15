from django import forms
from .models import Immagine, Progetto, Tag, Sviluppo, Contributo

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.ImageField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput(attrs={'class': 'form-control'}))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class ImmagineForm(forms.ModelForm):

    img = MultipleFileField(label='Immagini', required=False)

    class Meta:
        model = Immagine
        fields = ['img']


class ProgettoForm(forms.ModelForm):

    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all().order_by("nome"), required=False, widget=forms.SelectMultiple(attrs={"class":"form-control", "style":"height:200px;"}))
    stato = forms.ChoiceField(choices=Progetto.STATI , widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Progetto
        fields = ['titolo', 'descrizione', 'link_progetto', 'stato', 'tags']

class TagForm(forms.ModelForm):
    
    nome = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = Tag
        fields = ['nome']

    def clean_nome(self):
        nome = self.cleaned_data['nome'].capitalize()
        return nome
    
class SviluppoForm(forms.ModelForm):

    data_inizio = forms.DateField(widget=forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'}), required=False)
    data_fine = forms.DateField(widget=forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date', 'placeholder':""}), required=False)
    stato = forms.ChoiceField(choices=Sviluppo.STATI , widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Sviluppo
        fields = ['nome', 'descrizione', 'data_inizio', 'data_fine', 'stato']

class RuoloForm(forms.ModelForm):

    ruolo = forms.ChoiceField(choices=Contributo.RUOLI, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Contributo
        fields = ['ruolo']

class FiltroForm(forms.Form):
    titolo = forms.CharField(label='Titolo', max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    autore = forms.CharField(label='Autore', max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    contributore = forms.CharField(label='Contributore', max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    tag = forms.CharField(label='Tag', max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    data_da = forms.DateField(label='Da', required=False, widget=forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'}))
    data_a = forms.DateField(label='A', required=False, widget=forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'}))