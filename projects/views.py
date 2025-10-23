from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from .models import Project, Sprint, UserStory, Task, Comment
from .forms import ProjectForm, SprintForm, UserStoryForm, TaskForm, CommentForm


# ===== VISTAS DE PROYECTO =====

@login_required
def project_list(request):
    """
    Lista todos los proyectos donde el usuario es miembro, product owner o scrum master.
    Mejores prácticas:
    - Uso de Q objects para queries complejas
    - Anotaciones para información agregada
    - Decorador login_required
    """
    projects = Project.objects.filter(
        Q(team_members=request.user) |
        Q(product_owner=request.user) |
        Q(scrum_master=request.user)
    ).distinct().annotate(
        story_count=Count('user_stories'),
        sprint_count=Count('sprints')
    )

    context = {
        'projects': projects,
    }
    return render(request, 'projects/project_list.html', context)


@login_required
def project_detail(request, pk):
    """
    Muestra el detalle de un proyecto específico.
    """
    project = get_object_or_404(Project, pk=pk)

    # Verificar que el usuario tenga acceso al proyecto
    if not (request.user in project.team_members.all() or
            request.user == project.product_owner or
            request.user == project.scrum_master):
        messages.error(request, 'No tienes permiso para ver este proyecto.')
        return redirect('project_list')

    sprints = project.sprints.all()[:5]
    user_stories = project.user_stories.all()[:10]

    context = {
        'project': project,
        'sprints': sprints,
        'user_stories': user_stories,
    }
    return render(request, 'projects/project_detail.html', context)


@login_required
def project_create(request):
    """
    Crea un nuevo proyecto.
    Mejores prácticas:
    - Uso de forms para validación
    - Mensajes de éxito/error
    - Redirección después de POST
    """
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            messages.success(request, f'Proyecto "{project.name}" creado exitosamente.')
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectForm()

    context = {
        'form': form,
        'title': 'Crear Proyecto',
    }
    return render(request, 'projects/project_form.html', context)


@login_required
def project_update(request, pk):
    """
    Actualiza un proyecto existente.
    """
    project = get_object_or_404(Project, pk=pk)

    # Solo el product owner o scrum master pueden editar
    if request.user != project.product_owner and request.user != project.scrum_master:
        messages.error(request, 'No tienes permiso para editar este proyecto.')
        return redirect('project_detail', pk=pk)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, f'Proyecto "{project.name}" actualizado.')
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectForm(instance=project)

    context = {
        'form': form,
        'project': project,
        'title': 'Editar Proyecto',
    }
    return render(request, 'projects/project_form.html', context)


# ===== VISTAS DE SPRINT =====

@login_required
def sprint_list(request, project_pk):
    """
    Lista todos los sprints de un proyecto.
    """
    project = get_object_or_404(Project, pk=project_pk)
    sprints = project.sprints.all()

    context = {
        'project': project,
        'sprints': sprints,
    }
    return render(request, 'projects/sprint_list.html', context)


@login_required
def sprint_detail(request, pk):
    """
    Muestra el detalle de un sprint específico.
    """
    sprint = get_object_or_404(Sprint, pk=pk)
    user_stories = sprint.user_stories.all()

    context = {
        'sprint': sprint,
        'user_stories': user_stories,
    }
    return render(request, 'projects/sprint_detail.html', context)


@login_required
def sprint_create(request, project_pk):
    """
    Crea un nuevo sprint para un proyecto.
    """
    project = get_object_or_404(Project, pk=project_pk)

    if request.method == 'POST':
        form = SprintForm(request.POST, project=project)
        if form.is_valid():
            sprint = form.save(commit=False)
            sprint.project = project
            sprint.save()
            messages.success(request, f'Sprint "{sprint.name}" creado exitosamente.')
            return redirect('sprint_detail', pk=sprint.pk)
    else:
        form = SprintForm(project=project)

    context = {
        'form': form,
        'project': project,
        'title': 'Crear Sprint',
    }
    return render(request, 'projects/sprint_form.html', context)


# ===== VISTAS DE USER STORY =====

@login_required
def user_story_list(request, project_pk):
    """
    Lista todas las historias de usuario de un proyecto.
    """
    project = get_object_or_404(Project, pk=project_pk)
    user_stories = project.user_stories.all()

    # Filtros opcionales
    status = request.GET.get('status')
    priority = request.GET.get('priority')

    if status:
        user_stories = user_stories.filter(status=status)
    if priority:
        user_stories = user_stories.filter(priority=priority)

    context = {
        'project': project,
        'user_stories': user_stories,
    }
    return render(request, 'projects/user_story_list.html', context)


@login_required
def user_story_detail(request, pk):
    """
    Muestra el detalle de una historia de usuario.
    """
    user_story = get_object_or_404(UserStory, pk=pk)
    tasks = user_story.tasks.all()
    comments = user_story.comments.all()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user_story = user_story
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comentario agregado.')
            return redirect('user_story_detail', pk=pk)
    else:
        comment_form = CommentForm()

    context = {
        'user_story': user_story,
        'tasks': tasks,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'projects/user_story_detail.html', context)


@login_required
def user_story_create(request, project_pk):
    """
    Crea una nueva historia de usuario.
    """
    project = get_object_or_404(Project, pk=project_pk)

    if request.method == 'POST':
        form = UserStoryForm(request.POST, project=project)
        if form.is_valid():
            user_story = form.save(commit=False)
            user_story.project = project
            user_story.created_by = request.user
            user_story.save()
            messages.success(request, f'Historia de usuario "{user_story.title}" creada.')
            return redirect('user_story_detail', pk=user_story.pk)
    else:
        form = UserStoryForm(project=project)

    context = {
        'form': form,
        'project': project,
        'title': 'Crear Historia de Usuario',
    }
    return render(request, 'projects/user_story_form.html', context)


@login_required
def user_story_update(request, pk):
    """
    Actualiza una historia de usuario existente.
    """
    user_story = get_object_or_404(UserStory, pk=pk)

    if request.method == 'POST':
        form = UserStoryForm(request.POST, instance=user_story, project=user_story.project)
        if form.is_valid():
            form.save()
            messages.success(request, f'Historia "{user_story.title}" actualizada.')
            return redirect('user_story_detail', pk=user_story.pk)
    else:
        form = UserStoryForm(instance=user_story, project=user_story.project)

    context = {
        'form': form,
        'user_story': user_story,
        'title': 'Editar Historia de Usuario',
    }
    return render(request, 'projects/user_story_form.html', context)


# ===== VISTAS DE TAREA =====

@login_required
def task_create(request, user_story_pk):
    """
    Crea una nueva tarea para una historia de usuario.
    """
    user_story = get_object_or_404(UserStory, pk=user_story_pk)

    if request.method == 'POST':
        form = TaskForm(request.POST, user_story=user_story)
        if form.is_valid():
            task = form.save(commit=False)
            task.user_story = user_story
            task.save()
            messages.success(request, f'Tarea "{task.title}" creada.')
            return redirect('user_story_detail', pk=user_story.pk)
    else:
        form = TaskForm(user_story=user_story)

    context = {
        'form': form,
        'user_story': user_story,
        'title': 'Crear Tarea',
    }
    return render(request, 'projects/task_form.html', context)


@login_required
def task_update(request, pk):
    """
    Actualiza una tarea existente.
    """
    task = get_object_or_404(Task, pk=pk)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task, user_story=task.user_story)
        if form.is_valid():
            form.save()
            messages.success(request, f'Tarea "{task.title}" actualizada.')
            return redirect('user_story_detail', pk=task.user_story.pk)
    else:
        form = TaskForm(instance=task, user_story=task.user_story)

    context = {
        'form': form,
        'task': task,
        'title': 'Editar Tarea',
    }
    return render(request, 'projects/task_form.html', context)


# ===== VISTAS ADICIONALES =====

@login_required
def dashboard(request):
    """
    Dashboard principal con resumen de proyectos y tareas del usuario.
    """
    user_projects = Project.objects.filter(
        Q(team_members=request.user) |
        Q(product_owner=request.user) |
        Q(scrum_master=request.user)
    ).distinct()[:5]

    assigned_stories = UserStory.objects.filter(assigned_to=request.user)[:5]
    assigned_tasks = Task.objects.filter(assigned_to=request.user)[:5]

    context = {
        'user_projects': user_projects,
        'assigned_stories': assigned_stories,
        'assigned_tasks': assigned_tasks,
    }
    return render(request, 'projects/dashboard.html', context)
