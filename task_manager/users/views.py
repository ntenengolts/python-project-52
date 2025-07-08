from django.contrib import messages
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import (
    CustomAuthenticationForm,
    CustomUserChangeForm,
    CustomUserCreationForm,
)

User = get_user_model()


class UserListView(ListView):
    model = User
    template_name = "user_list.html"
    context_object_name = "users"


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = "user_form.html"
    success_url = reverse_lazy("login")
    success_message = "Пользователь успешно зарегистрирован"


class UserUpdateView(SuccessMessageMixin, UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = "user_form.html"
    success_url = reverse_lazy("users:list")
    success_message = "Пользователь успешно изменен"


class UserDeleteView(SuccessMessageMixin, DeleteView):
    model = User
    template_name = "user_confirm_delete.html"
    success_url = reverse_lazy("users:list")
    success_message = "Пользователь успешно удален"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object != request.user:
            messages.error(
                request,
                "У вас нет прав для удаления другого пользователя."
            )
            return redirect(self.success_url)

        if self.object == request.user and request.user.is_authenticated:
            messages.error(
                request,
                "Невозможно удалить пользователя, потому что он используется"
            )
            return redirect(self.success_url)


class CustomLogoutView(View):
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "Вы разлогинены")
        return redirect("/")


class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = "login.html"

    def form_valid(self, form):
        messages.success(self.request, "Вы залогинены")
        return super().form_valid(form)
