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
                _("У вас нет прав для изменения")
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
    """
    Ловит ProtectedError и выводит сообщение.
    Конкретные view могут переопределять:
      • success_url            – куда редирект при успешном удалении
      • protected_error_url    – куда редирект при ошибке
      • protected_error_message – текст сообщения
    """
    success_url = None                # обязателен в наследнике
    protected_error_url = None        # если None – берётся success_url
    protected_error_message = _(
        "Невозможно удалить объект, потому что он используется"
    )

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            return super().delete(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, self.protected_error_message)
            return redirect(self.protected_error_url or self.success_url)
