from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    CustomUserProf, Escolas, EscolaPdde,
    TipoDemanda, RoleModulePermission,
    Noticia, Module, UserModulePermission
)

from . import custom_totp_admin  # Força registro do admin customizado
from . import custom_otp_admin  # Força uso dos admins seguros


# ---------- Custom User Admin ----------
@admin.register(CustomUserProf)
class CustomUserProfAdmin(UserAdmin):
    model = CustomUserProf
    list_display = (
        'username', 'first_name', 'last_name', 'cpf',
        'escola', 'is_coordenador', 'is_professor', 'is_active'
    )
    list_filter = ('is_coordenador', 'is_professor', 'is_active', 'escola')
    search_fields = ('username', 'first_name', 'last_name', 'cpf', 'matricula')
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações Pessoais', {
            'fields': ('first_name', 'last_name', 'cpf', 'email', 'telefone', 'especializacao', 'matricula')
        }),
        ('Vínculo com Escolas', {
            'fields': ('escola', 'escolas', 'escola_pdde', 'is_coordenador', 'is_professor')
        }),
        ('Permissões', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Datas importantes', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'cpf', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )


# ---------- Escola Principal ----------
@admin.register(Escolas)
class EscolasAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'codigo_inep', 'cidade', 'bairro', 'uf', 'dependencia_administrativa')
    list_filter = ('cidade', 'uf', 'ano')
    search_fields = ('nome', 'codigo_inep', 'cidade', 'bairro')


# ---------- Escola PDDE ----------
@admin.register(EscolaPdde)
class EscolaPddeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'codigo_inep', 'cnpj', 'ano', 'status', 'cidade', 'uf', 'coordenador')
    search_fields = ('nome', 'codigo_inep', 'cnpj', 'coordenador__first_name', 'coordenador__last_name')
    list_filter = ('ano', 'status', 'uf', 'zona')
    autocomplete_fields = ['coordenador']


# ---------- Tipo Demanda ----------
@admin.register(TipoDemanda)
class TipoDemandaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'descricao', 'status', 'prioridade', 'data_cadastro']
    list_filter = ['status', 'prioridade', 'data_cadastro']
    search_fields = ['nome', 'descricao']


# ---------- Permissões por Role ----------
@admin.register(RoleModulePermission)
class RoleModulePermissionAdmin(admin.ModelAdmin):
    list_display = ('role', 'module')
    list_filter = ('role',)
    search_fields = ('module__nome',)  # Corrigido


# ---------- Notícias ----------
@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'publicado', 'criado_por', 'criado_em', 'publicado_em')
    list_filter = ('publicado',)
    search_fields = ('titulo',)


# ---------- Módulos ----------
@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'url')  # Corrigido
    search_fields = ('nome', 'url')       # Corrigido


# ---------- Permissões por Usuário ----------
@admin.register(UserModulePermission)
class UserModulePermissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'module')
    search_fields = ('user__username', 'module__nome')  # Corrigido



from .models import CertidaoEmitida
admin.site.register(CertidaoEmitida)
