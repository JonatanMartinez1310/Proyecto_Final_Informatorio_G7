from django.shortcuts import render, redirect
from .forms import UserRegisterForm, PacienteForm, UserForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Medico, Turnos, Paciente
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User

# from django.http import HttpResponse


# Create your views here.


def index(request):
    return render(request, "index.html", {})


# def login(request):
#    return render(request, "login.html", {})


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            messages.success(request, f"""Usuario {username} creado.
            Por favor inicie sesión""")
            return redirect("index")
        else:
            messages.warning(request, "Controle los datos ingresados")
    else:
        form = UserRegisterForm()
    context = {"form": form, }
    return render(request, "register.html", context)


@login_required(login_url='/turnos/login/')
def update(request):
    try:
        usuario = request.user.first_name
    except:
        usuario = "null"
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = PacienteForm(request.POST,
                                    instance=request.user.paciente)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Perfil Actualizado")
            return redirect("turnos:account")
        else:
            messages.warning(request, "Controle los datos ingresados")
    else:
        # aqui se envian al form los datos guardados del user en la db
        user_form = UserForm(instance=request.user)
        # aqui se envian al form los datos guardados del paciente en la db
        profile_form = PacienteForm(instance=request.user.paciente)
    context = {"user_form": user_form, "profile_form": profile_form,
               "usuario": usuario}
    return render(request, "update.html", context)


@login_required(login_url='/turnos/login/')
def account(request):
    return render(request, "account.html")


@method_decorator(login_required(login_url='/turnos/login/'), name='dispatch')
class Medicos(ListView):
    model = Medico


def appointment(request):
    matricula_medico = request.POST.get("matricula")
    turnos = Turnos.objects.all()
    turnos = turnos.values().filter(matricula_id=matricula_medico).filter(paciente_id=None)
    return render(request, "appointment.html", {'turnos': turnos})


def confirm(request):
    # Pantalla de confirmacion del turno. Falta agregarle el guardado
    # en la base de datos.

    turno_id = request.POST.get("turno_id")
    # turnos = Turnos.objects.all().values()
    try:
        turno = Turnos.objects.get(id=turno_id)
        matricula_id = turno.matricula_id.matricula
        medico = Medico.objects.get(matricula=matricula_id)
        userr = User.objects.get(username=request.user)
        paciente = Paciente.objects.get(user=userr.id)
        turno.paciente_id = paciente
        turno.save()
        # medico = medicos.filter(matricula=matricula_id)
        context = {"turno": turno.fecha_hora, "medico": medico.nombre}
        return render(request, "confirm.html", context)
    except:
        messages.warning(
            request, "Usted ingreso un turno invalido. Por favor seleccione un nuevo tuno")
        return redirect("turnos:medicos")


def misturnos(request):
    userr = User.objects.get(username=request.user)
    paciente = Paciente.objects.get(user_id=userr.id)
    turnos = Turnos.objects.all().filter(paciente_id=paciente.id)
    contex = {"userr": userr, "paciente": paciente, "turnos": turnos}
    return render(request, "misturnos.html", contex)


def edit(request):
    # borra la vinculacion del usuario con el turno y
    # te manda a elegir uno nuevo
    turno_id = request.POST.get("turno_id")
    turno = Turnos.objects.get(id=turno_id)
    matricula_medico = turno.matricula_id.matricula
    turnos = Turnos.objects.all()
    turnos = turnos.values().filter(matricula_id=matricula_medico).filter(paciente_id=None)
    return render(request, "edit_appointment.html", {'turnos': turnos,
                                                     "turno_id": turno_id})


def confirm_edit(request):
    turno_id = request.POST.get("turno_id")
    turno_edit = request.POST.get("turno_edit")
    try:
        turno = Turnos.objects.get(id=turno_id)
        matricula_id = turno.matricula_id.matricula
        medico = Medico.objects.get(matricula=matricula_id)
        userr = User.objects.get(username=request.user)
        paciente = Paciente.objects.get(user=userr.id)
        turno.paciente_id = paciente
        turno.save()
        turno_delete = Turnos.objects.get(id=turno_edit)
        turno_delete.paciente_id = None
        turno_delete.save()
        # medico = medicos.filter(matricula=matricula_id)
        context = {"turno": turno.fecha_hora, "medico": medico.nombre}
        return render(request, "confirm.html", context)
    except:
        messages.warning(
            request, "Usted ingreso un turno invalido. Por favor seleccione un nuevo tuno")
        return redirect("turnos:misturnos")


def delete(request):
    # Borra la vinculacion del usuario con el turno.
    # Los turnos siguen existiendo para que los saque alguien mas
    turno_id = request.POST.get("turno_id")
    turno = Turnos.objects.get(id=turno_id)
    turno.paciente_id = None
    turno.save()
    medico = turno.matricula_id
    context = {"turno": turno.fecha_hora, "medico": medico.nombre}
    return render(request, "delete.html", context)
