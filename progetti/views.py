from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from .models import Immagine, Progetto, Sviluppo
from .forms import ProgettoForm, ImmagineForm, TagForm, SviluppoForm, RuoloForm
from django.urls import reverse_lazy, reverse

class Home(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['progetti'] = Progetto.objects.all().order_by('-data_modifica')[:10]
        context['sviluppi'] = Sviluppo.objects.all().order_by('-id')[:10]
        return context

class ProgettoLista(ListView):
    model = Progetto
    template_name = 'progetti.html'
    context_object_name = 'progetti'
    ordering = ['-data_modifica']
    paginate_by = 24

    def get_queryset(self):
        queryset = super().get_queryset()

        stato = self.request.GET.get('stato')
        ordinamento = self.request.GET.get('ord')

        if open is not None:
            if stato == "opn":
                queryset = queryset.filter(contributi=None)
            elif stato == "inc":
                queryset = queryset.filter(stato="INCORSO")
            elif stato == "cmp":
                queryset = queryset.filter(stato="COMPLETATO")
        if ordinamento is not None:
            if ordinamento == "dasc":
                queryset = queryset.order_by('-data_modifica')
            elif ordinamento == "ddec":
                queryset = queryset.order_by('data_modifica')
            elif ordinamento == "tasc":
                queryset = queryset.order_by('titolo')
            elif ordinamento == "tdec":
                queryset = queryset.order_by('-titolo')

        return queryset.distinct()

class ProgettoDettaglio(DetailView):
    model = Progetto
    template_name = 'progetto_dettaglio.html'
    context_object_name = 'progetto'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['immagini'] = Immagine.objects.filter(progetto=self.kwargs.get('pk'))
        context['sviluppi_completati'] = Sviluppo.objects.filter(progetto=self.kwargs.get('pk'), stato='COMPLETATO')
        context['sviluppi_incorso'] = Sviluppo.objects.filter(progetto=self.kwargs.get('pk'), stato='INCORSO')
        context['sviluppi_futuri'] = Sviluppo.objects.filter(progetto=self.kwargs.get('pk'), stato='DAFARE')
        return context

class ProgettoCrea(LoginRequiredMixin, TemplateView):
    template_name = 'progetto_nuovo.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['progetto_form'] = ProgettoForm()
        context['immagine_form'] = ImmagineForm()
        return context

    def post(self, request, *args, **kwargs):

        progetto_form = ProgettoForm(request.POST)
        immagine_form = ImmagineForm(request.POST, request.FILES)

        if progetto_form.is_valid():
            progetto = progetto_form.save(commit=False)
            progetto.autore = request.user
            progetto.save()
            progetto_form.save_m2m()
            if immagine_form.is_valid() and immagine_form.cleaned_data['img'] is not None:
                for img in immagine_form.cleaned_data['img']:
                    immagine = Immagine(progetto=progetto, img=img)
                    immagine.save()
            return HttpResponseRedirect(reverse('progetti'))
        else:
            return render(request, self.template_name, {'progetto_form': progetto_form, 'immagine_form': immagine_form})

class ProgettoModifica(LoginRequiredMixin, UpdateView):
    template_name = 'progetto_modifica.html'
    model = Progetto
    form_class = ProgettoForm

    def get_success_url(self):
        return reverse_lazy('progetto_dettagli', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["immagine_form"] = ImmagineForm(instance=self.object)
        context["tag_form"] = TagForm()
        return context

    def get(self, request, *args, **kwargs):

        progetto = self.object = self.get_object()

        if request.user != progetto.autore:
            return HttpResponse("Non sei autorizzato a modificare questo progetto")

        return super(ProgettoModifica, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        progetto = self.object = self.get_object()

        if request.user != progetto.autore:
            return HttpResponse("Non sei autorizzato a modificare questo progetto")

        progetto_form = ProgettoForm(request.POST, instance=progetto)
        immagine_form = ImmagineForm(request.POST, request.FILES)
        tag_form = TagForm(request.POST)

        if "progetto_modifica" in request.POST:
            if progetto_form.is_valid():
                progetto.titolo = progetto_form.cleaned_data['titolo']
                progetto.descrizione = progetto_form.cleaned_data['descrizione']
                progetto.save()
                return HttpResponseRedirect(reverse('progetto_modifica', kwargs={'pk': progetto.pk}))
            
        elif "immagini_aggiungi" in request.POST:
            if immagine_form.is_valid() and immagine_form.cleaned_data['img'] is not None:
                for img in immagine_form.cleaned_data['img']:
                    immagine = Immagine(progetto=progetto, img=img)
                    immagine.save()
                return HttpResponseRedirect(reverse('progetto_modifica', kwargs={'pk': progetto.pk}))
        elif "tag_aggiungi" in request.POST:
            if tag_form.is_valid():
                progetto.tags.set(request.POST.getlist('tags'))
                if tag_form.cleaned_data['nome'] != "":
                    tag = tag_form.save()
                    progetto.tags.add(tag)
                return HttpResponseRedirect(reverse('progetto_modifica', kwargs={'pk': progetto.pk}))
        return HttpResponseRedirect(reverse('progetto_modifica', kwargs={'pk': progetto.pk}))

def immagine_elimina(request, pk):

    immagine = Immagine.objects.get(pk=pk)
    progetto = immagine.progetto
    if request.user == progetto.autore:
        immagine.delete()
        return HttpResponseRedirect(reverse('progetto_modifica', kwargs={'pk': progetto.pk}))
    else:
        return HttpResponse("Non sei autorizzato a eliminare questa immagine")
    
class StoriaProgetto(DetailView):
    model = Progetto
    template_name = 'progetto_storia.html'
    context_object_name = 'progetto'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sviluppi_completati'] = Sviluppo.objects.filter(progetto=self.kwargs.get('pk'), stato="COMPLETATO")
        context['sviluppi_incorso'] = Sviluppo.objects.filter(progetto=self.kwargs.get('pk'), stato="INCORSO")
        context['sviluppi_futuri'] = Sviluppo.objects.filter(progetto=self.kwargs.get('pk'), stato="DAFARE")
        return context
    
class SviluppoCrea(LoginRequiredMixin, CreateView):
    model = Sviluppo
    template_name = 'sviluppo_nuovo.html'
    success_url = reverse_lazy('progetti')
    form_class = SviluppoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['progetto'] = Progetto.objects.get(pk=self.kwargs.get('pk'))
        return context
    
    def form_valid(self, form):
        form.instance.progetto = Progetto.objects.get(pk=self.kwargs.get('pk'))
        form.instance.responsabile = self.request.user
        return super().form_valid(form)
    
class SviluppoModifica(LoginRequiredMixin, UpdateView):
    model = Sviluppo
    template_name = 'sviluppo_modifica.html'
    success_url = reverse_lazy('progetti')
    form_class = SviluppoForm
    context_object_name = 'sviluppo'
    
    def get(self, request, *args, **kwargs):
        contributo = self.object = self.get_object()
        if request.user != contributo.responsabile:
            return HttpResponse("Non sei autorizzato a modificare questo contributo")    
        return super(SviluppoModifica, self).get(request, *args, **kwargs)
    
class SviluppoDettaglio(DetailView):
    model = Sviluppo
    template_name = 'sviluppo_dettagli.html'
    context_object_name = 'sviluppo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sviluppi'] = Sviluppo.objects.filter(progetto=self.get_object().progetto).exclude(pk=self.kwargs.get('pk')).order_by('-data_inizio')
        return context
    
class RuoloImposta(LoginRequiredMixin, TemplateView):
    template_name = 'ruolo_imposta.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['progetto'] = Progetto.objects.get(pk=self.kwargs.get('pk'))
        context['ruolo_form'] = RuoloForm()
        return context
    
    def post(self, request, *args, **kwargs):

        ruolo_form = RuoloForm(request.POST)
        progetto = Progetto.objects.get(pk=self.kwargs.get('pk'))


        if ruolo_form.is_valid():
            if progetto.contributi.filter(contributore=request.user, ruolo=ruolo_form.cleaned_data['ruolo']).exists():
                return HttpResponse("Hai già impostato questo ruolo per questo progetto")
            ruolo = ruolo_form.save(commit=False)
            ruolo.contributore = request.user
            ruolo.save()
            progetto.contributi.add(ruolo)
            progetto.save()
            return HttpResponseRedirect(reverse('progetto_dettagli', kwargs={'pk': self.kwargs.get('pk')}))
        
        return render(request, self.template_name, {'ruolo_form': ruolo_form, 'progetto': Progetto.objects.get(pk=self.kwargs.get('pk'))})
        
class ProgettiUtente(LoginRequiredMixin, TemplateView):
    template_name = 'progetti_utente.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['progetti_creati'] = Progetto.objects.filter(autore=self.request.user)
        context['progetti_contribuiti'] = Progetto.objects.filter(contributi__contributore=self.request.user)
        context['sviluppi'] = Sviluppo.objects.filter(responsabile=self.request.user)
        return context
    
def progetto_elimina(request, pk):

    progetto = Progetto.objects.get(pk=pk)

    if request.user == progetto.autore:
        progetto.delete()
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    else:
        return HttpResponse("Non sei autorizzato a eliminare questo progetto")
    
def sviluppo_elimina(request, pk):

    sviluppo = Sviluppo.objects.get(pk=pk)

    if request.user == sviluppo.responsabile or request.user == sviluppo.progetto.autore:
        sviluppo.delete()
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    else:
        return HttpResponse("Non sei autorizzato a eliminare questa attività")