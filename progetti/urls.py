from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('progetti/', views.ProgettoLista.as_view(), name='progetti'),
    path('progetti/nuovo/', views.ProgettoCrea.as_view(), name='progetto_nuovo'),
    path('progetti/<int:pk>/', views.ProgettoDettaglio.as_view(), name='progetto_dettagli'),
    path('progetti/<int:pk>/modifica/', views.ProgettoModifica.as_view(), name='progetto_modifica'),
    path('progetti/<int:pk>/elimina/', views.progetto_elimina, name='progetto_elimina'),
    path('progetti/<int:pk>/ruolo/', views.RuoloImposta.as_view(), name='ruolo_imposta'),
    path('progetti/<int:pk>/storia/', views.StoriaProgetto.as_view(), name='progetto_storia'),
    path('progetti/<int:pk>/contributo/nuovo/', views.SviluppoCrea.as_view(), name='sviluppo_nuovo'),
    path('progetti_utente/', views.ProgettiUtente.as_view(), name='progetti_utente'),
    path('immagine/<int:pk>/elimina/', views.immagine_elimina, name='immagine_elimina'),
    path('contributo/<int:pk>/', views.SviluppoDettaglio.as_view(), name='sviluppo_dettagli'),
    path('contributo/<int:pk>/modifica/', views.SviluppoModifica.as_view(), name='sviluppo_modifica'),
    path('contributo/<int:pk>/elimina/', views.sviluppo_elimina, name='sviluppo_elimina'),
]