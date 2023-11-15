from django.urls import path
from . import views

urlpatterns = [
    path('', views.RicercaProgetto.as_view(), name='ricerca'),
]
