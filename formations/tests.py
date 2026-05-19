from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Formation


class ListeFormationsTests(TestCase):
    def test_la_liste_formations_n_affiche_pas_la_colonne_action(self):
        user = User.objects.create_user(username='simple', password='1234567')
        Formation.objects.create(titre='React', duree='2 mois', prix='700.00')

        self.client.login(username='simple', password='1234567')
        response = self.client.get(reverse('liste_formations'))

        self.assertContains(response, "React")
        self.assertNotContains(response, "<th>Action</th>", html=False)
        self.assertNotContains(response, "S'inscrire")
