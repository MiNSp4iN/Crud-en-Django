from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.


def home(request):
    return render(request, "home.html")


def signup(request):
    if request.method == "GET":
        form = UserCreationForm()
        return render(request, "signup.html", {"form": form})

    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user)
                return redirect("tasks")
            except IntegrityError:
                return render(request, "signup.html", {
                    "form": UserCreationForm(),
                    "error": "Username already exists",
                })

        return render(request, "signup.html", {
            "form": UserCreationForm(),
            "error": "Passwords did not match",
        })


@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    # Filtramos las tareas por el usuario que ha iniciado sesión. datecompleted__isnull=True es como decir que la fecha de completado es nula y quiero que me muestres las tareas que no tienen fecha de completado, es decir, me muestra las tareas que al no tener fecha de completado, aún no están acabadas, le estoy pidiendo las tareas que quedan por hacer.
    return render(request, "tasks.html", {
        "tasks": tasks,
        "mensaje": "Tasks pending",
    })


@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(
        user=request.user, datecompleted__isnull=False).order_by("-datecompleted")
    # Filtramos las tareas por el usuario que ha iniciado sesión. datecompleted__isnull=False es como decir que la fecha de completado no es nula y quiero que me muestres las tareas que tienen fecha de completado, es decir, me muestra las tareas que al tener fecha de completado, están acabadas, le estoy pidiendo las tareas que ya están hechas. Order_by("-datecompleted") nos indica que las tareas se ordenarán por la fecha de completado de forma descendente, es decir, que las tareas más recientes aparecerán primero.
    return render(request, "tasks.html", {
        "tasks": tasks,
        "mensaje": "Tasks completed",
    })


@login_required
def create_task(request):
    # Si el método es GET, devolvemos el formulario vacío.
    if request.method == "GET":
        return render(request, "create_task.html", {
            "form": TaskForm()
        })
    else:
        try:
            # Si el método es POST, cogemos los datos y los guardamos en la base de datos pasandole a TaskForm los datos y guardándolos en una variable, en este caso form.
            form = TaskForm(request.POST)
            # Creamos un objeto TaskForm con los datos que nos han pasado.
            new_task = form.save(commit=False)
            # commit=False nos indica que no se guarde la tarea en la base de datos todavía.
            new_task.user = request.user
            # Le asignamos el usuario que ha creado la tarea.
            new_task.save()
            print(new_task)
            return redirect("tasks")
        except ValueError:
            # Si hay un error, devolvemos el formulario con un mensaje de error.
            return render(request, "create_task.html", {
                "form": TaskForm(),
                "error": "Please provide valida data."
            })


@login_required
def task_detail(request, task_id):
    if request.method == "GET":
        # Si el método es GET, devolvemos el formulario con los datos de la tarea.
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        # get_object_or_404 nos devuelve el objeto que le pasamos o un error 404 si no lo encuentra. PK es la clave primaria. Task es el modelo y task_id es la clave primaria. User es el usuario que ha iniciado sesión.
        form = TaskForm(instance=task)
        # instance=task nos indica que el formulario se rellenará con los datos de la tarea.
        return render(request, "task_detail.html", {"task": task,
                                                    "form": form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect("tasks")
        except ValueError:
            return render(request, "task_detail.html", {
                "task": task,
                "form": form,
                "error": "Error updating task."
            })


@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == "POST":
        task.datecompleted = timezone.now()
        # timezone.now() nos devuelve la fecha y hora actual.
        task.save()
        # Guardamos la tarea después de cambiar y aplicar la fecha y hora actual en el atributo datecompleted de la variable task, que recordemos que por defecto está en nulo, es decir, que no tiene ni fecha ni hora.
        return redirect("tasks")


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == "POST":
        task.delete()
        return redirect("tasks")


@login_required
def signout(request):
    logout(request)
    return redirect("home")


def signin(request):
    if request.method == "GET":
        return render(request, "signin.html", {"form": AuthenticationForm()})
    else:
        user = authenticate(
            request, username=request.POST["username"], password=request.POST["password"])
        if user is None:
            return render(request, "signin.html", {
                "form": AuthenticationForm(),
                "error": "Username or password is incorrect", })
        else:
            login(request, user)
            return redirect("tasks")
