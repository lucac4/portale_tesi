from django.contrib import admin

from .models import Progetto, Immagine, Contributo, Sviluppo, Tag

# Register your models here.
admin.site.register(Progetto)
admin.site.register(Immagine)
admin.site.register(Contributo)
admin.site.register(Sviluppo)
admin.site.register(Tag)