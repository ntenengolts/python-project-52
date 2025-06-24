from django import forms

from task_manager.statuses.models import Status
from task_manager.users.models import User

from .models import Task


class TaskForm(forms.ModelForm):
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(), label="Статус", empty_label="Выберите статус"
    )
    executor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        label="Исполнитель",
        empty_label="Не назначен",
    )

    class Meta:
        model = Task
        fields = ["name", "description", "status", "executor", "labels"]
        widgets = {
            "labels": forms.SelectMultiple(),
        }
