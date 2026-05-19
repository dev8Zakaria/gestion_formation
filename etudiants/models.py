from django.db import models
from django.contrib.auth.models import User
from formations.models import Formation


class Etudiant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField()
    formations = models.ManyToManyField(Formation, blank=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"
