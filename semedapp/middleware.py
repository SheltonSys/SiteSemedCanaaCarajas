# middleware.py
class AccessLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Importação tardia para evitar circularidade
        from semedapp.models import ModuleAccess  

        response = self.get_response(request)

        if request.user.is_authenticated:
            path = request.path
            module_mapping = {
                '/configuracao/': 'configuracao',
                '/indicadores/': 'indicadores',
                '/pedagogico/': 'pedagogico',
                '/contabilidade/': 'contabilidade',
                '/curriculos/': 'curriculos',
                '/site-semed/': 'site_semed',
            }
            for module_path, module_name in module_mapping.items():
                if path.startswith(module_path):
                    ModuleAccess.objects.create(user=request.user, module=module_name)
                    break

        return response
