from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Formation
from .forms import FormationForm


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("Accès interdit : réservé aux administrateurs.")
    return wrapper


@login_required
def liste_formations(request):
    formations = Formation.objects.all()
    return render(request, 'formations/liste_formations.html', {
        'formations': formations
    })


@login_required
@admin_required
def dashboard_admin(request):
    formations = Formation.objects.all()
    return render(request, 'formations/dashboard_admin.html', {
        'formations': formations
    })


@login_required
@admin_required
def ajouter_formation(request):
    if request.method == 'POST':
        form = FormationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard_admin')
    else:
        form = FormationForm()

    return render(request, 'formations/formation_form.html', {
        'form': form
    })


@login_required
@admin_required
def modifier_formation(request, formation_id):
    formation = get_object_or_404(Formation, id=formation_id)

    if request.method == 'POST':
        form = FormationForm(request.POST, instance=formation)
        if form.is_valid():
            form.save()
            return redirect('dashboard_admin')
    else:
        form = FormationForm(instance=formation)

    return render(request, 'formations/formation_form.html', {
        'form': form
    })


@login_required
@admin_required
def supprimer_formation(request, formation_id):
    formation = get_object_or_404(Formation, id=formation_id)

    if request.method == 'POST':
        formation.delete()
        return redirect('dashboard_admin')

    return render(request, 'formations/confirmer_suppression.html', {
        'formation': formation
    })