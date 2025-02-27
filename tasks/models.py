from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    #El blank=True nos indica que si no nos pasan nada el texto estará vacío.
    created = models.DateTimeField(auto_now_add=True)
    #auto_now_add=True nos indica que la fecha y hora se establecerá automáticamente cuando se cree un objeto.
    datecompleted = models.DateTimeField(null=True, blank=True) 
    #null=True nos indica que la fecha y hora estarán vacías y las tendremos que completar nosotros. blank=True nos indica que si no nos pasan nada el campo estará vacío, sería opcional, pero para el administrador, a la base de datos debemos de pasarle algo.
    important = models.BooleanField(default=False)
    #default=False nos indica que por defecto la tarea no es importante, si lo es se cambiará a True.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #ForeignKey nos indica que la tarea pertenece a un usuario, on_delete=models.CASCADE nos indica que si el usuario se borra, se borrarán todas las tareas que pertenezcan a ese usuario.
    
    def __str__(self):
        return self.title + " - by " + self.user.username