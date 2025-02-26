from django.db import models
from django.conf import settings
from django.apps import apps  # 🔹 Importação atrasada

class UserModulePermission(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    module = models.ForeignKey('semedapp.Module', on_delete=models.CASCADE)  # 🔹 Carregamento atrasado

    def __str__(self):
        return f"{self.user.username} - {self.module.nome}"
