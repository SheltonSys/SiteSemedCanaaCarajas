from django.conf import settings
from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin

class MaintenanceModeMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if settings.MAINTENANCE_MODE:
            user = getattr(request, 'user', None)
            if not (user and user.is_authenticated and user.is_staff):
                return render(request, 'manutencao.html', status=503)
        return None
