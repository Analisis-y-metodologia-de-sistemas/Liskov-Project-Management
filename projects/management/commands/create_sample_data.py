from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from projects.models import Project, Sprint, UserStory, Task, Comment
from datetime import datetime, timedelta
from django.utils import timezone


class Command(BaseCommand):
    """
    Comando personalizado para crear datos de ejemplo.
    Mejores practicas:
    - Comando reutilizable
    - Mensajes informativos con self.stdout
    - Manejo de errores
    - Datos realistas
    """
    help = 'Crea datos de ejemplo para el sistema de gestion de proyectos'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clean',
            action='store_true',
            help='Elimina todos los datos antes de crear los nuevos',
        )

    def handle(self, *args, **options):
        if options['clean']:
            self.stdout.write(self.style.WARNING('Eliminando datos existentes...'))
            Comment.objects.all().delete()
            Task.objects.all().delete()
            UserStory.objects.all().delete()
            Sprint.objects.all().delete()
            Project.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()
            self.stdout.write(self.style.SUCCESS('Datos eliminados correctamente'))

        self.stdout.write('Creando usuarios...')
        users = self.create_users()

        self.stdout.write('Creando proyectos...')
        projects = self.create_projects(users)

        self.stdout.write('Creando sprints...')
        sprints = self.create_sprints(projects)

        self.stdout.write('Creando historias de usuario...')
        user_stories = self.create_user_stories(projects, sprints, users)

        self.stdout.write('Creando tareas...')
        self.create_tasks(user_stories, users)

        self.stdout.write('Creando comentarios...')
        self.create_comments(user_stories, users)

        self.stdout.write(self.style.SUCCESS('Datos de ejemplo creados exitosamente!'))
        self.print_summary(users, projects)

    def create_users(self):
        """Crea usuarios de ejemplo"""
        users_data = [
            {
                'username': 'maria.garcia',
                'email': 'maria.garcia@example.com',
                'first_name': 'Maria',
                'last_name': 'Garcia',
                'password': 'demo1234'
            },
            {
                'username': 'juan.lopez',
                'email': 'juan.lopez@example.com',
                'first_name': 'Juan',
                'last_name': 'Lopez',
                'password': 'demo1234'
            },
            {
                'username': 'ana.martinez',
                'email': 'ana.martinez@example.com',
                'first_name': 'Ana',
                'last_name': 'Martinez',
                'password': 'demo1234'
            },
            {
                'username': 'carlos.rodriguez',
                'email': 'carlos.rodriguez@example.com',
                'first_name': 'Carlos',
                'last_name': 'Rodriguez',
                'password': 'demo1234'
            },
            {
                'username': 'lucia.fernandez',
                'email': 'lucia.fernandez@example.com',
                'first_name': 'Lucia',
                'last_name': 'Fernandez',
                'password': 'demo1234'
            },
            {
                'username': 'diego.sanchez',
                'email': 'diego.sanchez@example.com',
                'first_name': 'Diego',
                'last_name': 'Sanchez',
                'password': 'demo1234'
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
                self.stdout.write(f'  - Usuario creado: {user.username}')
            users.append(user)

        return users

    def create_projects(self, users):
        """Crea proyectos de ejemplo"""
        projects_data = [
            {
                'name': 'Sistema de E-commerce',
                'description': 'Desarrollo de una plataforma de comercio electronico completa con carrito de compras, pasarela de pagos y gestion de inventario.',
                'status': 'IN_PROGRESS',
                'start_date': timezone.now().date() - timedelta(days=60),
                'product_owner': users[0],
                'scrum_master': users[1],
                'team_members': users[2:6],
            },
            {
                'name': 'App Movil de Delivery',
                'description': 'Aplicacion movil para pedidos de comida a domicilio con tracking en tiempo real y sistema de calificaciones.',
                'status': 'IN_PROGRESS',
                'start_date': timezone.now().date() - timedelta(days=45),
                'product_owner': users[1],
                'scrum_master': users[2],
                'team_members': [users[0], users[3], users[4]],
            },
            {
                'name': 'Portal Educativo Online',
                'description': 'Plataforma de educacion online con cursos, examenes, certificaciones y sistema de gamificacion.',
                'status': 'PLANNING',
                'start_date': timezone.now().date() - timedelta(days=15),
                'product_owner': users[2],
                'scrum_master': users[3],
                'team_members': [users[0], users[1], users[4], users[5]],
            },
        ]

        projects = []
        for proj_data in projects_data:
            team_members = proj_data.pop('team_members')
            project, created = Project.objects.get_or_create(
                name=proj_data['name'],
                defaults=proj_data
            )
            if created:
                project.team_members.set(team_members)
                self.stdout.write(f'  - Proyecto creado: {project.name}')
            projects.append(project)

        return projects

    def create_sprints(self, projects):
        """Crea sprints de ejemplo"""
        sprints = []

        # Sprints para Sistema de E-commerce
        sprints_ecommerce = [
            {
                'project': projects[0],
                'name': 'Sprint 1 - Fundamentos',
                'number': 1,
                'goal': 'Configurar arquitectura base y autenticacion de usuarios',
                'status': 'COMPLETED',
                'start_date': timezone.now().date() - timedelta(days=60),
                'end_date': timezone.now().date() - timedelta(days=46),
                'velocity': 34,
            },
            {
                'project': projects[0],
                'name': 'Sprint 2 - Catalogo',
                'number': 2,
                'goal': 'Implementar catalogo de productos y sistema de busqueda',
                'status': 'COMPLETED',
                'start_date': timezone.now().date() - timedelta(days=45),
                'end_date': timezone.now().date() - timedelta(days=31),
                'velocity': 38,
            },
            {
                'project': projects[0],
                'name': 'Sprint 3 - Carrito',
                'number': 3,
                'goal': 'Desarrollar carrito de compras y wishlist',
                'status': 'ACTIVE',
                'start_date': timezone.now().date() - timedelta(days=30),
                'end_date': timezone.now().date() + timedelta(days=4),
                'velocity': None,
            },
        ]

        # Sprints para App Movil de Delivery
        sprints_delivery = [
            {
                'project': projects[1],
                'name': 'Sprint 1 - MVP',
                'number': 1,
                'goal': 'Desarrollar funcionalidades basicas de la app',
                'status': 'COMPLETED',
                'start_date': timezone.now().date() - timedelta(days=45),
                'end_date': timezone.now().date() - timedelta(days=31),
                'velocity': 28,
            },
            {
                'project': projects[1],
                'name': 'Sprint 2 - Tracking',
                'number': 2,
                'goal': 'Implementar sistema de tracking en tiempo real',
                'status': 'ACTIVE',
                'start_date': timezone.now().date() - timedelta(days=30),
                'end_date': timezone.now().date() + timedelta(days=4),
                'velocity': None,
            },
        ]

        # Sprints para Portal Educativo
        sprints_educativo = [
            {
                'project': projects[2],
                'name': 'Sprint 1 - Planificacion',
                'number': 1,
                'goal': 'Planificar arquitectura y definir tecnologias',
                'status': 'PLANNED',
                'start_date': timezone.now().date() + timedelta(days=7),
                'end_date': timezone.now().date() + timedelta(days=21),
                'velocity': None,
            },
        ]

        all_sprints = sprints_ecommerce + sprints_delivery + sprints_educativo

        for sprint_data in all_sprints:
            sprint, created = Sprint.objects.get_or_create(
                project=sprint_data['project'],
                number=sprint_data['number'],
                defaults=sprint_data
            )
            if created:
                self.stdout.write(f'  - Sprint creado: {sprint.name}')
            sprints.append(sprint)

        return sprints

    def create_user_stories(self, projects, sprints, users):
        """Crea historias de usuario de ejemplo"""
        user_stories = []

        # Historias para E-commerce
        stories_ecommerce = [
            {
                'project': projects[0],
                'sprint': sprints[0],
                'title': 'Registro de usuarios',
                'description': 'Como usuario nuevo, quiero poder registrarme en la plataforma para poder realizar compras',
                'acceptance_criteria': '- Formulario de registro con validacion\n- Email de confirmacion\n- Perfil de usuario creado',
                'story_points': 8,
                'priority': 'HIGH',
                'status': 'DONE',
                'assigned_to': users[2],
                'created_by': users[0],
            },
            {
                'project': projects[0],
                'sprint': sprints[1],
                'title': 'Listado de productos',
                'description': 'Como usuario, quiero ver un listado de productos disponibles para poder explorar el catalogo',
                'acceptance_criteria': '- Grid de productos con imagenes\n- Paginacion\n- Filtros basicos',
                'story_points': 13,
                'priority': 'HIGH',
                'status': 'DONE',
                'assigned_to': users[3],
                'created_by': users[0],
            },
            {
                'project': projects[0],
                'sprint': sprints[2],
                'title': 'Agregar productos al carrito',
                'description': 'Como comprador, quiero agregar productos al carrito para poder comprar multiples items',
                'acceptance_criteria': '- Boton agregar al carrito\n- Actualizar cantidad\n- Persistencia del carrito',
                'story_points': 8,
                'priority': 'CRITICAL',
                'status': 'IN_PROGRESS',
                'assigned_to': users[2],
                'created_by': users[0],
            },
            {
                'project': projects[0],
                'sprint': sprints[2],
                'title': 'Checkout y pago',
                'description': 'Como comprador, quiero poder finalizar mi compra de forma segura para recibir mis productos',
                'acceptance_criteria': '- Formulario de datos de envio\n- Integracion con pasarela de pago\n- Confirmacion de orden',
                'story_points': 21,
                'priority': 'CRITICAL',
                'status': 'TODO',
                'assigned_to': users[4],
                'created_by': users[0],
            },
            {
                'project': projects[0],
                'sprint': None,
                'title': 'Sistema de resenas de productos',
                'description': 'Como comprador, quiero poder dejar resenas de productos para ayudar a otros usuarios',
                'acceptance_criteria': '- Calificacion por estrellas\n- Comentarios de texto\n- Moderacion de contenido',
                'story_points': 13,
                'priority': 'MEDIUM',
                'status': 'BACKLOG',
                'assigned_to': None,
                'created_by': users[0],
            },
        ]

        # Historias para App Delivery
        stories_delivery = [
            {
                'project': projects[1],
                'sprint': sprints[3],
                'title': 'Login con redes sociales',
                'description': 'Como usuario, quiero poder iniciar sesion con mis redes sociales para un acceso rapido',
                'acceptance_criteria': '- Login con Google\n- Login con Facebook\n- Sincronizacion de perfil',
                'story_points': 8,
                'priority': 'HIGH',
                'status': 'DONE',
                'assigned_to': users[3],
                'created_by': users[1],
            },
            {
                'project': projects[1],
                'sprint': sprints[4],
                'title': 'Tracking de pedido en tiempo real',
                'description': 'Como cliente, quiero ver en tiempo real donde esta mi pedido para saber cuando llegara',
                'acceptance_criteria': '- Mapa con ubicacion del repartidor\n- Actualizacion en tiempo real\n- Notificaciones de estado',
                'story_points': 21,
                'priority': 'CRITICAL',
                'status': 'IN_PROGRESS',
                'assigned_to': users[0],
                'created_by': users[1],
            },
            {
                'project': projects[1],
                'sprint': sprints[4],
                'title': 'Sistema de calificaciones',
                'description': 'Como cliente, quiero poder calificar mi experiencia para mejorar el servicio',
                'acceptance_criteria': '- Calificar restaurante\n- Calificar repartidor\n- Comentarios opcionales',
                'story_points': 5,
                'priority': 'MEDIUM',
                'status': 'TODO',
                'assigned_to': users[4],
                'created_by': users[1],
            },
            {
                'project': projects[1],
                'sprint': None,
                'title': 'Programa de fidelidad',
                'description': 'Como cliente frecuente, quiero acumular puntos para obtener descuentos',
                'acceptance_criteria': '- Sistema de puntos\n- Canje de puntos\n- Historial de recompensas',
                'story_points': 13,
                'priority': 'LOW',
                'status': 'BACKLOG',
                'assigned_to': None,
                'created_by': users[1],
            },
        ]

        # Historias para Portal Educativo
        stories_educativo = [
            {
                'project': projects[2],
                'sprint': None,
                'title': 'Catalogo de cursos',
                'description': 'Como estudiante, quiero ver todos los cursos disponibles para elegir el que me interesa',
                'acceptance_criteria': '- Listado de cursos\n- Filtros por categoria\n- Preview de contenido',
                'story_points': 8,
                'priority': 'HIGH',
                'status': 'BACKLOG',
                'assigned_to': None,
                'created_by': users[2],
            },
            {
                'project': projects[2],
                'sprint': None,
                'title': 'Reproductor de videos',
                'description': 'Como estudiante, quiero ver las clases en video para aprender el contenido',
                'acceptance_criteria': '- Reproductor HTML5\n- Control de velocidad\n- Marcadores de progreso',
                'story_points': 13,
                'priority': 'CRITICAL',
                'status': 'BACKLOG',
                'assigned_to': None,
                'created_by': users[2],
            },
            {
                'project': projects[2],
                'sprint': None,
                'title': 'Sistema de examenes',
                'description': 'Como instructor, quiero crear examenes para evaluar el conocimiento de los estudiantes',
                'acceptance_criteria': '- Crear preguntas multiple choice\n- Tiempo limite\n- Calificacion automatica',
                'story_points': 21,
                'priority': 'HIGH',
                'status': 'BACKLOG',
                'assigned_to': None,
                'created_by': users[2],
            },
        ]

        all_stories = stories_ecommerce + stories_delivery + stories_educativo

        for story_data in all_stories:
            story = UserStory.objects.create(**story_data)
            self.stdout.write(f'  - Historia creada: {story.title}')
            user_stories.append(story)

        return user_stories

    def create_tasks(self, user_stories, users):
        """Crea tareas de ejemplo"""
        tasks_count = 0

        # Tareas para algunas historias seleccionadas
        for story in user_stories[:6]:  # Solo las primeras 6 historias
            if story.status in ['IN_PROGRESS', 'DONE']:
                # Crear 3-5 tareas por historia
                num_tasks = 3 if story.story_points <= 8 else 5

                tasks_templates = [
                    'Disenar interfaz de usuario',
                    'Implementar backend/API',
                    'Crear tests unitarios',
                    'Documentar funcionalidad',
                    'Revision de codigo',
                ]

                for i in range(num_tasks):
                    task_status = 'DONE' if story.status == 'DONE' else 'IN_PROGRESS' if i == 0 else 'TODO'

                    Task.objects.create(
                        user_story=story,
                        title=f'{tasks_templates[i]} - {story.title[:30]}',
                        description=f'Tarea relacionada con: {story.title}',
                        status=task_status,
                        estimated_hours=4.0 if i < 2 else 2.0,
                        actual_hours=4.5 if task_status == 'DONE' else None,
                        assigned_to=story.assigned_to,
                    )
                    tasks_count += 1

        self.stdout.write(f'  - {tasks_count} tareas creadas')

    def create_comments(self, user_stories, users):
        """Crea comentarios de ejemplo"""
        comments_data = [
            'Excelente trabajo en esta historia!',
            'Necesitamos revisar los criterios de aceptacion',
            'Ya esta lista para testing',
            'Encontre un bug en la validacion, lo estoy corrigiendo',
            'Documentacion actualizada en el wiki',
            'Propongo cambiar el enfoque de esta funcionalidad',
        ]

        comments_count = 0
        for story in user_stories[:8]:  # Comentarios en las primeras 8 historias
            if story.status != 'BACKLOG':
                # 1-3 comentarios por historia
                num_comments = min(len(comments_data), 3)
                for i in range(num_comments):
                    Comment.objects.create(
                        user_story=story,
                        author=users[i % len(users)],
                        content=comments_data[i % len(comments_data)],
                    )
                    comments_count += 1

        self.stdout.write(f'  - {comments_count} comentarios creados')

    def print_summary(self, users, projects):
        """Imprime un resumen de los datos creados"""
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('RESUMEN DE DATOS CREADOS'))
        self.stdout.write('='*60)

        self.stdout.write(f'\nUsuarios creados: {len(users)}')
        for user in users:
            self.stdout.write(f'  - {user.username} / Password: demo1234')

        self.stdout.write(f'\nProyectos: {Project.objects.count()}')
        for project in projects:
            self.stdout.write(f'  - {project.name}')
            self.stdout.write(f'    Sprints: {project.sprints.count()}')
            self.stdout.write(f'    Historias: {project.user_stories.count()}')

        self.stdout.write(f'\nTotal de Sprints: {Sprint.objects.count()}')
        self.stdout.write(f'Total de Historias de Usuario: {UserStory.objects.count()}')
        self.stdout.write(f'Total de Tareas: {Task.objects.count()}')
        self.stdout.write(f'Total de Comentarios: {Comment.objects.count()}')

        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('Puedes iniciar sesion con cualquiera de los usuarios'))
        self.stdout.write(self.style.SUCCESS('Todos usan la password: demo1234'))
        self.stdout.write('='*60 + '\n')
