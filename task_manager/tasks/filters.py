import django_filters
from .models import Task
from django import forms


class TaskFilter(django_filters.FilterSet):
    self_tasks = django_filters.BooleanFilter(
         method='filter_self_tasks',
         label='Только свои задачи',
         widget=forms.CheckboxInput
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels', 'self_tasks']

    def filter_self_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset

