from django.urls import path
from . import views

urlpatterns = [
    path('inscription/', views.inscription_etudiant, name='inscription_etudiant'),
    path('', views.espace_etudiant, name='espace_etudiant'),
    path('inscrire/<int:formation_id>/', views.inscrire_formation, name='inscrire_formation'),
]
