from django.utils.deprecation import MiddlewareMixin
from django.utils.html import strip_tags
from django.shortcuts import render, redirect
from django.contrib.sessions.models import Session
from django.http import HttpResponse

class InputSanitizationMiddleware(MiddlewareMixin):
    BLACKLISTED_KEYWORDS = [
        'select', 'insert', 'update', 'delete', 'drop', 'alter', 'create', 'shutdown',
        'or ', 'and ', '--', ';', 'sleep(', 'benchmark(', 'union', 'waitfor', 'pg_sleep', 'dbms_pipe'
    ]

    def process_request(self, request):
        if request.method == 'POST':
            for key, value in request.POST.items():
                if value:
                    clean_value = strip_tags(value)
                    for keyword in self.BLACKLISTED_KEYWORDS:
                        if keyword in clean_value.lower():
                            # Destrói a sessão
                            request.session.flush()

                            # Retorna uma resposta HTML personalizada
                            html_response = """
                            <!DOCTYPE html>
                            <html lang="pt-BR">
                            <head>
                                <meta charset="UTF-8">
                                <title>Acesso Bloqueado</title>
                                <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
                                <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
                            </head>
                            <body>
                                <script>
                                    $(document).ready(function() {
                                        // Coletar dados do navegador
                                        const userAgent = navigator.userAgent;
                                        const platform = navigator.platform;
                                        
                                        // Coletar IP via serviço público (não 100% garantido)
                                        fetch('https://api.ipify.org?format=json')
                                            .then(response => response.json())
                                            .then(data => {
                                                const ip = data.ip;

                                                Swal.fire({
                                                    title: 'ATENÇÃO!',
                                                    html: `
                                                        <b>Seu acesso foi bloqueado.</b><br><br>
                                                        <b>IP Detectado:</b> ${ip}<br>
                                                        <b>Dispositivo:</b> ${platform}<br>
                                                        <b>Navegador:</b> ${userAgent}<br><br>
                                                        <span style="color:red;">Todas as informações de sua tentativa foram registradas e poderão ser utilizadas para ação legal.</span>
                                                    `,
                                                    icon: 'error',
                                                    confirmButtonText: 'Entendi'
                                                }).then((result) => {
                                                    if (result.isConfirmed) {
                                                        window.location.href = '/login/';
                                                    }
                                                });
                                            });
                                    });
                                </script>
                            </body>
                            </html>
                            """
                            return HttpResponse(html_response)
                    request.POST._mutable = True
                    request.POST[key] = clean_value
                    request.POST._mutable = False
