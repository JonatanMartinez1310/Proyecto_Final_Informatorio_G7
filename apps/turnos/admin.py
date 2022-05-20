from django.contrib import admin
from .models import Paciente, Medico, Turnos

# Register your models here.


class Paciente_Admin(admin.ModelAdmin):
    list_display = ("user", "dni", "obra_social", "n_obra_social",
                    "fecha_nacimiento", "telefono")
    search_fields = ("user", "dni", "obra_social")
    list_filter = ("obra_social",)


class Medico_Admin(admin.ModelAdmin):
    list_display = ("nombre", "especialidad", "matricula", "cuit")
    search_fields = ("nombre", "especialidad", "matricula", "cuit")
    list_filter = ("especialidad",)


class Turnos_Admin(admin.ModelAdmin):
    list_display = ("paciente_id", "matricula_id", "fecha_hora")
    list_filter = ("fecha_hora",)
    date_hierarchy = "fecha_hora"


admin.site.register(Paciente, Paciente_Admin)

admin.site.register(Medico, Medico_Admin)

admin.site.register(Turnos, Turnos_Admin)
