import os
from django.conf import settings
from django.shortcuts import render

class ForceMaintenanceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.flag_path = os.path.join(settings.BASE_DIR, 'maintenance.flag')

    def __call__(self, request):
        if os.path.exists(self.flag_path):
            return render(request, 'manutencao.html', status=503)
        return self.get_response(request)
