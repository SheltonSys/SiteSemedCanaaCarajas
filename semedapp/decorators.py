from functools import wraps
from django.http import HttpResponseForbidden

def module_required(module_name):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Usuário não autenticado.")

            user_modules = request.user.modulos_permitidos.values_list('module__nome', flat=True)
            if module_name not in user_modules:
                return HttpResponseForbidden("Você não tem permissão para acessar este módulo.")

            return view_func(request, *args, **kwargs)

        return _wrapped_view
    return decorator
