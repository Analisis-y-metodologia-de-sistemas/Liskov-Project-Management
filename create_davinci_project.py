#!/usr/bin/env python
"""
Script para crear un proyecto de ejemplo del Sistema de Gestión de Alumnos
para el Colegio Da Vinci.
"""
import os
import sys
import django
from datetime import datetime, timedelta

# Configurar Django
sys.path.append('/Users/fede/Documents/GitHub/Liskov Project Management')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "liscov_pm.settings")
django.setup()

from django.contrib.auth.models import User
from django.utils import timezone
from projects.models import Project, Sprint, UserStory, Task, Comment


def create_davinci_project():
    """Crea un proyecto completo para el Sistema de Gestión de Alumnos del Colegio Da Vinci"""

    print("="*70)
    print("CREANDO PROYECTO: Sistema de Gestión de Alumnos - Colegio Da Vinci")
    print("="*70)

    # 1. Crear/Obtener usuarios
    print("\n1. Creando usuarios...")
    users_data = [
        {
            'username': 'laura.director',
            'email': 'laura.director@davinci.edu.ar',
            'first_name': 'Laura',
            'last_name': 'Fernández',
            'password': '1234'
        },
        {
            'username': 'martin.tech',
            'email': 'martin.tech@davinci.edu.ar',
            'first_name': 'Martín',
            'last_name': 'González',
            'password': '1234'
        },
        {
            'username': 'sofia.dev',
            'email': 'sofia.dev@davinci.edu.ar',
            'first_name': 'Sofía',
            'last_name': 'Romero',
            'password': '1234'
        },
        {
            'username': 'pablo.frontend',
            'email': 'pablo.frontend@davinci.edu.ar',
            'first_name': 'Pablo',
            'last_name': 'Mendoza',
            'password': '1234'
        },
        {
            'username': 'julia.backend',
            'email': 'julia.backend@davinci.edu.ar',
            'first_name': 'Julia',
            'last_name': 'Torres',
            'password': '1234'
        },
        {
            'username': 'diego.qa',
            'email': 'diego.qa@davinci.edu.ar',
            'first_name': 'Diego',
            'last_name': 'Acosta',
            'password': '1234'
        },
    ]

    users = []
    for user_data in users_data:
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults={
                'email': user_data['email'],
                'first_name': user_data['first_name'],
                'last_name': user_data['last_name'],
            }
        )
        if created:
            user.set_password(user_data['password'])
            user.save()
            print(f"   ✓ Usuario creado: {user.get_full_name()} ({user.username})")
        else:
            print(f"   → Usuario existente: {user.get_full_name()} ({user.username})")
        users.append(user)

    # 2. Crear proyecto
    print("\n2. Creando proyecto...")
    project, created = Project.objects.get_or_create(
        name='Sistema de Gestión de Alumnos - Colegio Da Vinci',
        defaults={
            'description': '''Desarrollo de una plataforma integral para la gestión educativa del Colegio Da Vinci.

El sistema permitirá:
- Gestión completa de datos de alumnos (inscripción, datos personales, historial académico)
- Registro de asistencias con reportes automáticos
- Sistema de calificaciones y evaluaciones
- Portal de padres para seguimiento del progreso académico
- Generación de reportes y estadísticas
- Sistema de notificaciones automáticas
- Gestión de cursos, materias y docentes

Tecnologías: Django 5.0, PostgreSQL, Bootstrap 5, Chart.js
Metodología: Scrum con sprints de 2 semanas''',
            'status': 'IN_PROGRESS',
            'start_date': timezone.now().date() - timedelta(days=35),
            'product_owner': users[0],  # Laura (Directora)
            'scrum_master': users[1],   # Martín (Tech Lead)
        }
    )

    if created:
        project.team_members.set([users[2], users[3], users[4], users[5]])
        project.save()
        print(f"   ✓ Proyecto creado: {project.name}")
    else:
        print(f"   → Proyecto existente: {project.name}")

    # 3. Crear sprints
    print("\n3. Creando sprints...")
    sprints_data = [
        {
            'name': 'Sprint 1 - Fundación y Arquitectura',
            'number': 1,
            'goal': 'Establecer la arquitectura base del sistema y el módulo de autenticación',
            'status': 'COMPLETED',
            'start_date': timezone.now().date() - timedelta(days=35),
            'end_date': timezone.now().date() - timedelta(days=21),
            'velocity': 42,
        },
        {
            'name': 'Sprint 2 - Gestión de Alumnos',
            'number': 2,
            'goal': 'Implementar CRUD completo de alumnos y módulo de inscripción',
            'status': 'COMPLETED',
            'start_date': timezone.now().date() - timedelta(days=20),
            'end_date': timezone.now().date() - timedelta(days=6),
            'velocity': 38,
        },
        {
            'name': 'Sprint 3 - Asistencias y Calificaciones',
            'number': 3,
            'goal': 'Desarrollar sistema de registro de asistencias y carga de calificaciones',
            'status': 'ACTIVE',
            'start_date': timezone.now().date() - timedelta(days=5),
            'end_date': timezone.now().date() + timedelta(days=9),
            'velocity': None,
        },
        {
            'name': 'Sprint 4 - Portal de Padres',
            'number': 4,
            'goal': 'Crear portal para que padres consulten información de sus hijos',
            'status': 'PLANNED',
            'start_date': timezone.now().date() + timedelta(days=10),
            'end_date': timezone.now().date() + timedelta(days=24),
            'velocity': None,
        },
    ]

    sprints = []
    for sprint_data in sprints_data:
        sprint, created = Sprint.objects.get_or_create(
            project=project,
            number=sprint_data['number'],
            defaults=sprint_data
        )
        if created:
            print(f"   ✓ Sprint creado: {sprint.name}")
        else:
            print(f"   → Sprint existente: {sprint.name}")
        sprints.append(sprint)

    # 4. Crear historias de usuario
    print("\n4. Creando historias de usuario...")
    stories_data = [
        # Sprint 1 - Completadas
        {
            'sprint': sprints[0],
            'title': 'Autenticación de usuarios',
            'description': 'Como administrador del sistema, quiero que los usuarios puedan iniciar sesión de forma segura para acceder al sistema según sus permisos.',
            'acceptance_criteria': '''- Login con username/email y contraseña
- Recuperación de contraseña por email
- Diferentes roles: Admin, Docente, Padre, Alumno
- Logout seguro
- Sesiones con timeout configurable''',
            'story_points': 13,
            'priority': 'CRITICAL',
            'status': 'DONE',
            'assigned_to': users[4],  # Julia (Backend)
        },
        {
            'sprint': sprints[0],
            'title': 'Diseño de base de datos',
            'description': 'Como desarrollador, quiero diseñar la estructura de base de datos para almacenar toda la información del sistema de forma normalizada.',
            'acceptance_criteria': '''- Modelo de datos completo
- Relaciones entre entidades definidas
- Índices para optimización
- Constraints de integridad
- Documentación del modelo''',
            'story_points': 8,
            'priority': 'CRITICAL',
            'status': 'DONE',
            'assigned_to': users[1],  # Martín (Tech Lead)
        },
        {
            'sprint': sprints[0],
            'title': 'Configuración del entorno de desarrollo',
            'description': 'Como desarrollador, quiero tener un entorno de desarrollo configurado para poder trabajar eficientemente.',
            'acceptance_criteria': '''- Django 5.0 configurado
- PostgreSQL instalado
- Git repository inicializado
- Requirements.txt creado
- Docker Compose para desarrollo''',
            'story_points': 5,
            'priority': 'HIGH',
            'status': 'DONE',
            'assigned_to': users[1],  # Martín
        },
        {
            'sprint': sprints[0],
            'title': 'Layout base del sistema',
            'description': 'Como usuario, quiero tener una interfaz coherente y moderna para navegar cómodamente por el sistema.',
            'acceptance_criteria': '''- Template base con Bootstrap 5
- Navbar responsive
- Sidebar con menú
- Footer con información
- Diseño mobile-first''',
            'story_points': 8,
            'priority': 'HIGH',
            'status': 'DONE',
            'assigned_to': users[3],  # Pablo (Frontend)
        },

        # Sprint 2 - Completadas
        {
            'sprint': sprints[1],
            'title': 'Registro de nuevo alumno',
            'description': 'Como secretaria, quiero poder registrar nuevos alumnos en el sistema para mantener actualizada la base de datos estudiantil.',
            'acceptance_criteria': '''- Formulario con validaciones
- Campos: Nombre, Apellido, DNI, Fecha nacimiento, Dirección, Teléfono, Email
- Campos de contacto de padres/tutores
- Validación de DNI único
- Foto del alumno (opcional)
- Generación automática de legajo''',
            'story_points': 13,
            'priority': 'CRITICAL',
            'status': 'DONE',
            'assigned_to': users[2],  # Sofía
        },
        {
            'sprint': sprints[1],
            'title': 'Listado y búsqueda de alumnos',
            'description': 'Como usuario del sistema, quiero poder buscar y listar alumnos para encontrar rápidamente la información que necesito.',
            'acceptance_criteria': '''- Tabla con paginación
- Búsqueda por nombre, apellido, DNI, legajo
- Filtros por curso, año, estado (activo/inactivo)
- Ordenamiento por columnas
- Export a Excel/PDF''',
            'story_points': 13,
            'priority': 'HIGH',
            'status': 'DONE',
            'assigned_to': users[2],  # Sofía
        },
        {
            'sprint': sprints[1],
            'title': 'Ficha completa del alumno',
            'description': 'Como docente o administrativo, quiero ver toda la información de un alumno para tener un panorama completo de su situación.',
            'acceptance_criteria': '''- Vista con datos personales
- Historial académico
- Registro de asistencias
- Calificaciones
- Observaciones y comentarios
- Documentación adjunta''',
            'story_points': 8,
            'priority': 'HIGH',
            'status': 'DONE',
            'assigned_to': users[3],  # Pablo
        },
        {
            'sprint': sprints[1],
            'title': 'Edición de datos del alumno',
            'description': 'Como secretaria, quiero poder modificar los datos de un alumno para mantener la información actualizada.',
            'acceptance_criteria': '''- Formulario de edición
- Validaciones
- Historial de cambios
- Permisos según rol
- Confirmación antes de guardar''',
            'story_points': 5,
            'priority': 'MEDIUM',
            'status': 'DONE',
            'assigned_to': users[2],  # Sofía
        },

        # Sprint 3 - En progreso
        {
            'sprint': sprints[2],
            'title': 'Registro de asistencias diarias',
            'description': 'Como docente, quiero registrar la asistencia de mis alumnos cada día para llevar un control preciso de la concurrencia.',
            'acceptance_criteria': '''- Planilla por curso y fecha
- Opciones: Presente, Ausente, Tarde, Justificado
- Guardado rápido
- Edición posterior permitida
- Validación de fecha (no futuras)''',
            'story_points': 13,
            'priority': 'CRITICAL',
            'status': 'IN_PROGRESS',
            'assigned_to': users[4],  # Julia
        },
        {
            'sprint': sprints[2],
            'title': 'Reportes de asistencia',
            'description': 'Como director, quiero ver reportes de asistencia para detectar problemas de ausentismo.',
            'acceptance_criteria': '''- Reporte por alumno
- Reporte por curso
- Gráficos estadísticos
- Filtros por fecha
- Detección de alertas (>3 faltas sin justificar)
- Export a PDF''',
            'story_points': 8,
            'priority': 'HIGH',
            'status': 'TODO',
            'assigned_to': users[2],  # Sofía
        },
        {
            'sprint': sprints[2],
            'title': 'Carga de calificaciones',
            'description': 'Como docente, quiero cargar las calificaciones de mis alumnos para que queden registradas en el sistema.',
            'acceptance_criteria': '''- Formulario por materia y periodo
- Escala configurable (1-10, conceptual, etc)
- Múltiples tipos de evaluación (escrito, oral, TP)
- Observaciones por nota
- Cálculo de promedios automático''',
            'story_points': 13,
            'priority': 'CRITICAL',
            'status': 'TODO',
            'assigned_to': users[4],  # Julia
        },
        {
            'sprint': sprints[2],
            'title': 'Boletín de calificaciones',
            'description': 'Como padre, quiero ver las calificaciones de mi hijo en un formato claro para hacer seguimiento de su rendimiento.',
            'acceptance_criteria': '''- Vista con todas las materias
- Calificaciones por trimestre
- Promedios generales
- Gráfico de evolución
- Comparación con promedio del curso
- Descarga en PDF''',
            'story_points': 8,
            'priority': 'MEDIUM',
            'status': 'TODO',
            'assigned_to': users[3],  # Pablo
        },

        # Backlog
        {
            'sprint': None,
            'title': 'Notificaciones automáticas por email',
            'description': 'Como padre, quiero recibir notificaciones por email sobre eventos importantes de mi hijo para estar informado.',
            'acceptance_criteria': '''- Email por inasistencias
- Email por calificaciones bajas
- Email por comunicados
- Configuración de preferencias
- Templates personalizables''',
            'story_points': 13,
            'priority': 'MEDIUM',
            'status': 'BACKLOG',
            'assigned_to': None,
        },
        {
            'sprint': None,
            'title': 'Portal de padres - Acceso web',
            'description': 'Como padre, quiero acceder a un portal web para consultar información de mi hijo desde cualquier lugar.',
            'acceptance_criteria': '''- Login seguro para padres
- Dashboard con resumen
- Acceso a asistencias
- Acceso a calificaciones
- Mensajería con docentes
- Calendario escolar''',
            'story_points': 21,
            'priority': 'HIGH',
            'status': 'BACKLOG',
            'assigned_to': None,
        },
        {
            'sprint': None,
            'title': 'Gestión de cursos y materias',
            'description': 'Como director, quiero gestionar los cursos y materias del colegio para organizar el año lectivo.',
            'acceptance_criteria': '''- CRUD de cursos
- CRUD de materias
- Asignación docente-materia
- Horarios de clases
- División en trimestres/cuatrimestres''',
            'story_points': 13,
            'priority': 'MEDIUM',
            'status': 'BACKLOG',
            'assigned_to': None,
        },
        {
            'sprint': None,
            'title': 'Dashboard con estadísticas',
            'description': 'Como director, quiero ver estadísticas generales del colegio para tomar decisiones informadas.',
            'acceptance_criteria': '''- Total de alumnos activos
- Promedio general de calificaciones
- Índice de asistencia
- Gráficos interactivos
- Comparativas entre cursos
- Exportación de datos''',
            'story_points': 13,
            'priority': 'MEDIUM',
            'status': 'BACKLOG',
            'assigned_to': None,
        },
        {
            'sprint': None,
            'title': 'App móvil para docentes',
            'description': 'Como docente, quiero una app móvil para tomar asistencia y cargar notas desde mi celular.',
            'acceptance_criteria': '''- App nativa iOS/Android
- Login seguro
- Toma de asistencia offline
- Carga de calificaciones
- Sincronización automática
- Notificaciones push''',
            'story_points': 34,
            'priority': 'LOW',
            'status': 'BACKLOG',
            'assigned_to': None,
        },
    ]

    user_stories = []
    for story_data in stories_data:
        story = UserStory.objects.create(
            project=project,
            sprint=story_data['sprint'],
            title=story_data['title'],
            description=story_data['description'],
            acceptance_criteria=story_data['acceptance_criteria'],
            story_points=story_data['story_points'],
            priority=story_data['priority'],
            status=story_data['status'],
            assigned_to=story_data['assigned_to'],
            created_by=users[0],  # Laura (Product Owner)
        )
        print(f"   ✓ Historia creada: {story.title} [{story.status}]")
        user_stories.append(story)

    # 5. Crear tareas para las historias que están en un sprint
    print("\n5. Creando tareas...")
    tasks_count = 0

    # Tareas para historias que están asignadas a un sprint (no BACKLOG)
    # En Scrum real, las historias se descomponen en tareas durante el Sprint Planning
    for story in user_stories:
        # Solo crear tareas si la historia está asignada a un sprint
        if story.sprint is not None:

            # Definir tareas según el estado de la historia
            if story.status == 'DONE':
                # Historias completadas: todas las tareas están terminadas
                tasks_templates = [
                    ('Diseñar mockups de interfaz', 'DONE', 3.0, 3.5),
                    ('Implementar modelos en Django', 'DONE', 4.0, 4.0),
                    ('Crear vistas y URLs', 'DONE', 4.0, 4.5),
                    ('Desarrollar templates HTML', 'DONE', 5.0, 5.0),
                    ('Escribir tests unitarios', 'DONE', 3.0, 3.0),
                    ('Documentar funcionalidad', 'DONE', 2.0, 2.0),
                ]
            elif story.status == 'IN_PROGRESS':
                # Historias en progreso: algunas tareas completadas, otras en curso
                tasks_templates = [
                    ('Diseñar mockups de interfaz', 'DONE', 3.0, 3.5),
                    ('Implementar modelos en Django', 'DONE', 4.0, 4.0),
                    ('Crear vistas y URLs', 'IN_PROGRESS', 4.0, None),
                    ('Desarrollar templates HTML', 'TODO', 5.0, None),
                    ('Escribir tests unitarios', 'TODO', 3.0, None),
                    ('Documentar funcionalidad', 'TODO', 2.0, None),
                ]
            else:  # TODO, IN_REVIEW, BLOCKED
                # Historias planificadas pero no iniciadas: todas las tareas pendientes
                tasks_templates = [
                    ('Diseñar mockups de interfaz', 'TODO', 3.0, None),
                    ('Implementar modelos en Django', 'TODO', 4.0, None),
                    ('Crear vistas y URLs', 'TODO', 4.0, None),
                    ('Desarrollar templates HTML', 'TODO', 5.0, None),
                    ('Escribir tests unitarios', 'TODO', 3.0, None),
                    ('Documentar funcionalidad', 'TODO', 2.0, None),
                ]

            # Crear 4-6 tareas dependiendo de los story points
            num_tasks = 6 if story.story_points >= 13 else 4
            for i in range(num_tasks):
                if i < len(tasks_templates):
                    task_title, task_status, estimated, actual = tasks_templates[i]

                    task = Task.objects.create(
                        user_story=story,
                        title=f'{task_title}',
                        description=f'Tarea relacionada con la historia: {story.title}',
                        status=task_status,
                        estimated_hours=estimated,
                        actual_hours=actual,
                        assigned_to=story.assigned_to,
                    )
                    tasks_count += 1

    print(f"   ✓ {tasks_count} tareas creadas")
    print(f"   → Las historias en BACKLOG no tienen tareas (se crean durante Sprint Planning)")

    # 6. Crear comentarios en las historias
    print("\n6. Creando comentarios...")
    comments_data = [
        'Excelente trabajo! Esta funcionalidad quedó muy bien implementada.',
        'Hay que revisar la validación del campo DNI, permite valores duplicados.',
        'Ya probé en mobile y funciona perfectamente.',
        'Encontré un bug cuando el alumno no tiene foto asignada.',
        'Agregué la documentación en el wiki del proyecto.',
        'Propongo mejorar el diseño de esta pantalla en el próximo sprint.',
        'Los tests están pasando correctamente en el CI/CD.',
        'Necesitamos validación adicional para el campo de email.',
    ]

    comments_count = 0
    for i, story in enumerate(user_stories[:10]):  # Comentarios en las primeras 10 historias
        if story.status != 'BACKLOG':
            # 2-3 comentarios por historia
            num_comments = 3 if story.status == 'DONE' else 2
            for j in range(num_comments):
                comment = Comment.objects.create(
                    user_story=story,
                    author=users[(i + j) % len(users)],
                    content=comments_data[(i + j) % len(comments_data)],
                )
                comments_count += 1

    print(f"   ✓ {comments_count} comentarios creados")

    # Resumen final
    print("\n" + "="*70)
    print("✓ PROYECTO CREADO EXITOSAMENTE")
    print("="*70)
    print(f"\nProyecto: {project.name}")
    print(f"Estado: {project.get_status_display()}")
    print(f"Product Owner: {project.product_owner.get_full_name()}")
    print(f"Scrum Master: {project.scrum_master.get_full_name()}")
    print(f"\nEstadísticas:")
    print(f"  - Sprints: {project.sprints.count()}")
    print(f"  - Historias de Usuario: {project.user_stories.count()}")
    print(f"  - Tareas: {Task.objects.filter(user_story__project=project).count()}")
    print(f"  - Comentarios: {Comment.objects.filter(user_story__project=project).count()}")

    print(f"\n\nUsuarios creados para el proyecto:")
    print("-" * 70)
    for user in users:
        print(f"  Username: {user.username:20} | Password: 1234")

    print("\n" + "="*70)
    print("Accede al sistema en: http://127.0.0.1:8000")
    print("="*70 + "\n")


if __name__ == '__main__':
    try:
        create_davinci_project()
    except Exception as e:
        print(f"\n❌ Error al crear el proyecto: {e}")
        import traceback
        traceback.print_exc()
