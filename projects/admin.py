from django.contrib import admin
from .models import Project, Sprint, UserStory, Task, Comment


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """
    Admin personalizado para Project con mejores prácticas:
    - list_display para mostrar campos relevantes
    - list_filter para filtros rápidos
    - search_fields para búsqueda
    - readonly_fields para campos auto-generados
    - fieldsets para organización
    """
    list_display = ['name', 'status', 'product_owner', 'scrum_master', 'start_date', 'created_at']
    list_filter = ['status', 'start_date', 'created_at']
    search_fields = ['name', 'description', 'product_owner__username', 'scrum_master__username']
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


@admin.register(Sprint)
class SprintAdmin(admin.ModelAdmin):
    """
    Admin personalizado para Sprint.
    """
    list_display = ['name', 'project', 'number', 'status', 'start_date', 'end_date', 'velocity']
    list_filter = ['status', 'start_date', 'project']
    search_fields = ['name', 'goal', 'project__name']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Información del Sprint', {
            'fields': ('project', 'name', 'number', 'status')
        }),
        ('Objetivo y Planificación', {
            'fields': ('goal', 'start_date', 'end_date', 'velocity')
        }),
        ('Metadatos', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(UserStory)
class UserStoryAdmin(admin.ModelAdmin):
    """
    Admin personalizado para UserStory.
    """
    list_display = ['title', 'project', 'sprint', 'priority', 'status', 'story_points', 'assigned_to']
    list_filter = ['status', 'priority', 'project', 'sprint', 'created_at']
    search_fields = ['title', 'description', 'project__name']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Información Básica', {
            'fields': ('project', 'sprint', 'title', 'description')
        }),
        ('Criterios y Estimación', {
            'fields': ('acceptance_criteria', 'story_points')
        }),
        ('Estado y Prioridad', {
            'fields': ('status', 'priority')
        }),
        ('Asignación', {
            'fields': ('assigned_to', 'created_by')
        }),
        ('Metadatos', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Admin personalizado para Task.
    """
    list_display = ['title', 'user_story', 'status', 'estimated_hours', 'actual_hours', 'assigned_to']
    list_filter = ['status', 'user_story__project', 'created_at']
    search_fields = ['title', 'description', 'user_story__title']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Información de la Tarea', {
            'fields': ('user_story', 'title', 'description', 'status')
        }),
        ('Estimación de Tiempo', {
            'fields': ('estimated_hours', 'actual_hours')
        }),
        ('Asignación', {
            'fields': ('assigned_to',)
        }),
        ('Metadatos', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Admin personalizado para Comment.
    """
    list_display = ['author', 'user_story', 'created_at', 'content_preview']
    list_filter = ['created_at', 'author']
    search_fields = ['content', 'author__username', 'user_story__title']
    readonly_fields = ['created_at', 'updated_at']

    def content_preview(self, obj):
        """Muestra una preview del contenido."""
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content

    content_preview.short_description = 'Vista previa'

    fieldsets = (
        ('Comentario', {
            'fields': ('user_story', 'author', 'content')
        }),
        ('Metadatos', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
