from django import forms
from .models import Task
from task_manager.statuses.models import Status
from task_manager.users.models import User


class TaskForm(forms.ModelForm):
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        label='Статус',
        empty_label="Выберите статус"
    )
    executor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        label='Исполнитель',
        empty_label="Не назначен"
    )

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor']
        labels = {
            'name': 'Название задачи',
            'description': 'Описание',
        }
