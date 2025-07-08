import django_filters
from django import forms

from .models import Task
from task_manager.labels.models import Label


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Task._meta.get_field("status").related_model.objects.all(),
        label="Статус"
    )
    executor = django_filters.ModelChoiceFilter(
        queryset=Task._meta.get_field("executor").related_model.objects.all(),
        label="Исполнитель"
    )
    labels = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        label="Метка"
    )
    self_tasks = django_filters.BooleanFilter(
        method="filter_self_tasks",
        label="Только свои задачи",
        widget=forms.CheckboxInput,
    )

    class Meta:
        model = Task
        fields = ["status", "executor", "labels", "self_tasks"]

    def filter_self_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset
