from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# from django.dispatch import receiver

# Create your models here.


class Medico(models.Model):
    nombre = models.CharField(max_length=30)
    especialidad = models.CharField(max_length=50)
    matricula = models.IntegerField(primary_key=True)
    cuit = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return "%s - %s - %s" % (self.matricula, self.nombre,
                                 self.especialidad)


class Paciente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    medico = models.ManyToManyField(Medico, through='Turnos')
    id = models.IntegerField(primary_key=True)
    dni = models.IntegerField(null=True)
    obra_social = models.CharField(max_length=15)
    n_obra_social = models.IntegerField(null=True)
    fecha_nacimiento = models.DateField(null=True)
    telefono = models.IntegerField(null=True)

    def __str__(self):
        return "%s - %s %s" % (self.dni, self.user.first_name,
                               self.user.last_name)


class Turnos(models.Model):
    paciente_id = models.ForeignKey(Paciente, on_delete=models.CASCADE,
                                    null=True, blank=True)
    matricula_id = models.ForeignKey(Medico, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField()


def create_paciente(sender, instance, created, **kwargs):
    if created:
        Paciente.objects.create(user=instance)


post_save.connect(create_paciente, sender=User)
