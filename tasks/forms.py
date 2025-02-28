from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        #Meta es una clase interna que nos permite configurar el formulario.
        model = Task
        #model nos indica de qué modelo se va a crear el formulario. En este caso, de Task.
        fields = ["title", "description", "important"]
        #fields nos indica los campos que queremos que se muestren en el formulario. En este caso, el título, la descripción y si es importante o no.
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Escribe un título"}),
            "description": forms.Textarea(attrs={"class": "form-control" , "placeholder": "Escribe una descripción"}),
            "important": forms.CheckboxInput(attrs={"class": "form-check-input m-auto"}),
        }