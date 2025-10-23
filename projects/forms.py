from django import forms
from django.contrib.auth.models import User
from .models import Project, Sprint, UserStory, Task, Comment


class ProjectForm(forms.ModelForm):
    """
    Formulario para crear y editar proyectos.
    Mejores prácticas:
    - Uso de widgets para mejor UX
    - Validaciones personalizadas
    - Help texts descriptivos
    """

    class Meta:
        model = Project
        fields = [
            'name', 'description', 'status', 'start_date', 'end_date',
            'product_owner', 'scrum_master', 'team_members'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'product_owner': forms.Select(attrs={'class': 'form-select'}),
            'scrum_master': forms.Select(attrs={'class': 'form-select'}),
            'team_members': forms.SelectMultiple(attrs={'class': 'form-select', 'size': '5'}),
        }

    def clean(self):
        """Validación personalizada para fechas."""
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and end_date < start_date:
            raise forms.ValidationError(
                'La fecha de fin no puede ser anterior a la fecha de inicio.'
            )

        return cleaned_data


class SprintForm(forms.ModelForm):
    """
    Formulario para crear y editar sprints.
    """

    class Meta:
        model = Sprint
        fields = ['name', 'number', 'goal', 'status', 'start_date', 'end_date', 'velocity']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'number': forms.NumberInput(attrs={'class': 'form-control'}),
            'goal': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'velocity': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project', None)
        super().__init__(*args, **kwargs)

        if self.project and not self.instance.pk:
            # Sugerir el siguiente número de sprint
            last_sprint = Sprint.objects.filter(project=self.project).order_by('-number').first()
            if last_sprint:
                self.fields['number'].initial = last_sprint.number + 1
            else:
                self.fields['number'].initial = 1

    def clean(self):
        """Validación de fechas y número de sprint."""
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        number = cleaned_data.get('number')

        if start_date and end_date and end_date <= start_date:
            raise forms.ValidationError(
                'La fecha de fin debe ser posterior a la fecha de inicio.'
            )

        # Validar que no exista otro sprint con el mismo número
        if self.project and number:
            existing = Sprint.objects.filter(project=self.project, number=number)
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            if existing.exists():
                raise forms.ValidationError(
                    f'Ya existe un Sprint número {number} en este proyecto.'
                )

        return cleaned_data


class UserStoryForm(forms.ModelForm):
    """
    Formulario para crear y editar historias de usuario.
    """

    class Meta:
        model = UserStory
        fields = [
            'title', 'description', 'acceptance_criteria', 'story_points',
            'priority', 'status', 'sprint', 'assigned_to'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Como [rol], quiero [funcionalidad] para [beneficio]'
            }),
            'acceptance_criteria': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Criterios que deben cumplirse...'
            }),
            'story_points': forms.NumberInput(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'sprint': forms.Select(attrs={'class': 'form-select'}),
            'assigned_to': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project', None)
        super().__init__(*args, **kwargs)

        # Filtrar sprints y usuarios del proyecto
        if self.project:
            self.fields['sprint'].queryset = Sprint.objects.filter(project=self.project)
            self.fields['assigned_to'].queryset = self.project.team_members.all()

        # Hacer campos opcionales en el widget
        self.fields['sprint'].empty_label = 'Product Backlog'
        self.fields['assigned_to'].empty_label = 'Sin asignar'


class TaskForm(forms.ModelForm):
    """
    Formulario para crear y editar tareas.
    """

    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'estimated_hours', 'actual_hours', 'assigned_to']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'estimated_hours': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5'}),
            'actual_hours': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5'}),
            'assigned_to': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        self.user_story = kwargs.pop('user_story', None)
        super().__init__(*args, **kwargs)

        # Filtrar usuarios del proyecto de la historia
        if self.user_story:
            self.fields['assigned_to'].queryset = self.user_story.project.team_members.all()

        self.fields['assigned_to'].empty_label = 'Sin asignar'


class CommentForm(forms.ModelForm):
    """
    Formulario para agregar comentarios a historias de usuario.
    """

    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Escribe tu comentario...'
            }),
        }
        labels = {
            'content': 'Comentario'
        }
