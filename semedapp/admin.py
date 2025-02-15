from django.contrib import admin
from .models import Module, UserModulePermission
from .models import TipoDemanda

admin.site.register(Module)

admin.site.register(UserModulePermission)


@admin.register(TipoDemanda)
class TipoDemandaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'descricao', 'status', 'prioridade', 'data_cadastro']
    list_filter = ['status', 'prioridade', 'data_cadastro']
    search_fields = ['nome', 'descricao']


from django.contrib import admin
from .models import RoleModulePermission

@admin.register(RoleModulePermission)
class RoleModulePermissionAdmin(admin.ModelAdmin):
    list_display = ('role', 'module')
    list_filter = ('role',)
    search_fields = ('module__module_name',)



