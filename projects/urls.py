from django.urls import path
from . import views

# URLs del modulo de proyectos
# Mejores practicas:
# - Nombres descriptivos para las URLs
# - Organizacion logica por entidad
# - Patrones RESTful

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Proyectos
    path('projects/', views.project_list, name='project_list'),
    path('projects/create/', views.project_create, name='project_create'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('projects/<int:pk>/update/', views.project_update, name='project_update'),

    # Sprints
    path('projects/<int:project_pk>/sprints/', views.sprint_list, name='sprint_list'),
    path('projects/<int:project_pk>/sprints/create/', views.sprint_create, name='sprint_create'),
    path('sprints/<int:pk>/', views.sprint_detail, name='sprint_detail'),

    # User Stories
    path('projects/<int:project_pk>/stories/', views.user_story_list, name='user_story_list'),
    path('projects/<int:project_pk>/stories/create/', views.user_story_create, name='user_story_create'),
    path('stories/<int:pk>/', views.user_story_detail, name='user_story_detail'),
    path('stories/<int:pk>/update/', views.user_story_update, name='user_story_update'),

    # Tasks
    path('stories/<int:user_story_pk>/tasks/create/', views.task_create, name='task_create'),
    path('tasks/<int:pk>/update/', views.task_update, name='task_update'),
]
