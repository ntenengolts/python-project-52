from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views import View
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from .forms import CustomUserCreationForm, CustomUserChangeForm


User = get_user_model()


class UserListView(ListView):
    model = User
    template_name = 'user_list.html'
    context_object_name = 'users'


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'user_form.html'
    success_url = reverse_lazy('login')
    success_message = 'Пользователь успешно зарегистрирован'


class UserUpdateView(SuccessMessageMixin, UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'user_form.html'
    success_url = reverse_lazy('users:list')
    success_message = 'Пользователь успешно обновлён'


class UserDeleteView(SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'user_confirm_delete.html'
    success_url = reverse_lazy('users:list')
    success_message = 'Пользователь успешно удалён'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class CustomLogoutView(View):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "Вы разлогинились")
        return redirect('/')


