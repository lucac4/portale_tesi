from typing import Any
from django.views.generic import ListView
from progetti.models import Progetto
from django.db.models import Q
from .forms import RicercaForm

# Create your views here.
class RicercaProgetto(ListView):
    model = Progetto
    template_name = "ricerca.html"
    context_object_name = "progetti"
    paginate_by = 10
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['ricerca_form'] = RicercaForm(self.request.GET)
        return context

    def get_queryset(self):
        titolo = self.request.GET.get('titolo')
        autore = self.request.GET.get('autore')
        contributore = self.request.GET.get('contributore')
        tag = self.request.GET.get('tag')
        data_da = self.request.GET.get('data_da')
        data_a = self.request.GET.get('data_a')

        object_list = Progetto.objects.all()

        if titolo is not None and titolo is not "":
            object_list = object_list.filter(titolo__icontains=titolo)
        if autore is not None and autore is not "":
            object_list = object_list.filter(autore__username__icontains=autore)
        if contributore is not None and contributore is not "":
            object_list = object_list.filter(contributi__contributore__username__icontains=contributore)
        if tag is not None and tag is not "":
            object_list = object_list.filter(tags__nome__icontains=tag)
        if data_da is not None and data_da is not "":
            object_list = object_list.filter(data_creazione__gte=data_da)
        if data_a is not None and data_a is not "":
            object_list = object_list.filter(data_creazione__lte=data_a)
        
        return object_list.order_by('-data_creazione').distinct()