from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .models import Task
from .forms import TaskForm
from django.contrib import messages


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks_list.html'
    context_object_name = 'tasks'

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks_detail.html'

class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks_form.html'
    success_url = reverse_lazy('tasks:list')
    success_message = "Задача успешно создана"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks_form.html'
    success_url = reverse_lazy('tasks:list')
    success_message = "Задача успешно обновлена"

class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'tasks_confirm_delete.html'
    success_url = reverse_lazy('tasks:list')
    success_message = "Задача успешно удалена"

    def test_func(self):
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, 'Задачу может удалить только её автор')
        return redirect(self.success_url)
