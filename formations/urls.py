from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_formations, name='liste_formations'),
    path('dashboard/', views.dashboard_admin, name='dashboard_admin'),
    path('ajouter/', views.ajouter_formation, name='ajouter_formation'),
    path('modifier/<int:formation_id>/', views.modifier_formation, name='modifier_formation'),
    path('supprimer/<int:formation_id>/', views.supprimer_formation, name='supprimer_formation'),
]