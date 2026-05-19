from django.db import models


class Formation(models.Model):
    titre = models.CharField(max_length=100)
    duree = models.CharField(max_length=50)
    prix = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.titre