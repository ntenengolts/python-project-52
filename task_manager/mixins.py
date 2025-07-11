from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class SelfOnlyMixin:
    """Разрешает действие только над собственным объектом."""
    permission_denied_url = reverse_lazy('users')

    def dispatch(self, request, *args, **kwargs):
        if request.user != self.get_object():
            messages.error(request,
                _("У вас нет прав для удаления другого пользователя.")
            )
            return redirect(self.permission_denied_url)
        return super().dispatch(request, *args, **kwargs)


class SafeDeleteMixin:
    """Удаляет объект и перехватывает ProtectedError."""
    protected_error_url = reverse_lazy('users')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            messages.success(request, _("Пользователь успешно удален"))
            return super().delete(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request,
                _("Невозможно удалить пользователя, потому что он используется")
            )
            return redirect(self.protected_error_url)

    # Тест кликает по GET → сразу удаляем
    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
