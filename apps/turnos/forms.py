from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Paciente, Turnos


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(label="Nombre")
    last_name = forms.CharField(label="Apellido")
    password1 = forms.CharField(label="Contraseña",
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirma Contraseña",
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name",
                  "password1", "password2"]
        help_texts = {k: "" for k in fields}


class UserForm(forms.ModelForm):
    first_name = forms.CharField(label="Nombre")
    last_name = forms.CharField(label="Apellido")
    # formulario que será mostrado en la vista update_profile

    class Meta:
        model = User
        # estos datos estaran disponibles para rellenar o modificar
        fields = ('first_name', 'last_name', 'email')


class PacienteForm(forms.ModelForm):
    # formulario que será mostrado en la vista update_profile, trae los datos
    # que no forman parte del usuario
    fecha_nacimiento = forms.DateField(widget=forms.SelectDateWidget(
        years=range(1900, 2020)))

    class Meta:
        model = Paciente
        fields = ('dni', 'obra_social', 'n_obra_social',
                  'fecha_nacimiento', 'telefono',)
