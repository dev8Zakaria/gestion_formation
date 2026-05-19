from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from formations.models import Formation
from .models import Etudiant
from .forms import InscriptionEtudiantForm


def inscription_etudiant(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('dashboard_admin')
        return redirect('espace_etudiant')

    if request.method == 'POST':
        form = InscriptionEtudiantForm(request.POST)
        if form.is_valid():
            user = form.save()
            Etudiant.objects.create(
                user=user,
                nom=user.last_name,
                prenom=user.first_name,
                email=user.email,
            )
            login(request, user)
            return redirect('espace_etudiant')
    else:
        form = InscriptionEtudiantForm()

    return render(request, 'etudiants/inscription.html', {
        'form': form
    })


@login_required
def espace_etudiant(request):
    if request.user.is_staff:
        return redirect('dashboard_admin')

    formations = Formation.objects.all()
    etudiant = Etudiant.objects.filter(user=request.user).prefetch_related('formations').first()
    formations_rejointes = etudiant.formations.all() if etudiant else Formation.objects.none()
    formations_rejointes_ids = list(formations_rejointes.values_list('id', flat=True))

    return render(request, 'etudiants/espace_etudiant.html', {
        'formations': formations,
        'etudiant': etudiant,
        'formations_rejointes': formations_rejointes,
        'formations_rejointes_ids': formations_rejointes_ids,
    })


@login_required
def inscrire_formation(request, formation_id):
    if request.user.is_staff:
        return redirect('dashboard_admin')

    formation = get_object_or_404(Formation, id=formation_id)

    etudiant, created = Etudiant.objects.get_or_create(
        user=request.user,
        defaults={
            'nom': request.user.last_name or request.user.username,
            'prenom': request.user.first_name or '',
            'email': request.user.email or '',
        }
    )

    etudiant.formations.add(formation)

    return redirect('espace_etudiant')
