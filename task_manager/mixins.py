from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class SelfOnlyMixin:
    """Разрешает действие только над собственным объектом."""
    permission_denied_url = reverse_lazy('users:list')

    def dispatch(self, request, *args, **kwargs):
        if request.user != self.get_object():
            messages.error(request,
                _("У вас нет прав для удаления другого пользователя.")
            )
            return redirect(self.permission_denied_url)
        return super().dispatch(request, *args, **kwargs)


class ProtectedCheckMixin:
    """
    Если у пользователя есть связанные задачи, сразу прерываем
    удаление (ещё на GET) и делаем редирект с флеш‑сообщением.
    """
    protected_error_url = reverse_lazy('users:list')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self._has_related_objects():
            messages.error(request,
                _("Невозможно удалить пользователя, потому что он используется")
            )

            return redirect(self.protected_error_url)
        return super().get(request, *args, **kwargs)

    def _has_related_objects(self):
        from task_manager.tasks.models import Task  # локальный импорт
        return (
            Task.objects.filter(author=self.object).exists()
            or Task.objects.filter(executor=self.object).exists()
        )


class SafeDeleteMixin:
    """Удаляет объект и перехватывает ProtectedError."""
    success_url = reverse_lazy('users:list')
    protected_error_url = reverse_lazy('users:list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            response = super().delete(request, *args, **kwargs)
            return response
        except ProtectedError:
            messages.error(request,
                _("Невозможно удалить пользователя, потому что он используется")
            )
            return redirect(self.protected_error_url)
