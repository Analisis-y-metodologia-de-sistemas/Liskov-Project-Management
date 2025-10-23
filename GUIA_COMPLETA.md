# Guía Completa - Liscov Project Management
## Sistema de Gestión de Proyectos Scrum con Django

---

## 📋 Tabla de Contenidos

1. [Introducción](#introducción)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Instalación y Configuración](#instalación-y-configuración)
4. [Modelos de Datos](#modelos-de-datos)
5. [Vistas y Lógica de Negocio](#vistas-y-lógica-de-negocio)
6. [Formularios](#formularios)
7. [Templates y Frontend](#templates-y-frontend)
8. [Administración](#administración)
9. [Datos de Ejemplo](#datos-de-ejemplo)
10. [Mejores Prácticas Implementadas](#mejores-prácticas-implementadas)
11. [Ejercicios Prácticos](#ejercicios-prácticos)

---

## 1. Introducción

### 1.1 Objetivo del Proyecto

Este proyecto fue diseñado como **material educativo** para enseñar Django siguiendo las mejores prácticas de la industria. Implementa un sistema completo de gestión de proyectos basado en la metodología Scrum.

### 1.2 Tecnologías Utilizadas

- **Django 5.2**: Framework web principal
- **Bootstrap 5**: Framework CSS para diseño responsive
- **Python 3.11+**: Lenguaje de programación
- **SQLite**: Base de datos (desarrollo)
- **Django Crispy Forms**: Rendering avanzado de formularios

### 1.3 Características Principales

- ✅ Gestión completa de proyectos Scrum
- ✅ Sprints con objetivos y velocidad
- ✅ Product Backlog y Sprint Backlog
- ✅ Historias de usuario con criterios de aceptación
- ✅ Tareas con estimación de horas
- ✅ Sistema de comentarios
- ✅ Roles de equipo (PO, SM, Equipo)
- ✅ Dashboard interactivo
- ✅ Administración personalizada

---

## 2. Arquitectura del Sistema

### 2.1 Estructura del Proyecto

```
Biblioteca Django/
├── liscov_pm/                 # Configuración principal
│   ├── settings.py           # Configuración del proyecto
│   ├── urls.py               # URLs principales
│   └── wsgi.py               # Entry point WSGI
│
├── projects/                  # Aplicación principal
│   ├── models.py             # Modelos de datos
│   ├── views.py              # Lógica de vistas
│   ├── forms.py              # Formularios
│   ├── admin.py              # Configuración admin
│   ├── urls.py               # URLs de la app
│   └── management/           # Comandos personalizados
│       └── commands/
│           └── create_sample_data.py
│
├── templates/                 # Templates HTML
│   ├── base.html             # Template base
│   ├── registration/         # Login/Logout
│   └── projects/             # Templates de la app
│       ├── dashboard.html
│       ├── project_list.html
│       ├── project_detail.html
│       └── ...
│
├── static/                    # Archivos estáticos
│   ├── css/
│   │   └── custom.css
│   └── js/
│
├── media/                     # Archivos subidos
│
├── requirements.txt           # Dependencias
├── .env.example              # Variables de entorno
├── .gitignore                # Archivos ignorados
└── README.md                 # Documentación
```

### 2.2 Patrón MVT (Model-View-Template)

Django utiliza el patrón MVT:

- **Model (Modelo)**: Define la estructura de datos
- **View (Vista)**: Contiene la lógica de negocio
- **Template**: Presenta la información al usuario

---

## 3. Instalación y Configuración

### 3.1 Requisitos Previos

```bash
# Verificar versión de Python
python3 --version  # Debe ser 3.11+

# Verificar pip
pip3 --version
```

### 3.2 Instalación Paso a Paso

#### Paso 1: Clonar el Repositorio

```bash
git clone <url-repositorio>
cd "Biblioteca Django"
```

#### Paso 2: Crear Entorno Virtual

```bash
# Crear entorno virtual
python3 -m venv venv

# Activar (Linux/Mac)
source venv/bin/activate

# Activar (Windows)
venv\Scripts\activate
```

#### Paso 3: Instalar Dependencias

```bash
pip install -r requirements.txt
```

**Dependencias instaladas:**
- Django>=5.0,<6.0
- django-crispy-forms>=2.1
- crispy-bootstrap5>=2.0
- Pillow>=10.0
- python-decouple>=3.8

#### Paso 4: Configurar Variables de Entorno (Opcional)

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env
SECRET_KEY=tu-clave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

#### Paso 5: Aplicar Migraciones

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate
```

#### Paso 6: Crear Superusuario

```bash
python manage.py createsuperuser
# Seguir las instrucciones en pantalla
```

#### Paso 7: Cargar Datos de Ejemplo

```bash
# Crear datos de ejemplo
python manage.py create_sample_data

# O limpiar y crear nuevos datos
python manage.py create_sample_data --clean
```

#### Paso 8: Ejecutar Servidor

```bash
python manage.py runserver
```

**Acceder a:**
- Aplicación: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

---

## 4. Modelos de Datos

### 4.1 Diagrama de Relaciones

```
User (Django Auth)
  ↓
Project ──┬── Sprint ──── UserStory ──┬── Task
          │                           │
          └── (team_members)          └── Comment
```

### 4.2 Modelo: Project

**Propósito**: Representa un proyecto Scrum completo.

```python
class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    product_owner = models.ForeignKey(User, on_delete=models.PROTECT)
    scrum_master = models.ForeignKey(User, on_delete=models.PROTECT)
    team_members = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

**Estados posibles:**
- PLANNING: Planificación
- IN_PROGRESS: En Progreso
- ON_HOLD: En Pausa
- COMPLETED: Completado
- CANCELLED: Cancelado

**Mejores prácticas aplicadas:**
✅ `verbose_name` para nombres legibles
✅ `help_text` para documentación
✅ `choices` para campos limitados
✅ `related_name` descriptivos
✅ `on_delete=PROTECT` para datos críticos

### 4.3 Modelo: Sprint

**Propósito**: Representa un sprint dentro de un proyecto.

```python
class Sprint(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    number = models.PositiveIntegerField()
    goal = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    velocity = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        unique_together = [['project', 'number']]
```

**Estados:**
- PLANNED: Planificado
- ACTIVE: Activo
- COMPLETED: Completado
- CANCELLED: Cancelado

**Características importantes:**
- `unique_together`: Evita duplicación de números de sprint
- `velocity`: Puntos de historia completados

### 4.4 Modelo: UserStory

**Propósito**: Historia de usuario siguiendo formato estándar.

```python
class UserStory(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    sprint = models.ForeignKey(Sprint, on_delete=models.SET_NULL,
                               null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    acceptance_criteria = models.TextField()
    story_points = models.PositiveIntegerField(null=True, blank=True)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL,
                                   null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
```

**Prioridades:**
- LOW: Baja
- MEDIUM: Media
- HIGH: Alta
- CRITICAL: Crítica

**Estados del flujo:**
- BACKLOG: Product Backlog
- TODO: Por Hacer
- IN_PROGRESS: En Progreso
- IN_REVIEW: En Revisión
- DONE: Completada
- BLOCKED: Bloqueada

### 4.5 Modelo: Task

**Propósito**: Tareas técnicas para implementar historias.

```python
class Task(models.Model):
    user_story = models.ForeignKey(UserStory, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    estimated_hours = models.DecimalField(max_digits=5, decimal_places=2)
    actual_hours = models.DecimalField(max_digits=5, decimal_places=2)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL,
                                   null=True, blank=True)
```

### 4.6 Modelo: Comment

**Propósito**: Sistema de comentarios para colaboración.

```python
class Comment(models.Model):
    user_story = models.ForeignKey(UserStory, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
```

---

## 5. Vistas y Lógica de Negocio

### 5.1 Vista: Dashboard

**Archivo**: `projects/views.py`

```python
@login_required
def dashboard(request):
    """Dashboard principal con resumen del usuario"""
    user_projects = Project.objects.filter(
        Q(team_members=request.user) |
        Q(product_owner=request.user) |
        Q(scrum_master=request.user)
    ).distinct()[:5]

    assigned_stories = UserStory.objects.filter(
        assigned_to=request.user
    )[:5]

    assigned_tasks = Task.objects.filter(
        assigned_to=request.user
    )[:5]

    return render(request, 'projects/dashboard.html', {
        'user_projects': user_projects,
        'assigned_stories': assigned_stories,
        'assigned_tasks': assigned_tasks,
    })
```

**Mejores prácticas:**
- ✅ `@login_required` para protección
- ✅ `Q` objects para consultas complejas
- ✅ `.distinct()` para evitar duplicados
- ✅ Limitar resultados con `[:5]`

### 5.2 Vista: Project Detail

```python
@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)

    # Verificar permisos
    if not (request.user in project.team_members.all() or
            request.user == project.product_owner or
            request.user == project.scrum_master):
        messages.error(request, 'No tienes permiso para ver este proyecto.')
        return redirect('project_list')

    sprints = project.sprints.all()[:5]
    user_stories = project.user_stories.all()[:10]

    return render(request, 'projects/project_detail.html', {
        'project': project,
        'sprints': sprints,
        'user_stories': user_stories,
    })
```

**Características importantes:**
- ✅ Validación de permisos
- ✅ Mensajes de error
- ✅ `get_object_or_404` para manejo de errores

### 5.3 Vista: Create/Update con Formularios

```python
@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            messages.success(request,
                f'Proyecto "{project.name}" creado exitosamente.')
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectForm()

    return render(request, 'projects/project_form.html', {
        'form': form,
        'title': 'Crear Proyecto',
    })
```

**Patrón POST-Redirect-GET:**
1. GET: Mostrar formulario vacío
2. POST: Procesar datos
3. Redirect: Prevenir doble envío

---

## 6. Formularios

### 6.1 ProjectForm

```python
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'name', 'description', 'status',
            'start_date', 'end_date',
            'product_owner', 'scrum_master',
            'team_members'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            # ...
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and end_date < start_date:
            raise forms.ValidationError(
                'La fecha de fin no puede ser anterior a la fecha de inicio.'
            )

        return cleaned_data
```

**Mejores prácticas:**
- ✅ Widgets personalizados con Bootstrap
- ✅ Validación en `clean()`
- ✅ Mensajes de error descriptivos

### 6.2 SprintForm con Lógica Dinámica

```python
class SprintForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project', None)
        super().__init__(*args, **kwargs)

        if self.project and not self.instance.pk:
            # Sugerir siguiente número de sprint
            last_sprint = Sprint.objects.filter(
                project=self.project
            ).order_by('-number').first()

            if last_sprint:
                self.fields['number'].initial = last_sprint.number + 1
            else:
                self.fields['number'].initial = 1
```

**Características:**
- ✅ Inicialización dinámica en `__init__`
- ✅ Contexto del proyecto
- ✅ Sugerencia inteligente de valores

---

## 7. Templates y Frontend

### 7.1 Template Base

```django
{% load static %}
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}Liscov PM{% endblock %}</title>

    <!-- Bootstrap 5 -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

    <!-- Bootstrap Icons -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css">

    <!-- Custom CSS -->
    <link rel="stylesheet" href="{% static 'css/custom.css' %}">

    {% block extra_css %}{% endblock %}
</head>
<body>
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <!-- Contenido del navbar -->
    </nav>

    <!-- Messages -->
    {% if messages %}
    <div class="container mt-3">
        {% for message in messages %}
        <div class="alert alert-{{ message.tags }} alert-dismissible fade show">
            {{ message }}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
        {% endfor %}
    </div>
    {% endif %}

    <!-- Content -->
    <main class="container-fluid py-4">
        {% block content %}{% endblock %}
    </main>

    <!-- Footer -->
    <footer class="bg-light text-center py-3">
        <!-- Contenido del footer -->
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
```

### 7.2 Template de Lista

```django
{% extends 'base.html' %}

{% block content %}
<div class="container">
    <div class="row mb-4">
        <div class="col">
            <h1><i class="bi bi-folder"></i> Proyectos</h1>
        </div>
        <div class="col-auto">
            <a href="{% url 'project_create' %}" class="btn btn-primary">
                <i class="bi bi-plus-circle"></i> Nuevo Proyecto
            </a>
        </div>
    </div>

    {% if projects %}
    <div class="row">
        {% for project in projects %}
        <div class="col-md-6 col-lg-4 mb-4">
            <div class="card h-100 shadow-sm">
                <div class="card-body">
                    <h5 class="card-title">{{ project.name }}</h5>
                    <p class="card-text">
                        {{ project.description|truncatewords:20 }}
                    </p>
                    <span class="badge bg-info">
                        {{ project.get_status_display }}
                    </span>
                </div>
                <div class="card-footer">
                    <a href="{% url 'project_detail' project.pk %}"
                       class="btn btn-sm btn-primary w-100">
                        <i class="bi bi-eye"></i> Ver Proyecto
                    </a>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
    {% else %}
    <div class="alert alert-info">
        No hay proyectos disponibles.
    </div>
    {% endif %}
</div>
{% endblock %}
```

**Elementos clave:**
- ✅ Herencia de templates con `extends`
- ✅ Bloques para contenido dinámico
- ✅ Template tags (`url`, `static`)
- ✅ Template filters (`truncatewords`)
- ✅ Bootstrap 5 components

---

## 8. Administración

### 8.1 Admin Personalizado

```python
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'status', 'product_owner',
        'scrum_master', 'start_date', 'created_at'
    ]
    list_filter = ['status', 'start_date', 'created_at']
    search_fields = [
        'name', 'description',
        'product_owner__username',
        'scrum_master__username'
    ]
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['team_members']

    fieldsets = (
        ('Información General', {
            'fields': ('name', 'description', 'status')
        }),
        ('Fechas', {
            'fields': ('start_date', 'end_date')
        }),
        ('Roles Scrum', {
            'fields': ('product_owner', 'scrum_master', 'team_members')
        }),
        ('Metadatos', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
```

**Características del Admin:**
- ✅ `list_display`: Columnas visibles
- ✅ `list_filter`: Filtros laterales
- ✅ `search_fields`: Búsqueda
- ✅ `readonly_fields`: Campos solo lectura
- ✅ `filter_horizontal`: Widget para M2M
- ✅ `fieldsets`: Organización visual

### 8.2 Métodos Personalizados en Admin

```python
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        'author', 'user_story',
        'created_at', 'content_preview'
    ]

    def content_preview(self, obj):
        """Muestra preview del contenido"""
        max_length = 50
        if len(obj.content) > max_length:
            return obj.content[:max_length] + '...'
        return obj.content

    content_preview.short_description = 'Vista previa'
```

---

## 9. Datos de Ejemplo

### 9.1 Comando Personalizado

El sistema incluye un comando para crear datos de ejemplo:

```bash
# Crear datos de ejemplo
python manage.py create_sample_data

# Limpiar y crear nuevos datos
python manage.py create_sample_data --clean
```

### 9.2 Usuarios Creados

| Username | Email | Nombre | Password |
|----------|-------|--------|----------|
| maria.garcia | maria.garcia@example.com | Maria Garcia | demo1234 |
| juan.lopez | juan.lopez@example.com | Juan Lopez | demo1234 |
| ana.martinez | ana.martinez@example.com | Ana Martinez | demo1234 |
| carlos.rodriguez | carlos.rodriguez@example.com | Carlos Rodriguez | demo1234 |
| lucia.fernandez | lucia.fernandez@example.com | Lucia Fernandez | demo1234 |
| diego.sanchez | diego.sanchez@example.com | Diego Sanchez | demo1234 |

### 9.3 Proyectos Creados

#### 1. Sistema de E-commerce
- **Estado**: En Progreso
- **Sprints**: 3 (2 completados, 1 activo)
- **Historias**: 5
- **Product Owner**: Maria Garcia
- **Scrum Master**: Juan Lopez

**Sprints:**
- Sprint 1: Fundamentos ✅
- Sprint 2: Catálogo ✅
- Sprint 3: Carrito 🔄

#### 2. App Móvil de Delivery
- **Estado**: En Progreso
- **Sprints**: 2 (1 completado, 1 activo)
- **Historias**: 4
- **Product Owner**: Juan Lopez
- **Scrum Master**: Ana Martinez

#### 3. Portal Educativo Online
- **Estado**: Planificación
- **Sprints**: 1 (planificado)
- **Historias**: 3
- **Product Owner**: Ana Martinez
- **Scrum Master**: Carlos Rodriguez

### 9.4 Estadísticas de Datos

```
📊 Total de Datos Creados:
- 6 Usuarios
- 3 Proyectos
- 6 Sprints
- 12 Historias de Usuario
- 14 Tareas
- 21 Comentarios
```

---

## 10. Mejores Prácticas Implementadas

### 10.1 Modelos

✅ **Uso de verbose_name**
```python
name = models.CharField(
    max_length=200,
    verbose_name=_('Nombre')
)
```

✅ **Help text descriptivo**
```python
story_points = models.PositiveIntegerField(
    help_text='Estimación de complejidad (1-100)'
)
```

✅ **Choices para opciones limitadas**
```python
status = models.CharField(
    max_length=20,
    choices=STATUS_CHOICES,
    default='PLANNING'
)
```

✅ **Validators personalizados**
```python
story_points = models.PositiveIntegerField(
    validators=[
        MinValueValidator(1),
        MaxValueValidator(100)
    ]
)
```

✅ **Related names descriptivos**
```python
product_owner = models.ForeignKey(
    User,
    on_delete=models.PROTECT,
    related_name='owned_projects'
)
```

### 10.2 Vistas

✅ **Decoradores de seguridad**
```python
@login_required
def view_name(request):
    pass
```

✅ **get_object_or_404**
```python
project = get_object_or_404(Project, pk=pk)
```

✅ **Mensajes al usuario**
```python
messages.success(request, 'Operación exitosa')
messages.error(request, 'Error en la operación')
```

✅ **Queries optimizadas**
```python
projects = Project.objects.filter(
    Q(team_members=request.user) |
    Q(product_owner=request.user)
).distinct().annotate(
    story_count=Count('user_stories')
)
```

### 10.3 Formularios

✅ **Validación personalizada**
```python
def clean(self):
    cleaned_data = super().clean()
    # Validaciones personalizadas
    return cleaned_data
```

✅ **Widgets con Bootstrap**
```python
widgets = {
    'name': forms.TextInput(attrs={
        'class': 'form-control'
    })
}
```

### 10.4 Templates

✅ **Herencia de templates**
```django
{% extends 'base.html' %}
```

✅ **Template tags**
```django
{% url 'project_detail' project.pk %}
{% static 'css/custom.css' %}
```

✅ **Template filters**
```django
{{ project.description|truncatewords:20 }}
{{ project.created_at|date:"d/m/Y" }}
```

### 10.5 Seguridad

✅ **CSRF Protection**
```django
<form method="post">
    {% csrf_token %}
    <!-- campos -->
</form>
```

✅ **SQL Injection Prevention** (ORM)
✅ **XSS Prevention** (auto-escape)
✅ **Variables de entorno** (python-decouple)

---

## 11. Ejercicios Prácticos

### Ejercicio 1: Agregar Campo a Modelo

**Objetivo**: Agregar un campo `budget` (presupuesto) al modelo Project.

**Pasos:**
1. Modificar `projects/models.py`
2. Ejecutar `makemigrations`
3. Ejecutar `migrate`
4. Actualizar formulario
5. Actualizar templates

**Solución:**
```python
# models.py
budget = models.DecimalField(
    max_digits=10,
    decimal_places=2,
    null=True,
    blank=True,
    verbose_name='Presupuesto'
)
```

### Ejercicio 2: Nueva Vista de Búsqueda

**Objetivo**: Crear una vista para buscar historias de usuario.

**Requerimientos:**
- Búsqueda por título
- Filtro por prioridad
- Filtro por estado
- Template con formulario de búsqueda

**Pista:**
```python
def user_story_search(request):
    query = request.GET.get('q', '')
    priority = request.GET.get('priority', '')

    stories = UserStory.objects.all()

    if query:
        stories = stories.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )

    if priority:
        stories = stories.filter(priority=priority)

    # ...
```

### Ejercicio 3: Reportes de Sprint

**Objetivo**: Crear una vista de reporte de sprint con métricas.

**Métricas a calcular:**
- Puntos planificados vs completados
- Burndown básico
- Historias por estado
- Eficiencia del equipo

### Ejercicio 4: API REST Simple

**Objetivo**: Crear un endpoint API para listar proyectos en JSON.

**Requerimientos:**
- Endpoint: `/api/projects/`
- Respuesta en JSON
- Solo usuarios autenticados

**Solución:**
```python
from django.http import JsonResponse

@login_required
def projects_api(request):
    projects = Project.objects.filter(
        team_members=request.user
    ).values('id', 'name', 'status')

    return JsonResponse({
        'projects': list(projects)
    })
```

### Ejercicio 5: Tests Unitarios

**Objetivo**: Escribir tests para el modelo Project.

```python
from django.test import TestCase
from django.contrib.auth.models import User
from projects.models import Project

class ProjectModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test',
            password='test123'
        )

    def test_create_project(self):
        project = Project.objects.create(
            name='Test Project',
            description='Test',
            status='PLANNING',
            start_date='2024-01-01',
            product_owner=self.user,
            scrum_master=self.user
        )

        self.assertEqual(project.name, 'Test Project')
        self.assertEqual(project.status, 'PLANNING')
```

---

## 12. Recursos Adicionales

### 12.1 Documentación Oficial

- [Django Documentation](https://docs.djangoproject.com/)
- [Bootstrap 5 Docs](https://getbootstrap.com/docs/5.3/)
- [Python Documentation](https://docs.python.org/3/)

### 12.2 Comandos Útiles

```bash
# Desarrollo
python manage.py runserver
python manage.py shell
python manage.py dbshell

# Base de datos
python manage.py makemigrations
python manage.py migrate
python manage.py showmigrations

# Testing
python manage.py test
python manage.py test projects

# Datos
python manage.py create_sample_data
python manage.py create_sample_data --clean

# Producción
python manage.py collectstatic
python manage.py check --deploy
```

### 12.3 Troubleshooting

**Problema**: Error de migraciones
```bash
# Solución: Resetear migraciones
python manage.py migrate --fake projects zero
python manage.py migrate projects
```

**Problema**: Puerto ocupado
```bash
# Solución: Usar otro puerto
python manage.py runserver 8080
```

**Problema**: Static files no cargan
```bash
# Solución: Recolectar archivos estáticos
python manage.py collectstatic --noinput
```

---

## 13. Conclusión

Este proyecto demuestra una implementación completa de Django siguiendo las mejores prácticas de la industria. Los estudiantes pueden aprender:

1. ✅ Arquitectura MVT de Django
2. ✅ ORM y modelado de datos
3. ✅ Vistas basadas en funciones
4. ✅ Sistema de templates
5. ✅ Formularios y validación
6. ✅ Admin personalizado
7. ✅ Autenticación y permisos
8. ✅ Manejo de archivos estáticos
9. ✅ Comandos personalizados
10. ✅ Mejores prácticas de seguridad

---

## 📞 Soporte

Para preguntas o sugerencias sobre este proyecto educativo:
- Consultar la documentación en `README.md`
- Revisar los comentarios en el código
- Contactar al docente de la materia

---

**Desarrollado con ❤️ para enseñar Django**

*Última actualización: 2024*
