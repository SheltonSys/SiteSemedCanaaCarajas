from django.utils.deprecation import MiddlewareMixin
from django.utils.html import strip_tags
from django.http import HttpResponse
import re

class InputSanitizationMiddleware(MiddlewareMixin):
    # Regex para detectar uso malicioso de comandos SQL
    SQLI_PATTERNS = [
        r"(?i)(\bselect\b\s.*\bfrom\b)",  # SELECT ... FROM
        r"(?i)(\bor\b\s+1\s*=\s*1)",      # OR 1=1
        r"(?i)(\bunion\b\s+select)",      # UNION SELECT
        r"(?i)(\bsleep\s*\()",            # sleep(15)
        r"(?i)(pg_sleep\s*\()",           # pg_sleep
        r"(?i)(waitfor\s+delay)",         # waitfor delay '0:0:15'
        r"(?i)(benchmark\s*\()",          # benchmark(
        r"(?i)(dbms_pipe.receive_message)"# Oracle injection
    ]

    def process_request(self, request):
        if request.method == 'POST':
            for key, value in request.POST.items():
                if value:
                    clean_value = strip_tags(value)

                    # Verifica padrões maliciosos, não só palavras-chave
                    for pattern in self.SQLI_PATTERNS:
                        if re.search(pattern, clean_value):
                            request.session.flush()  # Destrói a sessão do invasor

                            html_response = f"""
                            <!DOCTYPE html>
                            <html lang="pt-BR">
                            <head>
                                <meta charset="UTF-8">
                                <title>Acesso Bloqueado</title>
                                <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
                                <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
                                <style>
                                    body {{
                                        background: rgba(0,0,0,0.7);
                                        display: flex;
                                        justify-content: center;
                                        align-items: center;
                                        height: 100vh;
                                        margin: 0;
                                        font-family: Arial, sans-serif;
                                    }}
                                </style>
                            </head>
                            <body>
                                <script>
                                    let ip, userAgent, platform;

                                    userAgent = navigator.userAgent;
                                    platform = navigator.platform;

                                    fetch('https://api.ipify.org?format=json')
                                        .then(response => response.json())
                                        .then(data => {{
                                            ip = data.ip;

                                            Swal.fire({{
                                                icon: 'error',
                                                title: 'Acesso Bloqueado',
                                                html: `
                                                    <p><b>Seu acesso foi bloqueado.</b></p>
                                                    <p><b>IP:</b> ${ip}</p>
                                                    <p><b>Dispositivo:</b> ${platform}</p>
                                                    <p><b>Navegador:</b> ${userAgent}</p>
                                                    <p style='color:red;'><b>Esta tentativa foi registrada e poderá ser usada para responsabilização legal.</b></p>
                                                `,
                                                confirmButtonText: 'Entendi'
                                            }}).then(() => {{
                                                window.location.href = '/login/';
                                            }});
                                        }});
                                </script>
                            </body>
                            </html>
                            """
                            return HttpResponse(html_response, content_type="text/html", status=400)

                    request.POST._mutable = True
                    request.POST[key] = clean_value
                    request.POST._mutable = False
