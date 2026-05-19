from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from formations.models import Formation

from .models import Etudiant


class InscriptionEtudiantTests(TestCase):
    def test_un_etudiant_peut_creer_son_compte(self):
        response = self.client.post(reverse('inscription_etudiant'), data={
            'username': 'etudiant1',
            'first_name': 'Ali',
            'last_name': 'Bennani',
            'email': 'ali@example.com',
            'password1': 'MotdepasseTest123',
            'password2': 'MotdepasseTest123',
        })

        self.assertRedirects(response, reverse('espace_etudiant'))
        user = User.objects.get(username='etudiant1')
        etudiant = Etudiant.objects.get(user=user)

        self.assertEqual(user.email, 'ali@example.com')
        self.assertFalse(user.is_staff)
        self.assertEqual(etudiant.prenom, 'Ali')
        self.assertEqual(etudiant.nom, 'Bennani')

    def test_un_mot_de_passe_numerique_de_7_caracteres_est_accepte(self):
        response = self.client.post(reverse('inscription_etudiant'), data={
            'username': 'etudiant2',
            'first_name': 'Sara',
            'last_name': 'Amrani',
            'email': 'sara@example.com',
            'password1': '1234567',
            'password2': '1234567',
        })

        self.assertRedirects(response, reverse('espace_etudiant'))
        self.assertTrue(User.objects.filter(username='etudiant2').exists())

    def test_un_mot_de_passe_de_6_caracteres_est_refuse(self):
        response = self.client.post(reverse('inscription_etudiant'), data={
            'username': 'etudiant3',
            'first_name': 'Lina',
            'last_name': 'Fassi',
            'email': 'lina@example.com',
            'password1': '123456',
            'password2': '123456',
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ce mot de passe est trop court")
        self.assertFalse(User.objects.filter(username='etudiant3').exists())


class EspaceEtudiantTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='etudiant-espace',
            password='1234567',
            first_name='Yasmine',
            last_name='Tazi',
            email='yasmine@example.com',
        )
        self.etudiant = Etudiant.objects.create(
            user=self.user,
            nom='Tazi',
            prenom='Yasmine',
            email='yasmine@example.com',
        )
        self.formation_jointe = Formation.objects.create(
            titre='Python',
            duree='2 mois',
            prix='500.00',
        )
        self.formation_disponible = Formation.objects.create(
            titre='Django',
            duree='3 mois',
            prix='900.00',
        )

    def test_un_etudiant_peut_rejoindre_plusieurs_formations(self):
        self.client.login(username='etudiant-espace', password='1234567')

        self.client.get(reverse('inscrire_formation', args=[self.formation_jointe.id]))
        self.client.get(reverse('inscrire_formation', args=[self.formation_disponible.id]))

        self.etudiant.refresh_from_db()
        self.assertEqual(self.etudiant.formations.count(), 2)

    def test_espace_etudiant_affiche_formations_rejointes_et_toutes_les_formations(self):
        self.etudiant.formations.add(self.formation_jointe)
        self.client.login(username='etudiant-espace', password='1234567')

        response = self.client.get(reverse('espace_etudiant'))

        self.assertContains(response, "Mes formations rejointes")
        self.assertContains(response, "Toutes les formations disponibles")
        self.assertContains(response, "Python")
        self.assertContains(response, "Django")
        self.assertContains(response, "Deja inscrit")
