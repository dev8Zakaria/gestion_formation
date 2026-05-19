from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class InscriptionEtudiantForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, label="Prenom")
    last_name = forms.CharField(max_length=100, label="Nom")
    email = forms.EmailField(label="Email")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Cet email est deja utilise.")
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Nom d'utilisateur"
        self.fields["username"].help_text = ""
        self.fields["password1"].label = "Mot de passe"
        self.fields["password1"].help_text = "Le mot de passe doit contenir au moins 7 caracteres."
        self.fields["password2"].label = "Confirmer le mot de passe"
        self.fields["password2"].help_text = ""

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        user.is_staff = False
        user.is_superuser = False

        if commit:
            user.save()

        return user
