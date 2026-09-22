from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import (
    CommentForm,
    ProjectForm,
    SubtaskForm,
    TaskFileForm,
    TaskForm,
    UserRegisterForm,
)
from .models import Category, Favorite, FavoriteItem, Project, Subtask, Task


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("project_list")
    else:
        form = UserRegisterForm()
    return render(request, "tasks/register.html", {"form": form})


@login_required
def profile(request):
    return render(request, "tasks/profile.html", {"profile_user": request.user})

def category_list(request):
    categories = Category.objects.all()
    return render(request, "tasks/category_list.html", {"categories": categories})

@login_required
def project_list(request):
    projects = Project.objects.filter(owner=request.user)
    return render(request, "tasks/project_list.html", {"projects": projects})


@login_required
def project_create(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            return redirect("project_detail", pk=project.pk)
    else:
        form = ProjectForm()
    return render(request, "tasks/project_form.html", {"form": form})


@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    tasks = project.tasks.all()
    return render(
        request, "tasks/project_detail.html", {"project": project, "tasks": tasks}
    )


@login_required
def task_create(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk, owner=request.user)
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            form.save_m2m()
            return redirect("task_detail", pk=task.pk)
    else:
        form = TaskForm()
    return render(request, "tasks/task_form.html", {"form": form, "project": project})


@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, project__owner=request.user)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("task_detail", pk=task.pk)
    else:
        form = TaskForm(instance=task)
    return render(request, "tasks/task_form.html", {"form": form, "task": task})


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, project__owner=request.user)
    project_pk = task.project_id
    if request.method == "POST":
        task.delete()
        return redirect("project_detail", pk=project_pk)
    return render(request, "tasks/task_confirm_delete.html", {"task": task})


@login_required
@require_POST
def task_toggle_complete(request, pk):
    task = get_object_or_404(Task, pk=pk, project__owner=request.user)
    task.completed = not task.completed
    task.save(update_fields=["completed"])
    return redirect("task_detail", pk=task.pk)


@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk, project__owner=request.user)
    subtask_form = SubtaskForm()
    comment_form = CommentForm()
    file_form = TaskFileForm()
    is_favorite = FavoriteItem.objects.filter(
        favorite__user=request.user, task=task
    ).exists()
    context = {
        "task": task,
        "subtask_form": subtask_form,
        "comment_form": comment_form,
        "file_form": file_form,
        "is_favorite": is_favorite,
    }
    return render(request, "tasks/task_detail.html", context)

@login_required
@require_POST
def subtask_add(request, task_pk):
    task = get_object_or_404(Task, pk=task_pk, project__owner=request.user)
    form = SubtaskForm(request.POST)
    if form.is_valid():
        subtask = form.save(commit=False)
        subtask.task = task
        subtask.save()
    return redirect("task_detail", pk=task.pk)


@login_required
@require_POST
def subtask_toggle(request, pk):
    subtask = get_object_or_404(Subtask, pk=pk, task__project__owner=request.user)
    subtask.completed = not subtask.completed
    subtask.save(update_fields=["completed"])
    return redirect("task_detail", pk=subtask.task_id)


@login_required
@require_POST
def task_file_upload(request, task_pk):
    task = get_object_or_404(Task, pk=task_pk, project__owner=request.user)
    form = TaskFileForm(request.POST, request.FILES)
    if form.is_valid():
        task_file = form.save(commit=False)
        task_file.task = task
        task_file.save()
    return redirect("task_detail", pk=task.pk)


@login_required
@require_POST
def comment_add(request, task_pk):
    task = get_object_or_404(Task, pk=task_pk, project__owner=request.user)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.task = task
        comment.user = request.user
        comment.save()
    return redirect("task_detail", pk=task.pk)

@login_required
def favorite_list(request):
    favorite, _ = Favorite.objects.get_or_create(user=request.user)
    items = favorite.items.select_related("task")
    return render(request, "tasks/favorite_list.html", {"items": items})


@login_required
@require_POST
def favorite_toggle(request, task_pk):
    task = get_object_or_404(Task, pk=task_pk, project__owner=request.user)
    favorite, _ = Favorite.objects.get_or_create(user=request.user)
    item = FavoriteItem.objects.filter(favorite=favorite, task=task).first()
    if item:
        item.delete()
    else:
        FavoriteItem.objects.get_or_create(favorite=favorite, task=task)
    return redirect("task_detail", pk=task.pk)