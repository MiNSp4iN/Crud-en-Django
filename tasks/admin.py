from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("created", )
    #readonly_fields nos indica que el campo created no se podrá modificar. Se le asigna una tupla con el campo que no se podrá modificar y por eso se le pone la coma final. Esto lo hemos usado porque en el panel de administrador no podíamos ver el atributo created y queríamos verlo.
# Register your models here.
admin.site.register(Task, TaskAdmin)