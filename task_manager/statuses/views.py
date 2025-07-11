from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.mixins import SafeDeleteMixin

from .forms import StatusForm
from .models import Status


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = "status_list.html"
    context_object_name = "statuses"


class StatusCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = "status_form.html"
    success_url = reverse_lazy("statuses:list")
    success_message = "Статус успешно создан"


class StatusUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = "status_form.html"
    success_url = reverse_lazy("statuses:list")
    success_message = "Статус успешно изменен"


class StatusDeleteView(
    LoginRequiredMixin, SafeDeleteMixin,
    SuccessMessageMixin, DeleteView
):
    model = Status
    template_name = "status_confirm_delete.html"
    success_url = reverse_lazy("statuses:list")
    protected_error_url = success_url
    protected_error_message = _(
         "Невозможно удалить статус, потому что он используется"
    )
    success_message = _("Статус успешно удален")
