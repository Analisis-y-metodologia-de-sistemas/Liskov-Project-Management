from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


class Project(models.Model):
    """
    Modelo que representa un proyecto Scrum.
    Mejores prácticas implementadas:
    - Uso de choices para estados
    - Métodos __str__ descriptivos
    - Meta class para ordenamiento
    - Documentación clara
    """

    STATUS_CHOICES = [
        ('PLANNING', 'Planificación'),
        ('IN_PROGRESS', 'En Progreso'),
        ('ON_HOLD', 'En Pausa'),
        ('COMPLETED', 'Completado'),
        ('CANCELLED', 'Cancelado'),
    ]

    name = models.CharField(
        max_length=200,
        verbose_name=_('Nombre'),
        help_text='Nombre del proyecto'
    )
    description = models.TextField(
        verbose_name=_('Descripción'),
        help_text='Descripción detallada del proyecto'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PLANNING',
        verbose_name=_('Estado')
    )
    start_date = models.DateField(
        verbose_name=_('Fecha de inicio')
    )
    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Fecha de fin')
    )
    product_owner = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='owned_projects',
        verbose_name=_('Product Owner')
    )
    scrum_master = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='managed_projects',
        verbose_name=_('Scrum Master')
    )
    team_members = models.ManyToManyField(
        User,
        related_name='projects',
        verbose_name=_('Miembros del equipo'),
        blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Fecha de creación')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Última actualización')
    )

    class Meta:
        verbose_name = _('Proyecto')
        verbose_name_plural = _('Proyectos')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.get_status_display()})"


class Sprint(models.Model):
    """
    Modelo que representa un Sprint dentro de un proyecto Scrum.
    """

    STATUS_CHOICES = [
        ('PLANNED', 'Planificado'),
        ('ACTIVE', 'Activo'),
        ('COMPLETED', 'Completado'),
        ('CANCELLED', 'Cancelado'),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='sprints',
        verbose_name=_('Proyecto')
    )
    name = models.CharField(
        max_length=100,
        verbose_name=_('Nombre')
    )
    goal = models.TextField(
        verbose_name=_('Objetivo del Sprint'),
        help_text='Meta u objetivo principal del sprint'
    )
    number = models.PositiveIntegerField(
        verbose_name=_('Número de Sprint'),
        validators=[MinValueValidator(1)]
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PLANNED',
        verbose_name=_('Estado')
    )
    start_date = models.DateField(
        verbose_name=_('Fecha de inicio')
    )
    end_date = models.DateField(
        verbose_name=_('Fecha de fin')
    )
    velocity = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_('Velocidad'),
        help_text='Puntos de historia completados'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Fecha de creación')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Última actualización')
    )

    class Meta:
        verbose_name = _('Sprint')
        verbose_name_plural = _('Sprints')
        ordering = ['-number']
        unique_together = [['project', 'number']]

    def __str__(self):
        return f"{self.project.name} - Sprint {self.number}"


class UserStory(models.Model):
    """
    Modelo que representa una Historia de Usuario.
    """

    PRIORITY_CHOICES = [
        ('LOW', 'Baja'),
        ('MEDIUM', 'Media'),
        ('HIGH', 'Alta'),
        ('CRITICAL', 'Crítica'),
    ]

    STATUS_CHOICES = [
        ('BACKLOG', 'Product Backlog'),
        ('TODO', 'Por Hacer'),
        ('IN_PROGRESS', 'En Progreso'),
        ('IN_REVIEW', 'En Revisión'),
        ('DONE', 'Completada'),
        ('BLOCKED', 'Bloqueada'),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='user_stories',
        verbose_name=_('Proyecto')
    )
    sprint = models.ForeignKey(
        Sprint,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='user_stories',
        verbose_name=_('Sprint')
    )
    title = models.CharField(
        max_length=200,
        verbose_name=_('Título')
    )
    description = models.TextField(
        verbose_name=_('Descripción'),
        help_text='Como [rol], quiero [funcionalidad] para [beneficio]'
    )
    acceptance_criteria = models.TextField(
        verbose_name=_('Criterios de aceptación'),
        help_text='Condiciones que deben cumplirse para considerar la historia completa'
    )
    story_points = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_('Puntos de historia'),
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='MEDIUM',
        verbose_name=_('Prioridad')
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='BACKLOG',
        verbose_name=_('Estado')
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_stories',
        verbose_name=_('Asignado a')
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='created_stories',
        verbose_name=_('Creado por')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Fecha de creación')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Última actualización')
    )

    class Meta:
        verbose_name = _('Historia de Usuario')
        verbose_name_plural = _('Historias de Usuario')
        ordering = ['-priority', '-created_at']

    def __str__(self):
        return f"{self.title} ({self.get_priority_display()})"


class Task(models.Model):
    """
    Modelo que representa una Tarea dentro de una Historia de Usuario.
    """

    STATUS_CHOICES = [
        ('TODO', 'Por Hacer'),
        ('IN_PROGRESS', 'En Progreso'),
        ('DONE', 'Completada'),
    ]

    user_story = models.ForeignKey(
        UserStory,
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name=_('Historia de usuario')
    )
    title = models.CharField(
        max_length=200,
        verbose_name=_('Título')
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('Descripción')
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='TODO',
        verbose_name=_('Estado')
    )
    estimated_hours = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_('Horas estimadas'),
        validators=[MinValueValidator(0)]
    )
    actual_hours = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_('Horas reales'),
        validators=[MinValueValidator(0)]
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tasks',
        verbose_name=_('Asignado a')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Fecha de creación')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Última actualización')
    )

    class Meta:
        verbose_name = _('Tarea')
        verbose_name_plural = _('Tareas')
        ordering = ['status', '-created_at']

    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"


class Comment(models.Model):
    """
    Modelo que representa comentarios en historias de usuario.
    """

    user_story = models.ForeignKey(
        UserStory,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name=_('Historia de usuario')
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name=_('Autor')
    )
    content = models.TextField(
        verbose_name=_('Contenido')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Fecha de creación')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Última actualización')
    )

    class Meta:
        verbose_name = _('Comentario')
        verbose_name_plural = _('Comentarios')
        ordering = ['-created_at']

    def __str__(self):
        return f"Comentario de {self.author.username} en {self.user_story.title}"
