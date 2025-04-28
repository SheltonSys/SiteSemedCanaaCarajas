# Em um arquivo novo, ex: 'middlewares/input_sanitization.py'

from django.utils.deprecation import MiddlewareMixin
from django.utils.html import strip_tags
from django.http import HttpResponseBadRequest

class InputSanitizationMiddleware(MiddlewareMixin):
    BLACKLISTED_KEYWORDS = [
        'select', 'insert', 'update', 'delete', 'drop', 'alter', 'create', 'shutdown',
        'or ', 'and ', '--', ';', 'sleep(', 'benchmark(', 'union', 'waitfor', 'pg_sleep', 'dbms_pipe'
    ]

    def process_request(self, request):
        if request.method == 'POST':
            for key, value in request.POST.items():
                if value:
                    # Limpa HTML
                    clean_value = strip_tags(value)
                    # Verifica palavras perigosas
                    for keyword in self.BLACKLISTED_KEYWORDS:
                        if keyword in clean_value.lower():
                            return HttpResponseBadRequest(f"Tentativa de ataque detectada em campo '{key}'.")
                    # Substitui o valor original pelo valor limpo
                    request.POST._mutable = True
                    request.POST[key] = clean_value
                    request.POST._mutable = False
