# Liscov Project Management

Sistema completo de gestión de proyectos Scrum desarrollado con Django, diseñado para demostrar las mejores prácticas de desarrollo web con el framework.

## 🎯 Objetivo

Este proyecto fue creado como material educativo para enseñar las mejores prácticas en el desarrollo de aplicaciones Django, implementando un sistema real de gestión de proyectos ágiles siguiendo la metodología Scrum.

## ✨ Características

### Gestión de Proyectos
- Creación y administración de proyectos Scrum
- Asignación de roles (Product Owner, Scrum Master, Equipo)
- Estados de proyecto (Planificación, En Progreso, En Pausa, Completado, Cancelado)
- Dashboard con resumen de proyectos activos

### Sprints
- Creación y seguimiento de sprints
- Objetivos y metas del sprint
- Control de velocidad del equipo
- Estados del sprint (Planificado, Activo, Completado, Cancelado)

### Historias de Usuario
- Product Backlog completo
- Formato estándar: "Como [rol], quiero [funcionalidad] para [beneficio]"
- Criterios de aceptación
- Estimación con puntos de historia
- Priorización (Baja, Media, Alta, Crítica)
- Estados del flujo de trabajo (Backlog, Por Hacer, En Progreso, En Revisión, Completada, Bloqueada)

### Tareas
- Descomposición de historias en tareas
- Estimación y seguimiento de horas
- Asignación a miembros del equipo

### Comentarios y Colaboración
- Sistema de comentarios en historias de usuario
- Historial de cambios
- Comunicación del equipo

## 🏗️ Arquitectura y Mejores Prácticas Implementadas

### Modelos
- ✅ Uso de `verbose_name` y `help_text` para documentación
- ✅ Choices para campos con opciones limitadas
- ✅ Validators para validación de datos
- ✅ Métodos `__str__` descriptivos
- ✅ Meta classes para configuración (ordering, verbose_name, unique_together)
- ✅ Related names descriptivos en ForeignKey y ManyToMany
- ✅ Uso apropiado de `on_delete` (CASCADE, PROTECT, SET_NULL)

### Vistas
- ✅ Decoradores `@login_required` para protección
- ✅ Uso de `get_object_or_404` para manejo de errores
- ✅ Messages framework para feedback al usuario
- ✅ Queries optimizadas con `Q` objects y `annotate`
- ✅ Validación de permisos a nivel de vista
- ✅ Separación de lógica por entidad

### Formularios
- ✅ ModelForms para validación automática
- ✅ Widgets personalizados con Bootstrap
- ✅ Validación personalizada en método `clean()`
- ✅ Inicialización dinámica con `__init__`
- ✅ Filtrado de querysets por contexto
- ✅ Uso de Crispy Forms para rendering

### Admin
- ✅ Admin personalizado con `@admin.register`
- ✅ `list_display` para columnas importantes
- ✅ `list_filter` y `search_fields` para búsqueda
- ✅ `readonly_fields` para campos auto-generados
- ✅ `fieldsets` para organización
- ✅ Métodos personalizados para display
- ✅ `filter_horizontal` para ManyToMany

### Templates
- ✅ Template base con herencia
- ✅ Bloques para extensibilidad
- ✅ Uso de Bootstrap 5 para diseño responsive
- ✅ Bootstrap Icons para iconografía
- ✅ Mensajes flash con framework de messages
- ✅ Breadcrumbs para navegación
- ✅ Cards y componentes modernos

### Configuración
- ✅ Uso de `python-decouple` para variables de entorno
- ✅ Separación de settings sensibles
- ✅ Configuración de archivos estáticos y media
- ✅ Internacionalización (i18n)
- ✅ Zona horaria configurada
- ✅ INSTALLED_APPS organizado por secciones

### URLs
- ✅ Nombres descriptivos para reverse()
- ✅ Separación por app con include()
- ✅ Patrones RESTful
- ✅ Organización lógica por entidad

## 🚀 Instalación

### Requisitos Previos
- Python 3.11 o superior
- pip
- Virtualenv (recomendado)

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone <url-repositorio>
cd "Biblioteca Django"
```

2. **Crear y activar entorno virtual**
```bash
python3 -m venv venv
source venv/bin/activate  # En Linux/Mac
# o
venv\Scripts\activate  # En Windows
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno** (opcional)
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

5. **Aplicar migraciones**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Crear superusuario**
```bash
python manage.py createsuperuser
```

7. **Cargar datos de prueba** (opcional)
```bash
python manage.py loaddata fixtures/initial_data.json
```

8. **Ejecutar el servidor de desarrollo**
```bash
python manage.py runserver
```

9. **Acceder a la aplicación**
- Aplicación: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## 👥 Usuarios de Prueba

Correr el script create_davinci_project.py y despues update_passwords.py

El sistema incluye usuarios de prueba con datos de ejemplo. Todos los usuarios usan la contraseña: **`1234`**

### Proyecto: Sistema de Gestión de Alumnos - Colegio Da Vinci

| Username | Nombre Completo | Rol | Contraseña |
|----------|----------------|-----|------------|
| `laura.director` | Laura Fernández | Product Owner (Directora) | `1234` |
| `martin.tech` | Martín González | Scrum Master (Tech Lead) | `1234` |
| `sofia.dev` | Sofía Romero | Desarrolladora | `1234` |
| `pablo.frontend` | Pablo Mendoza | Desarrollador Frontend | `1234` |
| `julia.backend` | Julia Torres | Desarrolladora Backend | `1234` |
| `diego.qa` | Diego Acosta | QA Tester | `1234` |

### Otros Proyectos de Ejemplo

| Username | Nombre Completo | Contraseña |
|----------|----------------|------------|
| `maria.garcia` | Maria Garcia | `1234` |
| `juan.lopez` | Juan Lopez | `1234` |
| `ana.martinez` | Ana Martinez | `1234` |
| `carlos.rodriguez` | Carlos Rodriguez | `1234` |
| `lucia.fernandez` | Lucia Fernandez | `1234` |
| `diego.sanchez` | Diego Sanchez | `1234` |

### 📝 Datos de Ejemplo Incluidos

El proyecto incluye un ejemplo completo del **Sistema de Gestión de Alumnos para el Colegio Da Vinci** que demuestra:

- **4 Sprints** (2 completados, 1 activo, 1 planificado)
- **17 Historias de Usuario** distribuidas en diferentes estados
- **43 Tareas** con estimaciones y seguimiento de horas
- **28 Comentarios** de colaboración entre el equipo

#### Características del Proyecto Da Vinci

El proyecto de ejemplo implementa un sistema integral que incluye:
- Gestión completa de datos de alumnos
- Registro de asistencias con reportes automáticos
- Sistema de calificaciones y evaluaciones
- Portal de padres para seguimiento académico
- Dashboard con estadísticas
- Sistema de notificaciones

Para explorar este proyecto, inicia sesión con cualquiera de los usuarios del equipo Da Vinci listados arriba.

## 📦 Dependencias Principales

- **Django 5.2**: Framework web principal
- **django-crispy-forms**: Rendering de formularios
- **crispy-bootstrap5**: Templates Bootstrap 5 para crispy-forms
- **python-decouple**: Gestión de variables de entorno
- **Pillow**: Procesamiento de imágenes

## 📚 Estructura del Proyecto

```
Biblioteca Django/
├── liscov_pm/              # Configuración del proyecto
│   ├── settings.py         # Configuración principal
│   ├── urls.py            # URLs raíz
│   └── wsgi.py            # WSGI entry point
├── projects/              # App principal
│   ├── models.py          # Modelos (Project, Sprint, UserStory, Task, Comment)
│   ├── views.py           # Vistas
│   ├── forms.py           # Formularios
│   ├── admin.py           # Configuración del admin
│   └── urls.py            # URLs de la app
├── templates/             # Templates HTML
│   ├── base.html          # Template base
│   ├── registration/      # Templates de autenticación
│   └── projects/          # Templates de la app
├── static/                # Archivos estáticos
│   ├── css/               # Hojas de estilo
│   └── js/                # JavaScript
├── media/                 # Archivos subidos por usuarios
├── requirements.txt       # Dependencias Python
└── manage.py             # Script de gestión Django
```

## 🎓 Conceptos Educativos Demostrados

### 1. Modelos y ORM
- Relaciones uno a muchos (ForeignKey)
- Relaciones muchos a muchos (ManyToManyField)
- Validadores personalizados
- Métodos de modelo
- Meta opciones

### 2. Vistas y URLs
- Function-based views
- Decoradores de autorización
- Manejo de formularios POST/GET
- Queries complejas con Q objects
- Anotaciones y agregaciones

### 3. Formularios
- ModelForms
- Validación de formularios
- Widgets personalizados
- Formularios con contexto dinámico

### 4. Templates
- Herencia de templates
- Template tags y filters
- Contexto de templates
- Bootstrap integration

### 5. Admin
- Personalización del admin
- Inlines
- Actions personalizadas
- Filtros y búsqueda

### 6. Seguridad
- Autenticación y autorización
- CSRF protection
- Validación de permisos
- SQL injection prevention (ORM)

### 7. Mejores Prácticas
- DRY (Don't Repeat Yourself)
- Separación de concerns
- Código limpio y documentado
- Manejo de errores
- Mensajes al usuario

## 🔧 Configuración Avanzada

### Variables de Entorno

Crear un archivo `.env` en la raíz del proyecto:

```env
SECRET_KEY=tu-secret-key-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

### Base de Datos

Por defecto usa SQLite. Para usar PostgreSQL:

1. Instalar psycopg2:
```bash
pip install psycopg2-binary
```

2. Configurar en `.env`:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

## 🧪 Testing

```bash
# Ejecutar todos los tests
python manage.py test

# Test de una app específica
python manage.py test projects

# Test con coverage
coverage run --source='.' manage.py test
coverage report
```

## 📖 Uso del Sistema

### Flujo de Trabajo Recomendado

1. **Crear un Proyecto**
   - Definir Product Owner y Scrum Master
   - Agregar miembros del equipo
   - Establecer fechas

2. **Crear Product Backlog**
   - Agregar historias de usuario
   - Definir criterios de aceptación
   - Priorizar historias

3. **Planificar Sprint**
   - Crear nuevo sprint
   - Asignar historias al sprint
   - Estimar puntos de historia

4. **Durante el Sprint**
   - Crear tareas para cada historia
   - Actualizar estados
   - Agregar comentarios

5. **Finalizar Sprint**
   - Marcar historias como completadas
   - Registrar velocidad
   - Preparar siguiente sprint

## 🤝 Contribuciones

Este es un proyecto educativo. Las contribuciones son bienvenidas para:
- Mejorar la documentación
- Agregar tests
- Optimizar código
- Agregar nuevas características

## 🎯 Roadmap

### Características Futuras
- [ ] API REST con Django REST Framework
- [ ] WebSockets para actualizaciones en tiempo real
- [ ] Gráficos de burndown chart
- [ ] Exportación de informes
- [ ] Notificaciones por email
- [ ] Integración con herramientas externas (GitHub, Slack)
- [ ] Tests unitarios y de integración
- [ ] Docker containerization
- [ ] CI/CD pipeline

## 📚 Recursos Adicionales

- [Documentación de Django](https://docs.djangoproject.com/)
- [Guía de Scrum](https://scrumguides.org/)
- [Bootstrap 5 Docs](https://getbootstrap.com/docs/5.3/)
- [Python Best Practices](https://docs.python-guide.org/)

---

**Nota**: Este proyecto está en constante evolución y se actualiza regularmente con nuevas características y mejoras basadas en el feedback de los estudiantes.
