from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum, Count
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse
from django.middleware.csrf import get_token
import csv
import chardet
import io
import mimetypes
from django.contrib.auth import authenticate, login
from .models import Module, UserModulePermission
from .forms import UserModulePermissionForm
from django.core.exceptions import PermissionDenied
from .models import Habilidade
from django.http import HttpResponse
from .models import Acompanhamento
import datetime
from datetime import date
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import CandidatoCurriculo  # Certifique-se de usar o modelo correto
import os
import pandas as pd
from reportlab.pdfgen import canvas
from .models import PDDE
from .models import Diretoria
from .models import MembroConselho
from .models import LivroCaixa
from .forms import LivroCaixaForm
from .models import EscrituraFiscal
from .forms import EscrituraFiscalForm
from .models import Relatorio
from .models import Escola, Membro, Caixa, Certidao
from .models import Legislacao
from .forms import LegislacaoForm  # Supondo que exista um formulário para legislação
from .models import InscricaoPlanetario  # Substitua pelo nome do modelo correto, se aplicável
from .models import Imagem, Conteudo, Evento, Usuario
from .forms import ImagemForm, ConteudoForm, EventoForm, UsuarioForm
from .models import Funcionario  # Supondo que tenha um modelo Funcionario
from .models import Bairro
from .models import Disciplina
from .models import Inscricao
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.contrib.auth.views import LoginView
from .models import DiagnoseInicProfPort, DiagnoseAlunoMatematica, DiagnoseAlunoPortugues
from .models import Professor,Aluno,HabilidadeMatematica, HabilidadePortugues
from django.core.files.storage import FileSystemStorage
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.conf import settings
from django.templatetags.static import static
from django.contrib.messages import get_messages
from .models import Student, UploadedFile
from django.contrib.auth.models import User  # Importe o modelo padrão do Django
from semedapp.models import IndicadoresTransporte
from .models import IndicadoresTransporte
from django.db.models import Count
from datetime import date
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Funcionario, RegimentoCadastro, Regimento, Registro
#from .forms import FuncionarioForm, RegimentoCadastroForm, RegimentoForm, RegistroForm
from .models import RegimentoCadastro  # Substitua pelo nome do seu modelo
from .models import SemedAppRegimentoCadastro
from semedapp.models import RegimentoCadastro  # Substitua pelo caminho correto do modelo
from .models import HabilidadeProf
from .forms import UploadPlanilhaForm
from .models import HabilidadeProfAnosFinais
from .models import HabilidadeProfFinal  # Ajuste o modelo para anos finais
from .forms import CurriculoForm
from .forms import EscolaForm
from semedapp.forms import DiretorForm  # Certifique-se de que o formulário está configurado corretamente
from .models import Curriculo
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .models import CandidatoAutenticado
from django.contrib import messages
from django.db import IntegrityError
from .forms import FormDeAtualizacao
from semedapp.models import RoleModulePermission

from django.db import IntegrityError
import logging

logger = logging.getLogger(__name__)

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .models import CadastroCandidato
from django.contrib import messages
from .forms import TipoDemandaForm
from .models import TipoDemanda
from .models import Candidato

import qrcode
from io import BytesIO
from django.template.loader import render_to_string
from weasyprint import HTML
from django.views.generic.edit import DeleteView
from .forms import DiretorForm  # Certifique-se de ter um formulário para o modelo Diretor
from django.views.generic import DetailView
from .models import Diretor
from semedapp.models import Diretor
from django.shortcuts import get_object_or_404, redirect
from .forms import ProfessorForm

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

import xlwt
import openpyxl
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.forms import inlineformset_factory
from .models import Formacao, Experiencia
from .forms import CurriculoForm, FormacaoForm, ExperienciaForm



class Site1Backend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(username=username, login_type='site1')
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None



@login_required
def dashboard(request):
    return render(request, 'dashboard.html')
# *********************************************************************************************************************

def BASE(request):
    return render(request, 'base.html')
# *********************************************************************************************************************

@login_required
def dashboard_admin(request):
    user = request.user  # Obtém o usuário autenticado
    return render(request, 'dashboardadmin.html', {'user': user})
# *********************************************************************************************************************

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({
                'status': 'success',
                'message': f'Bem-vindo, {user.first_name}!',
                'redirect_url': '/dashboardadmin/'
            })
        else:
            return JsonResponse({'status': 'error', 'message': 'Usuário ou senha inválidos.'}, status=401)

    # Para GET, retorne o CSRF token
    return JsonResponse({'csrf_token': get_token(request)})
# *********************************************************************************************************************

def definir_permissoes(request):
    return render(request, 'definir_permissoes.html')
# *********************************************************************************************************************

def vinculacoes(request):
    return render(request, 'vinculacoes.html')
# *********************************************************************************************************************

def controle_usuarios(request):
    users = User.objects.all()  # Ou o modelo correto de usuários
    context = {'users': users}
    return render(request, 'controle_usuarios.html', context)

# *********************************************************************************************************************

def gestao_escolar(request):
    return render(request, 'gestao_escolar.html')
# *********************************************************************************************************************

def transporte(request):
    return render(request, 'transporte.html')
# *********************************************************************************************************************

def financeiro(request):
    return render(request, 'financeiro.html')
# *********************************************************************************************************************

def contabilidade(request):
    return render(request, 'contabilidade.html')
# *********************************************************************************************************************

def soe(request):
    return render(request, 'soe.html')
# *********************************************************************************************************************

def pedagogico(request):
    return render(request, 'pedagogico.html')
# *********************************************************************************************************************

def legislacao(request):
    return render(request, 'legislacao.html')
# *********************************************************************************************************************

def logout_view(request):
    logout(request)  # Logs the user out and clears their session
    return redirect('login')  # Replace 'login' with the name of your login URL
# *********************************************************************************************************************

def controle_usuarios(request):
    usuarios = User.objects.all()  # Obtém todos os usuários
    return render(request, 'controle_usuarios.html', {'usuarios': usuarios})
# *********************************************************************************************************************

def adicionar_usuario(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        is_active = request.POST.get('is_active') == 'True'
        is_superuser = 'is_superuser' in request.POST

        try:
            # Criação do usuário
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
            user.is_active = is_active
            user.is_superuser = is_superuser
            user.is_staff = is_superuser
            user.save()

            return JsonResponse({'success': True, 'message': 'Usuário criado com sucesso!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Erro ao criar usuário: {e}'})
    return JsonResponse({'success': False, 'message': 'Requisição inválida.'})
# *********************************************************************************************************************

def transporte_dashboard(request):
    # Adicione lógica para retornar dados relevantes, se necessário
    return render(request, 'transporte_dashboard.html')
# *********************************************************************************************************************

def financeiro_dashboard(request):
    # Adicione lógica ou dados para a dashboard financeira, se necessário
    return render(request, 'financeiro_dashboard.html')
# *********************************************************************************************************************

# Indicadores de Transporte Escolar
def transporte_indicadores(request):
    return render(request, 'indicadores/transporte.html')
# *********************************************************************************************************************

def upload_arquivos(request):
    if request.method == 'POST':
        if 'file' not in request.FILES:
            messages.error(request, 'Nenhum arquivo foi enviado.')
            return redirect('upload_arquivos')

        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'O arquivo deve estar no formato CSV.')
            return redirect('upload_arquivos')

        try:
            # Decodifica o arquivo CSV
            file_data = csv_file.read().decode('utf-8')
            csv_data = csv.reader(file_data.splitlines(), delimiter=';')
            
            # Ignorar o cabeçalho
            header = next(csv_data, None)

            for row in csv_data:
                try:
                    # Converte o formato da data
                    data_nascimento = datetime.strptime(row[3], '%d/%m/%Y').strftime('%Y-%m-%d')

                    # Cria o objeto no banco de dados
                    IndicadoresTransporte.objects.create(
                        numero_matricula=row[0],
                        nome_completo=row[1],
                        escola=row[2],
                        data_nascimento=data_nascimento,
                        sexo=row[4],
                        turno=row[5],
                        telefone=row[6],
                        nivel_escolaridade=row[7],
                        endereco=row[8],
                        bairro=row[9],
                        cep=row[10],
                        codigo_rota=row[11],
                        email_responsavel=row[12],
                        cpf_responsavel=row[13],
                        nome_responsavel=row[14],
                        parentesco=row[15],
                        telefone_responsavel=row[16],
                        responsavel_legal=True if row[17].strip().upper() == 'SIM' else False,
                    )
                except Exception as e:
                    # Log de erro por linha
                    print(f"Erro ao processar a linha: {row}. {str(e)}")
                    messages.warning(request, f'Erro ao salvar a linha: {row}. {str(e)}')

            messages.success(request, 'Arquivo processado e dados salvos com sucesso.')
            return redirect('upload_arquivos')
        except Exception as e:
            print(f"Erro ao processar o arquivo: {str(e)}")  # Log para diagnóstico
            messages.error(request, f'Ocorreu um erro ao processar o arquivo: {str(e)}')
            return redirect('upload_arquivos')
    else:
        return render(request, 'upload_arquivos.html')



# *********************************************************************************************************************

# Gestão de Dados
def gestao_dados(request):
    # Exemplo de dados fictícios
    dados = {
        'total_escolas': 50,
        'total_alunos': 1000,
        'alunos_transportados': 300,
    }
    return render(request, 'indicadores/gestao.html', {'dados': dados})
# *********************************************************************************************************************

# Diagnosis
def diagnosis(request):
    # Dados fictícios ou lógica para a página
    dados_diagnosis = {
        'total_escolas_avaliadas': 20,
        'total_alunos_avaliados': 300,
        'medias_gerais': 7.5,
    }
    return render(request, 'pedagogico/diagnosis.html', {'dados': dados_diagnosis})
# *********************************************************************************************************************

# Orientação Educacional
def orientacao_educacional(request):
    return render(request, 'pedagogico/orientacao.html')
# *********************************************************************************************************************

# Legislação
def legislacao(request):
    # Dados fictícios ou lógica para a página
    legislacao_dados = {
        'total_leis': 15,
        'total_normas': 30,
    }
    return render(request, 'setor_pedagogico/legislacao.html', {'dados': legislacao_dados})
# *********************************************************************************************************************

# Escolas
def escolas(request):
    dados_escolas = {
        'total_escolas': 10,
        'escolas_ativas': 8,
        'escolas_inativas': 2,
    }
    return render(request, 'contabilidade/escolas.html', {'dados': dados_escolas})
# *********************************************************************************************************************

# Conselho
def conselho(request):
    dados_conselho = {
        'total_conselheiros': 5,
        'reunioes_ano': 12,
    }
    return render(request, 'contabilidade/conselho.html', {'dados': dados_conselho})
# *********************************************************************************************************************

# Contas
def contas(request):
    dados_contas = {
        'saldo_total': 50000,
        'despesas_mes': 15000,
        'receitas_mes': 20000,
    }
    return render(request, 'contabilidade/contas.html', {'dados': dados_contas})
# *********************************************************************************************************************

def dashboardadmin(request):
    modules = [
        {"name": "Gestão Escolar", "url": reverse('gestao_escolar'), "icon": "fas fa-school", "color": "primary"},
        {"name": "Transporte Escolar", "url": reverse('transporte_dashboard'), "icon": "fas fa-bus", "color": "success"},
        {"name": "Financeiro", "url": reverse('financeiro_dashboard'), "icon": "fas fa-dollar-sign", "color": "warning"},
        {"name": "Indicadores", "url": reverse('indicadores'), "icon": "fas fa-chart-bar", "color": "info"},
        {"name": "Pedagógico", "url": reverse('pedagogico'), "icon": "fas fa-book", "color": "secondary"},
    ]
    return render(request, 'dashboardadmin.html', {'modules': modules})
# ********************************************************************************************************************

def transporte_escolar(request):
    try:
        # Consulta os dados do banco de dados
        total_alunos = IndicadoresTransporte.objects.count()
        total_escolas = IndicadoresTransporte.objects.values('escola').distinct().count()
        alunos_ensino_medio = IndicadoresTransporte.objects.filter(
            nivel_escolaridade__icontains='Ensino Médio'
        ).count()
        alunos_ensino_fundamental = IndicadoresTransporte.objects.filter(
            nivel_escolaridade__icontains='Ensino Fundamental'
        ).count()

        # Prepara os dados para o gráfico de barras
        alunos_por_escola = (
            IndicadoresTransporte.objects
            .values('escola')
            .annotate(total=Count('id'))
            .order_by('-total')
        )

        escolas = [item['escola'] for item in alunos_por_escola]
        alunos = [item['total'] for item in alunos_por_escola]

        # Passa os dados para o template
        context = {
            'total_alunos': total_alunos,
            'total_escolas': total_escolas,
            'alunos_ensino_medio': alunos_ensino_medio,
            'alunos_ensino_fundamental': alunos_ensino_fundamental,
            'escolas': escolas,
            'alunos': alunos,
        }

        return render(request, 'indicadores/transporte.html', context)

    except Exception as e:
        # Em caso de erro, exibe uma página de erro ou mensagem
        return render(request, 'indicadores/erro.html', {'mensagem_erro': str(e)})


# *********************************************************************************************************************

# def upload_arquivos(request):
#     # Substitua o conteúdo abaixo com a lógica da sua visão
#     return render(request, 'indicadores/upload.html')
# *********************************************************************************************************************

def gestao_dados(request):
    # Substitua o conteúdo abaixo com a lógica necessária
    return render(request, 'indicadores/gestao.html')
# *********************************************************************************************************************

def diagnosis(request):
    # Lógica ou dados para a página de Diagnosis
    return render(request, 'diagnosis.html')
# *********************************************************************************************************************

def orientacao_educacional(request):
    # Adicione lógica para Orientação Educacional, se necessário
    return render(request, 'orientacao_educacional.html')
# *********************************************************************************************************************

def escolas(request):
    # Adicione lógica específica, se necessário
    return render(request, 'escolas.html')
# *********************************************************************************************************************

def conselho(request):
    # Adicione lógica específica para o conselho, se necessário
    return render(request, 'conselho.html')
# *********************************************************************************************************************

def contas(request):
    # Adicione lógica específica para contas, se necessário
    return render(request, 'contas.html')
# *********************************************************************************************************************

def site_curriculos(request):
    return render(request, 'site_curriculos.html')  # Use o template correto
# *********************************************************************************************************************

def cadastro_curriculo(request):
    return render(request, 'cadastro_curriculo.html')  # Certifique-se de que o template existe
# *********************************************************************************************************************

def gestao_curriculo(request):
    return render(request, 'gestao_curriculo.html')  # Certifique-se de criar o template.
# *********************************************************************************************************************

def gestao_conteudo(request):
    return render(request, 'gestao_conteudo.html')
# *********************************************************************************************************************

def index(request):
    return render(request, 'index.html')
# *********************************************************************************************************************

def cadastro_imagens(request):
    return render(request, 'cadastro_imagens.html')
# *********************************************************************************************************************

def cadastro_conteudo(request):
    return render(request, 'cadastro_conteudo.html')
# *********************************************************************************************************************

def gestao_noticias(request):
    return render(request, 'gestao_noticias.html')
# *********************************************************************************************************************

def gestao_eventos(request):
    return render(request, 'gestao_eventos.html')
# *********************************************************************************************************************

def configuracoes_site(request):
    return render(request, 'configuracoes_site.html')
# *********************************************************************************************************************

def estatisticas_site(request):
    return render(request, 'estatisticas_site.html')
# *********************************************************************************************************************

def gestao_usuarios_site(request):
    return render(request, 'gestao_usuarios_site.html')
# *********************************************************************************************************************

def gestao_processos(request):
    # Lógica da view (por exemplo, buscar processos do banco de dados)
    return render(request, 'gestao_processos.html')
# *********************************************************************************************************************

def relatorios(request):
    # Lógica da view para exibir os relatórios
    return render(request, 'relatorios.html')
# *********************************************************************************************************************

def setor_pedagogico(request):
    return render(request, 'setor_pedagogico/index.html')
# *********************************************************************************************************************

def gestao_habilidades(request):
    return render(request, 'setor_pedagogico/gestao_habilidades.html')
# *********************************************************************************************************************

def indicadores_educacionais(request):
    return render(request, 'setor_pedagogico/indicadores.html')
# *********************************************************************************************************************

def relatorios_pedagogicos(request):
    return render(request, 'setor_pedagogico/relatorios.html')
# *********************************************************************************************************************

def diagnosis_prof_portugues(request):
    return render(request, 'diagnosis/prof/portugues.html')
# *********************************************************************************************************************

def diagnosis_prof_matematica(request):
    return render(request, 'diagnosis/prof/matematica.html')
# *********************************************************************************************************************

def diagnosis_aluno_portugues(request):
    return render(request, 'diagnosis/aluno/portugues.html')
# *********************************************************************************************************************

def diagnosis_aluno_matematica(request):
    return render(request, 'diagnosis/aluno/matematica.html')
# *********************************************************************************************************************

def diagnosis_eja_site(request):
    return render(request, 'diagnosis/eja/site.html')
# *********************************************************************************************************************

def diagnosis_eja_adm(request):
    return render(request, 'diagnosis/eja/adm.html')
# *********************************************************************************************************************

def admin_eja_noticias(request):
    return render(request, 'diagnosis/eja/admin_noticias.html')
# *********************************************************************************************************************

def admin_eja_eventos(request):
    return render(request, 'diagnosis/eja/admin_eventos.html')
# *********************************************************************************************************************

def admin_eja_relatorios(request):
    return render(request, 'diagnosis/eja/admin_relatorios.html')
# *********************************************************************************************************************
def admin_site_eja(request):
    return render(request, 'diagnosis/eja/admin_dashboard.html')
# *********************************************************************************************************************

def diagnosis_emcceja(request):
    return render(request, 'diagnosis/emcceja.html')
# *********************************************************************************************************************

def indicadores_setor_pedagogico(request):
    return render(request, 'setor_pedagogico/indicadores.html')
# *********************************************************************************************************************

@login_required
def gerenciar_permissoes(request):
    users = User.objects.all()
    permissions = Permission.objects.all()
    groups = Group.objects.all()
    return render(request, 'configuracoes/gerenciar_permissoes.html', {
        'users': users,
        'permissions': permissions,
        'groups': groups,
    })

# *********************************************************************************************************************

@login_required
def add_user(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        email = request.POST.get('email')
        user_type = request.POST.get('user_type')

        # Criar usuário
        user = User.objects.create_user(
            username=email, 
            email=email, 
            first_name=first_name
        )

        # Atribuir tipo
        if user_type == "admin":
            user.is_superuser = True
            user.is_staff = True
        elif user_type == "staff":
            user.is_staff = True

        user.save()
        messages.success(request, "Usuário adicionado com sucesso!")
        return redirect('gerenciar_permissoes')

    return redirect('gerenciar_permissoes')
# *********************************************************************************************************************

@login_required
def edit_permissions(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        # Atualizar permissões do usuário
        permissions = request.POST.getlist('permissions')
        user.user_permissions.set(Permission.objects.filter(id__in=permissions))

        # Atualizar grupos do usuário
        groups = request.POST.getlist('groups')
        user.groups.set(Group.objects.filter(id__in=groups))

        # Atualizar permissões dos grupos
        group_permissions = request.POST.getlist('group_permissions')
        group_permission_map = {}
        for group_permission in group_permissions:
            group_id, permission_id = group_permission.split('-')
            if group_id not in group_permission_map:
                group_permission_map[group_id] = []
            group_permission_map[group_id].append(permission_id)

        for group_id, permission_ids in group_permission_map.items():
            group = Group.objects.get(id=group_id)
            group.permissions.set(Permission.objects.filter(id__in=permission_ids))

        user.save()
        messages.success(request, "Permissões e grupos atualizados com sucesso.")
        return redirect('gerenciar_permissoes')

    return redirect('gerenciar_permissoes')
# *********************************************************************************************************************

@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, "Usuário excluído com sucesso!")
    return redirect('gerenciar_permissoes')
# *********************************************************************************************************************

def manage_permissions(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        user = get_object_or_404(User, id=user_id)

        group_ids = request.POST.getlist("groups")
        user.groups.set(Group.objects.filter(id__in=group_ids))

        permission_ids = request.POST.getlist("permissions")
        user.user_permissions.set(Permission.objects.filter(id__in=permission_ids))

        for group in Group.objects.all():
            group_permission_ids = request.POST.getlist(f"group_permissions_{group.id}")
            group.permissions.set(Permission.objects.filter(id__in=group_permission_ids))

        messages.success(request, "Permissões atualizadas!")
        return redirect("gerenciar_permissoes")
# *********************************************************************************************************************

def add_group(request):
    if request.method == 'POST':
        group_name = request.POST.get('group_name')
        if group_name:
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                messages.success(request, f'Grupo "{group_name}" adicionado com sucesso.')
            else:
                messages.warning(request, f'O grupo "{group_name}" já existe.')
        else:
            messages.error(request, 'O nome do grupo não pode estar vazio.')
    return redirect('gerenciar_permissoes')
# *********************************************************************************************************************

def add_permission(request):
    if request.method == 'POST':
        permission_name = request.POST.get('permission_name')
        permission_codename = request.POST.get('permission_codename')
        app_label = request.POST.get('app_label')
        model_name = request.POST.get('model_name')

        if permission_name and permission_codename and app_label and model_name:
            content_type, created = ContentType.objects.get_or_create(
                app_label=app_label, model=model_name
            )
            Permission.objects.create(
                name=permission_name,
                codename=permission_codename,
                content_type=content_type,
            )
            messages.success(request, f'Permissão "{permission_name}" adicionada com sucesso.')
        else:
            messages.error(request, 'Todos os campos são obrigatórios.')

    return redirect('gerenciar_permissoes')
# *********************************************************************************************************************

@login_required
def dashboard_view(request):
    user_modules = UserModulePermission.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'user_modules': user_modules})
# *********************************************************************************************************************

def check_module_permission(user, module_name):
    if not UserModulePermission.objects.filter(user=user, module=module_name).exists():
        raise PermissionDenied
# *********************************************************************************************************************

@login_required
def configuracao_view(request):
    if not check_module_permission(request.user, 'configuracao'):
        return redirect('no_access')  # Redireciona para página de acesso negado
    return render(request, 'configuracao.html')
# *********************************************************************************************************************
# Somente administradores podem configurar acessos
def is_admin(user):
    return user.is_staff or user.is_superuser

@user_passes_test(is_admin)
@login_required
def configure_access_view(request):
    if request.method == 'POST':
        form = UserModulePermissionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('configure_access')
    else:
        form = UserModulePermissionForm()

    permissions = UserModulePermission.objects.all()
    return render(request, 'configure_access.html', {'form': form, 'permissions': permissions})
# *********************************************************************************************************************

def check_module_permission(user, module):
    return UserModulePermission.objects.filter(user=user, module=module).exists()
# *********************************************************************************************************************

# Exemplo de uso em uma view
@login_required
def some_module_view(request):
    if not check_module_permission(request.user, 'pedagogico'):
        return redirect('no_access')  # Redireciona se o usuário não tiver acesso
    return render(request, 'pedagogico.html')
# *********************************************************************************************************************
@login_required
def indicadores_view(request):
    if not check_module_permission(request.user, 'indicadores'):
        return redirect('no_access')
    return render(request, 'indicadores.html')

# Repita para cada módulo
# *********************************************************************************************************************

@login_required
def access_user_modules(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user_modules = UserModulePermission.objects.filter(user=user)
    return render(request, 'dashboard.html', {'user': user, 'user_modules': user_modules})

# *********************************************************************************************************************

@login_required
def configure_user_modules(request, user_id):
    user = get_object_or_404(User, id=user_id)
    modules = Module.objects.all()

    if request.method == 'POST':
        selected_modules = request.POST.getlist('modules')
        # Limpa permissões antigas
        UserModulePermission.objects.filter(user=user).delete()
        # Adiciona novas permissões
        for module_id in selected_modules:
            module = get_object_or_404(Module, id=module_id)
            UserModulePermission.objects.create(user=user, module=module)
        return redirect('dashboard')  # Redireciona ao dashboard ou outra página

    user_modules = user.module_permissions.values_list('module_id', flat=True)
    return render(request, 'configure_modules.html', {
        'user': user,
        'modules': modules,
        'user_modules': user_modules,
    })

@login_required
def curriculos_view(request):
    # Substitua 'curriculos.html' pelo template correto para esta página
    return render(request, 'curriculos.html', {})
# *********************************************************************************************************************

@login_required
def modulo_view(request, slug):
    module = get_object_or_404(Module, slug=slug)
    return render(request, 'modulo.html', {'module': module})
# *********************************************************************************************************************

def update_habilidades(request):
    if request.method == 'POST':
        aluno_id = request.POST.get('aluno')
        habilidade_nome = request.POST.get('habilidade')
        # Salvar ou atualizar no banco de dados
        Habilidade.objects.create(aluno_id=aluno_id, nome=habilidade_nome)
        return redirect('gestao_habilidades')  # Redirecionar para a página atual
    return HttpResponse("Método não permitido.", status=405)
# *********************************************************************************************************************

def download_relatorio(request, tipo_relatorio):
    # Lógica para gerar ou buscar o relatório com base no tipo
    if tipo_relatorio == "aprovacao":
        # Simule o arquivo do relatório
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="taxa_aprovacao.pdf"'
        response.write("Conteúdo do relatório de aprovação")  # Substitua por geração de PDF
    elif tipo_relatorio == "frequencia":
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="frequencia.pdf"'
        response.write("Conteúdo do relatório de frequência")  # Substitua por geração de PDF
    elif tipo_relatorio == "desempenho":
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="desempenho.pdf"'
        response.write("Conteúdo do relatório de desempenho")  # Substitua por geração de PDF
    else:
        return HttpResponse("Relatório não encontrado", status=404)

    return response
# *********************************************************************************************************************

def agenda_educacional(request):
    return render(request, 'setor_pedagogico/agenda_educacional.html')
# *********************************************************************************************************************

def acompanhamento_individual(request):
    return render(request, 'setor_pedagogico/acompanhamento_individual.html')
# *********************************************************************************************************************

def registrar_acompanhamento(request):
    if request.method == 'POST':
        aluno_id = request.POST.get('aluno')
        descricao = request.POST.get('descricao')

        if aluno_id and descricao:
            Acompanhamento.objects.create(aluno_id=aluno_id, descricao=descricao)
            messages.success(request, 'Acompanhamento registrado com sucesso.')
            return redirect('orientacao_educacional')  # Substitua pelo nome correto da view de redirecionamento
        else:
            messages.error(request, 'Preencha todos os campos.')

    return render(request, 'orientacao_educacional.html')
# *********************************************************************************************************************

def pdde_view(request):
    anos = [2022, 2023, 2024]  # Example data
    pdde_data = [
        {'ano': 2023, 'escola': 'Escola A', 'status': 'aprovado'},
        {'ano': 2024, 'escola': 'Escola B', 'status': 'pendente'},
    ]
    return render(request, 'contabilidade/pdde.html', {'anos': anos, 'pdde_data': pdde_data})
# *********************************************************************************************************************

def conselho_diretoria(request):
    # Example context data
    diretoria_data = [
        {'nome': 'João Silva', 'cargo': 'Presidente'},
        {'nome': 'Maria Oliveira', 'cargo': 'Vice-presidente'},
        {'nome': 'Carlos Souza', 'cargo': 'Tesoureiro'},
    ]
    return render(request, 'contabilidade/conselho/diretoria.html', {'diretoria_data': diretoria_data})
# *********************************************************************************************************************

def conselho_membros(request):
    # Example context data
    membros_data = [
        {'nome': 'Ana Pereira', 'funcao': 'Conselheira'},
        {'nome': 'Carlos Silva', 'funcao': 'Conselheiro'},
        {'nome': 'Beatriz Costa', 'funcao': 'Secretária'},
    ]
    return render(request, 'contabilidade/conselho/membros.html', {'membros_data': membros_data})
# *********************************************************************************************************************

def download_page(request):
    # Diretório onde os manuais estão armazenados
    manuals_dir = os.path.join('media', 'manuals')
    
    # Listar todos os arquivos no diretório de manuais
    if os.path.exists(manuals_dir):
        manuals = os.listdir(manuals_dir)
    else:
        manuals = []

    return render(request, 'downloads/manuals_list.html', {'manuals': manuals})
# *********************************************************************************************************************

def pdde(request):
    context = {
        'range_10': range(10)  # Cria um range de 10 para usar no template
    }
    return render(request, 'contabilidade/pdde.html', context)

def pdde(request):
    context = {
        'range_3': range(3)  # Cria um range de 3 para usar no template
    }
    return render(request, 'contabilidade/pdde.html', context)
# *********************************************************************************************************************

def pdde(request):
    context = {
        'range_5': range(5)  # Cria um range de 5 para usar no template
    }
    return render(request, 'contabilidade/pdde.html', context)
# *********************************************************************************************************************

def view_pdde(request, pdde_id):
    return HttpResponse(f"Detalhes do PDDE com ID: {pdde_id}")
# *********************************************************************************************************************

def download_manual(request, file_name):
    file_path = os.path.join('media/manuals', file_name)  # Caminho relativo
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/pdf")
            response['Content-Disposition'] = f'attachment; filename={file_name}'
            return response
    else:
        return HttpResponse("Arquivo não encontrado.", status=404)
# *********************************************************************************************************************

def pdde_view(request):
    # Filtros
    ano = request.GET.get('year', None)
    status = request.GET.get('status', None)

    # Consulta com filtros
    pdde_data = PDDE.objects.all()
    if ano:
        pdde_data = pdde_data.filter(ano=ano)
    if status:
        pdde_data = pdde_data.filter(status=status)

    # Anos únicos para o filtro
    anos = PDDE.objects.values_list('ano', flat=True).distinct().order_by('-ano')

    context = {
        'pdde_data': pdde_data,
        'anos': anos,
    }
    return render(request, 'app/pdde.html', context)
# *********************************************************************************************************************

def cadastro_diretoria(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        cargo = request.POST.get("cargo")
        endereco = request.POST.get("endereco")
        bairro = request.POST.get("bairro")
        telefone = request.POST.get("telefone")
        email = request.POST.get("email")
        cep = request.POST.get("cep")
        cpf = request.POST.get("cpf")

        # Salvar os dados no banco
        Diretoria.objects.create(
            nome=nome,
            cargo=cargo,
            endereco=endereco,
            bairro=bairro,
            telefone=telefone,
            email=email,
            cep=cep,
            cpf=cpf,
        )
        messages.success(request, "Membro cadastrado com sucesso!")
        return redirect("diretoria")  # Substitua por sua URL correspondente à página da diretoria

    return render(request, "contabilidade/conselho/diretoria.html")
# *********************************************************************************************************************

def listar_membros(request):
    """
    Exibe a lista de membros do conselho.
    """
    membros_data = MembroConselho.objects.all()
    return render(request, 'contabilidade/conselho/membros.html', {'membros_data': membros_data})
# *********************************************************************************************************************

def cadastrar_membro(request):
    """
    Processa o formulário de cadastro de novos membros do conselho.
    """
    if request.method == 'POST':
        try:
            # Recuperar dados do formulário
            inep = request.POST.get('inep')
            escola = request.POST.get('escola')
            data_abertura = request.POST.get('data_abertura')
            data_vencimento = request.POST.get('data_vencimento')
            nome = request.POST.get('nome')
            funcao = request.POST.get('funcao')
            endereco = request.POST.get('endereco')
            bairro = request.POST.get('bairro')
            telefone = request.POST.get('telefone')
            email = request.POST.get('email')
            cep = request.POST.get('cep')
            cpf = request.POST.get('cpf')

            # Criar novo membro
            novo_membro = MembroConselho(
                inep=inep,
                escola=escola,
                data_abertura=data_abertura,
                data_vencimento=data_vencimento,
                nome=nome,
                funcao=funcao,
                endereco=endereco,
                bairro=bairro,
                telefone=telefone,
                email=email,
                cep=cep,
                cpf=cpf,
            )
            novo_membro.save()

            # Mensagem de sucesso
            messages.success(request, 'Membro cadastrado com sucesso!')
            return redirect('listar_membros')

        except Exception as e:
            # Mensagem de erro
            messages.error(request, f'Ocorreu um erro ao cadastrar o membro: {e}')
            return redirect('listar_membros')
    else:
        return redirect('listar_membros')
# *********************************************************************************************************************

def listar_livro_caixa(request):
    """
    Exibe o Livro Caixa com as entradas cadastradas.
    """
    entradas_caixa = LivroCaixa.objects.all().order_by('-data')
    return render(request, 'contabilidade/conselho/caixa.html', {'entradas_caixa': entradas_caixa})


def adicionar_livro_caixa(request):
    """
    Adiciona uma nova entrada ao Livro Caixa.
    """
    if request.method == 'POST':
        try:
            descricao = request.POST.get('descricao')
            tipo = request.POST.get('tipo')  # 'Receita' ou 'Despesa'
            valor = float(request.POST.get('valor'))
            data = request.POST.get('data')

            nova_entrada = LivroCaixa(
                descricao=descricao,
                tipo=tipo,
                valor=valor,
                data=data,
            )
            nova_entrada.save()

            # Mensagem de sucesso
            messages.success(request, 'Entrada adicionada com sucesso ao Livro Caixa!')
            return redirect('listar_livro_caixa')

        except Exception as e:
            # Mensagem de erro
            messages.error(request, f'Ocorreu um erro ao adicionar a entrada: {e}')
            return redirect('listar_livro_caixa')

    return render(request, 'contabilidade/conselho/adicionar_caixa.html')
# *********************************************************************************************************************
# View para listar o Livro Caixa
def listar_livro_caixa(request):
    registros = LivroCaixa.objects.all()
    return render(request, 'contabilidade/caixa.html', {'registros': registros})
# *********************************************************************************************************************
# View para adicionar um registro no Livro Caixa
def adicionar_livro_caixa(request):
    if request.method == 'POST':
        form = LivroCaixaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_livro_caixa')
    else:
        form = LivroCaixaForm()
    return render(request, 'contabilidade/adicionar_caixa.html', {'form': form})
# *********************************************************************************************************************

def adicionar_escritura_fiscal(request):
    if request.method == 'POST':
        form = EscrituraFiscalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_livro_caixa')
    else:
        form = EscrituraFiscalForm()
    return render(request, 'contabilidade/adicionar_caixa.html', {'form': form})
# *********************************************************************************************************************

def adicionar_escritura_fiscal(request):
    if request.method == 'POST':
        form = EscrituraFiscalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_livro_caixa')  # Certifique-se de que essa URL está configurada
    else:
        form = EscrituraFiscalForm()
    return render(request, 'contabilidade/adicionar_caixa.html', {'form': form})
# *********************************************************************************************************************

def adicionar_escrituracao(request):
    if request.method == 'POST':
        # Captura os dados do formulário
        ano_base = request.POST.get('ano_base')
        conselho_escolar = request.POST.get('conselho_escolar')
        cnpj = request.POST.get('cnpj')
        rendimentos_aplicacao = request.POST.get('rendimentos_aplicacao')
        saldo_anterior = request.POST.get('saldo_anterior')
        despesas_manutencao = request.POST.get('despesas_manutencao')

        # Realiza cálculos
        receita_total = float(rendimentos_aplicacao) + float(saldo_anterior)
        despesa_total = float(despesas_manutencao)
        superavit_deficit = receita_total - despesa_total

        # Aqui você pode salvar os dados no banco de dados
        # Exemplo:
        # model_instance = LivroCaixa(
        #     ano_base=ano_base,
        #     conselho_escolar=conselho_escolar,
        #     cnpj=cnpj,
        #     rendimentos_aplicacao=rendimentos_aplicacao,
        #     saldo_anterior=saldo_anterior,
        #     receita_total=receita_total,
        #     despesas_manutencao=despesas_manutencao,
        #     despesa_total=despesa_total,
        #     superavit_deficit=superavit_deficit
        # )
        # model_instance.save()

        # Exibe uma mensagem de sucesso
        messages.success(request, 'Escrituração contábil adicionada com sucesso!')
        return redirect('contabilidade:caixa')  # Redirecione para a lista de registros ou página desejada

    # Renderiza o template do modal
    return render(request, 'contabilidade/adicionar_caixa.html')
# *********************************************************************************************************************

def listar_relatorios_pdde(request):
    # Filtros
    tipo_relatorio = request.GET.get('tipo_relatorio', '')
    ano = request.GET.get('ano', '')
    escola = request.GET.get('escola', '')

    # Query básica
    relatorios = Relatorio.objects.all()

    # Aplica filtros se disponíveis
    if tipo_relatorio:
        relatorios = relatorios.filter(tipo__icontains=tipo_relatorio)
    if ano:
        relatorios = relatorios.filter(ano=ano)
    if escola:
        relatorios = relatorios.filter(escola__icontains=escola)

    context = {
        'relatorios_data': relatorios,
    }
    return render(request, 'contabilidade/relatorios_pdde.html', context)
# *********************************************************************************************************************

def emissao_certidoes(request):
    certidoes_data = [
        {'id': 1, 'nome': 'DEMOSTRATIVO EDUCAÇAO BÁSICA', 'descricao': 'Confirma a inexistência de débitos.', 'data_emissao': datetime.date.today()},
        {'id': 2, 'nome': 'SALDO BANCARIO PDDE EDUCAÇÃO BASICA', 'descricao': 'Atesta a regularidade cadastral.', 'data_emissao': datetime.date.today()},
        {'id': 3, 'nome': 'CHECK LIST EXECUÇÃO RECURSO', 'descricao': 'Declara a quitação de obrigações.', 'data_emissao': datetime.date.today()},
        {'id': 4, 'nome': 'PDDE PRESTAÇÃO DE CONTAS', 'descricao': 'Declara a quitação de obrigações.', 'data_emissao': datetime.date.today()},
        {'id': 5, 'nome': 'DADOS FINANCEIRO', 'descricao': 'Declara a quitação de obrigações.', 'data_emissao': datetime.date.today()},
        {'id': 6, 'nome': 'ATA DE PLANEJAMENTO ANUAL', 'descricao': 'Declara a quitação de obrigações.', 'data_emissao': datetime.date.today()},
        {'id': 7, 'nome': 'RECURSOS POR ESCOLA', 'descricao': 'Declara a quitação de obrigações.', 'data_emissao': datetime.date.today()},
    ]

    context = {
        'certidoes': certidoes_data,
    }

    return render(request, 'contabilidade/emissao_certidoes.html', context)
# *********************************************************************************************************************

def dashboard(request):
    context = {
        "total_escolas": Escola.objects.count(),
        "total_membros": Membro.objects.count(),
        "total_pdde": PDDE.objects.aggregate(total=Sum('valor'))['total'] or 0,
        "total_caixas": Caixa.objects.aggregate(total=Sum('saldo'))['total'] or 0,
        "total_certidoes": Certidao.objects.count(),
        "recent_certidoes": Certidao.objects.order_by('-data_emissao')[:5],
        "recent_movements": PDDE.objects.order_by('-data_movimentacao')[:5],
    }
    return render(request, 'dashboard/seppec_dashboard.html', context)
# *********************************************************************************************************************

def dashboard_view(request):
    # Lógica da dashboard (substitua conforme necessário)
    context = {
        'title': 'Dashboard SEPPEC',
        # Adicione outros dados ao contexto, se necessário
    }
    return render(request, 'dashboard.html', context)
# *********************************************************************************************************************

def listar_documentos(request):
    # Substitua pelo código real para buscar documentos
    documentos = []  # Exemplo: Documento.objects.all()
    return render(request, 'setor_pedagogico/documentos_list.html', {'documentos': documentos})
# *********************************************************************************************************************

def gerenciar_categorias(request):
    # Substitua pelo código real para buscar categorias
    categorias = []  # Exemplo: Categoria.objects.all()
    return render(request, 'setor_pedagogico/categorias_list.html', {'categorias': categorias})
# *********************************************************************************************************************

def relatorio_atualizacoes(request):
    # Exemplo: Carregar dados de atualizações recentes
    atualizacoes = []  # Exemplo: Atualizacao.objects.filter(data__gte=hoje - timedelta(days=30))
    total_atualizacoes = len(atualizacoes)
    return render(request, 'setor_pedagogico/relatorio_atualizacoes.html', {
        'atualizacoes': atualizacoes,
        'total_atualizacoes': total_atualizacoes,
    })
# *********************************************************************************************************************

def adicionar_legislacao(request):
    if request.method == 'POST':
        form = LegislacaoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Legislação adicionada com sucesso!')
            return redirect('legislacao')  # Redireciona para a página principal de legislação
    else:
        form = LegislacaoForm()

    return render(request, 'setor_pedagogico/adicionar_legislacao.html', {'form': form})
# *********************************************************************************************************************

def planetario(request):
    return render(request, 'planetario.html')
# *********************************************************************************************************************

def planetario_inscricao(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        atividade = request.POST.get('atividade')
        mensagem = request.POST.get('mensagem')

        InscricaoPlanetario.objects.create(
            nome=nome,
            email=email,
            telefone=telefone,
            atividade=atividade,
            mensagem=mensagem
        )

        return render(request, 'planetario_sucesso.html')

    return render(request, 'planetario_inscricao.html')
# *********************************************************************************************************************

def galeria(request):
    imagens = Imagem.objects.all()
    return render(request, 'galeria.html', {'imagens': imagens})
# *********************************************************************************************************************

def galeria_view(request):
    imagens = Imagem.objects.all()  # Certifique-se de que o modelo `Imagem` está configurado corretamente
    return render(request, 'nome_do_template.html', {'imagens': imagens})
# *********************************************************************************************************************

# Gestão de Imagens
def gerenciar_imagens(request):
    imagens = Imagem.objects.all()
    return render(request, 'cadastro_imagens.html', {'imagens': imagens})
# *********************************************************************************************************************

# Gestão de Imagens
def adicionar_imagem(request):
    if request.method == 'POST':
        form = ImagemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('galeria')  # Redirecione para a galeria após salvar
    else:
        form = ImagemForm()
    return render(request, 'adicionar_imagem.html', {'form': form})
# *********************************************************************************************************************

def lista_imagens(request):
    imagens = Imagem.objects.all().order_by('-data_criacao')
    return render(request, 'lista_imagens.html', {'imagens': imagens})
# *********************************************************************************************************************
# Gestão de Conteúdo
def gerenciar_conteudo(request):
    conteudos = Conteudo.objects.all()
    return render(request, 'cadastro_conteudo.html', {'conteudos': conteudos})
# *********************************************************************************************************************
# Gestão de Conteúdo
def adicionar_conteudo(request):
    if request.method == 'POST':
        form = ConteudoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('gerenciar_conteudo')
    else:
        form = ConteudoForm()
    return render(request, 'adicionar_conteudo.html', {'form': form})

# *********************************************************************************************************************
# Gestão de Eventos
def gerenciar_eventos(request):
    eventos = Evento.objects.all()
    return render(request, 'gestao_eventos.html', {'eventos': eventos})
# *********************************************************************************************************************

def adicionar_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gerenciar_eventos')
    else:
        form = EventoForm()
    return render(request, 'adicionar_evento.html', {'form': form})
# *********************************************************************************************************************
# Gestão de Usuários
def gerenciar_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'gestao_usuarios_site.html', {'usuarios': usuarios})

# *********************************************************************************************************************

def adicionar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gerenciar_usuarios')
    else:
        form = UsuarioForm()
    return render(request, 'adicionar_usuario.html', {'form': form})
# *********************************************************************************************************************

def site_semed(request):
    return render(request, 'sitesemed.html')
# *********************************************************************************************************************

def cadastro_imagens(request):
    return render(request, 'cadastro_imagens.html')
# *********************************************************************************************************************

def cadastro_conteudo(request):
    return render(request, 'cadastro_conteudo.html')
# *********************************************************************************************************************

def gestao_conteudo(request):
    return render(request, 'gestao_conteudo.html')
# *********************************************************************************************************************

def gestao_noticias(request):
    return render(request, 'gestao_noticias.html')
# *********************************************************************************************************************

def gestao_eventos(request):
    return render(request, 'gestao_eventos.html')
# *********************************************************************************************************************

def configuracoes_site(request):
    return render(request, 'configuracoes_site.html')
# *********************************************************************************************************************

def estatisticas_site(request):
    return render(request, 'estatisticas_site.html')
# *********************************************************************************************************************

def gestao_usuarios_site(request):
    return render(request, 'gestao_usuarios_site.html')
# *********************************************************************************************************************

# View para a apresentação
def apresentacao(request):
    return render(request, 'apresentacao.html')
# *********************************************************************************************************************

# View para as atribuições
def atribuicoes(request):
    return render(request, 'atribuicoes.html')
# *********************************************************************************************************************

# View para os contatos
def contatos(request):
    return render(request, 'contatos.html')
# *********************************************************************************************************************

def organograma(request):
    """
    Renderiza a página do Organograma.
    """
    return render(request, 'organograma.html')
# *********************************************************************************************************************

def escolas(request):
    return render(request, 'escolas.html')
# *********************************************************************************************************************

def escola(request):
    return render(request, 'escola.html')
# *********************************************************************************************************************

def centro_viver_conviver(request):
    return render(request, 'centro_viver_conviver.html')
# *********************************************************************************************************************

def centro_formacao(request):
    return render(request, 'centro_formacao.html')
# *********************************************************************************************************************

def diretoria_ensino_superior(request):
    return render(request, 'diretoria_ensino_superior.html')
# *********************************************************************************************************************

def centro_midias_educacionais(request):
    return render(request, 'centro_midias_educacionais.html')
# *********************************************************************************************************************

def conselho_municipal_educacao(request):
    return render(request, 'conselho_municipal_educacao.html')
# *********************************************************************************************************************

def cacs_fundeb(request):
    return render(request, 'cacs_fundeb.html')
# *********************************************************************************************************************

def conselho_alimentacao_escolar(request):
    return render(request, 'conselho_alimentacao_escolar.html')
# *********************************************************************************************************************

def forum_municipal_educacao(request):
    return render(request, 'forum_municipal_educacao.html')
# *********************************************************************************************************************

def fale_conosco(request):
    return render(request, 'faleconosco.html')
# *********************************************************************************************************************

def repositorio(request):
    return render(request, 'repositorio.html')
# *********************************************************************************************************************

def curriculo_ensino(request):
    return render(request, 'curriculo_ensino.html')
# *********************************************************************************************************************

def programas_projetos(request):
    return render(request, 'programas_projetos.html')
# *********************************************************************************************************************

def calendario_escolar(request):
    return render(request, 'calendario_escolar.html')
# *********************************************************************************************************************

def portal_aluno(request):
    return render(request, 'portal_aluno.html')
# *********************************************************************************************************************

def sige(request):
    return render(request, 'sige.html')
# *********************************************************************************************************************

def consulta_publica(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        capitulo = request.POST.get('capitulo')
        tipo_alteracao = request.POST.get('tipo_alteracao')
        justificativa = request.POST.get('justificativa')
        nome_completo = request.POST.get('nome_completo')
        email = request.POST.get('email')
        cpf = request.POST.get('cpf')
        telefone = request.POST.get('telefone')
        cargo = request.POST.get('cargo')
        lotacao = request.POST.get('lotacao')
        observacoes_adicionais = request.POST.get('observacoes_adicionais')

        # Criação do objeto e salvamento no banco
        try:
            RegimentoCadastro.objects.create(
                titulo=titulo,
                capitulo=capitulo,
                tipo_alteracao=tipo_alteracao,
                justificativa=justificativa,
                nome_completo=nome_completo,
                email=email,
                cpf=cpf,
                telefone=telefone,
                cargo=cargo,
                lotacao=lotacao,
                observacoes_adicionais=observacoes_adicionais,
            )
            messages.success(request, "Sua sugestão foi enviada com sucesso!")
        except Exception as e:
            messages.error(request, f"Erro ao salvar a sugestão: {e}")

        return redirect('consulta_publica')  # Redirecione para evitar duplicação ao recarregar a página

    return render(request, 'consulta_publica.html')
# *********************************************************************************************************************

def jornal_escolar(request):
    return render(request, 'jornal_escolar.html')
# *********************************************************************************************************************

def noticia_unifesspa(request):
    return render(request, 'noticias/noticia_unifesspa.html')
# *********************************************************************************************************************

def noticia_eja(request):
    return render(request, 'noticias/noticia_eja.html')
# *********************************************************************************************************************

def noticia_planetario(request):
    return render(request, 'noticias/noticia_planetario.html')
# *********************************************************************************************************************

def programas_projetos(request):
    return render(request, 'programas_projetos.html')
# *********************************************************************************************************************

def portal_aluno(request):
    return render(request, 'portal_aluno.html')
# *********************************************************************************************************************

def emeb_gercino_correa(request):
    return render(request, 'escolas/emeb_gercino_correa.html')
# *********************************************************************************************************************

def emeb_luis_carlos_prestes(request):
    return render(request, 'escolas/emeb_luis_carlos_prestes.html')
# *********************************************************************************************************************

def emeb_ronilton(request):
    return render(request, 'escolas/emeb_ronilton.html')
# *********************************************************************************************************************

def agenda_view(request):
    return render(request, 'agenda.html')
# *********************************************************************************************************************

def inscricoes_view(request):
    return render(request, 'inscricoes.html')
# *********************************************************************************************************************

def certificado_view(request):
    return render(request, 'certificado.html')
# *********************************************************************************************************************

def encontro_pedagogico(request):
    return render(request, 'encontro_pedagogico.html')
# *********************************************************************************************************************

def emef_alexandro_nunes(request):
    return render(request, 'escolas/emef_alexandro_nunes.html')
# *********************************************************************************************************************

def emef_benedita_torres(request):
    return render(request, 'escolas/emef_benedita_torres.html')
# *********************************************************************************************************************

def emef_carmelo_mendes(request):
    return render(request, 'escolas/emef_carmelo_mendes.html')
# *********************************************************************************************************************

def emef_francisca_romana(request):
    return render(request, 'escolas/emef_francisca_romana.html')
# *********************************************************************************************************************

def emef_joao_nelson(request):
    return render(request, 'escolas/emef_joao_nelson.html')
# *********************************************************************************************************************

def emef_maria_lourdes(request):
    return render(request, 'escolas/emef_maria_lourdes.html')
# *********************************************************************************************************************

def sebastiao_agripino(request):
    return render(request, 'escolas/sebastiao_agripino.html')
# *********************************************************************************************************************

def adelaide_molinari(request):
    return render(request, 'escolas/adelaide_molinari.html')
# *********************************************************************************************************************

def carlos_henrique(request):
    return render(request, 'escolas/carlos_henrique.html')
# *********************************************************************************************************************

def juscelino_kubitschek(request):
    return render(request, 'escolas/juscelino_kubitschek.html')
# *********************************************************************************************************************

def emeif_raimundo_oliveira(request):
    return render(request, 'escolas/emeif_raimundo_oliveira.html')
# *********************************************************************************************************************

def emeif_magalhaes_barata(request):
    return render(request, 'escolas/emeif_magalhaes_barata.html')
# *********************************************************************************************************************

def magalhaes_barata(request):
    return render(request, 'escolas/magalhaes_barata.html')
# *********************************************************************************************************************

def tancredo_almeida(request):
    return render(request, 'escolas/tancredo_almeida.html')
# *********************************************************************************************************************

def teotonio_vilela(request):
    return render(request, 'escolas/teotonio_vilela.html')
# *********************************************************************************************************************

def detalhes_escola(request, escola_id):
    # Simulação de dados da escola. Substitua pelos dados reais do seu banco de dados.
    escolas = {
        1: {
            "nome": "EMEIF Maria de Lourdes",
            "descricao": "Uma escola comprometida com o futuro e com a qualidade da educação para todos.",
            "endereco": "Rua Itamarati, S/Nº – Novo Horizonte, Canaã dos Carajás-PA",
            "imagem": "assets/dist/img/escola_1.jpg",
        },
        2: {
            "nome": "EMEIF Juscelino Kubitschek",
            "descricao": "Escola de excelência que transforma vidas através da educação.",
            "endereco": "Avenida Brasil, 123 – Centro, Canaã dos Carajás-PA",
            "imagem": "assets/dist/img/escola_2.jpg",
        },
        3: {
            "nome": "EMEIF Teotônio Vilela",
            "descricao": "Onde o aprendizado se encontra com a dedicação.",
            "endereco": "Rua Amazonas, 456 – Bairro Amazonas, Canaã dos Carajás-PA",
            "imagem": "assets/dist/img/escola_3.jpg",
        },
    }

    escola = escolas.get(escola_id, None)

    if not escola:
        return render(request, "404.html", status=404)  # Exibe página de erro se a escola não existir

    return render(request, "escolas/detalhes_escola.html", {"escola": escola})

# *********************************************************************************************************************

def adicionar_escola(request):
    if request.method == "POST":
        # Aqui você adicionará a lógica para salvar os dados da nova escola.
        nome = request.POST.get("nome")
        descricao = request.POST.get("descricao")
        endereco = request.POST.get("endereco")
        imagem = request.POST.get("imagem")  # Isso dependerá do upload de arquivos

        # Simulação de salvamento (substitua pela lógica de banco de dados)
        print(f"Escola adicionada: {nome}, {descricao}, {endereco}, {imagem}")

        return redirect("escolas")  # Redireciona para a página de escolas

    return render(request, "escolas/adicionar_escola.html")
# *********************************************************************************************************************

def site_pedagogico(request):
    """
    View para a página 'Site Pedagógico'.
    """
    return render(request, 'setor_pedagogico/site_pedagogico.html')
# *********************************************************************************************************************

def verificar_cpf_ajax(request):
    if request.method == 'POST':
        cpf = request.POST.get('cpf')
        try:
            # Fetch user by CPF and check if they are a superuser
            user = User.objects.get(cpf=cpf)
            if user.is_superuser:
                return JsonResponse({'status': 'success', 'redirect_url': '/admin-login/'})
            else:
                return JsonResponse({'status': 'error', 'message': 'CPF válido, mas o usuário não é um administrador.'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'CPF não encontrado.'})
    
    return JsonResponse({'status': 'error', 'message': 'Método de requisição inválido.'})
# *********************************************************************************************************************

def admin_login_view(request):
    if request.method == 'POST':
        cpf = request.POST.get('username')  # Assuming CPF is entered in 'username' field
        password = request.POST.get('password')

        # Authenticate user by CPF and password
        user = authenticate(request, username=cpf, password=password)

        if user is not None:
            # Check if the authenticated user is a superuser
            if user.is_superuser:
                login(request, user)
                # Redirect to the admin dashboard if the user is a superuser
                return redirect('regimento_list')
            else:
                messages.error(request, 'CPF válido, mas você não é um administrador.')
        else:
            messages.error(request, 'CPF ou senha inválidos.')

    # Render the admin login template for GET requests or if authentication fails
    return render(request, 'registration/admin_login.html')
# *********************************************************************************************************************

def adm_site_pedagogico(request):
    return render(request, 'setor_pedagogico/adm_site_pedagogico.html')
# *********************************************************************************************************************

def upload_arquivo(request):
    if request.method == 'POST' and request.FILES.get('arquivo'):
        arquivo_csv = request.FILES['arquivo']
        
        try:
            # Ler o arquivo CSV usando Pandas
            df = pd.read_csv(arquivo_csv)

            # Verifica se o dataframe foi lido corretamente
            if df.empty:
                messages.error(request, "O arquivo está vazio ou não pôde ser lido.")
                return redirect('admin_dashboard')

            print(f"DataFrame lido com {len(df)} linhas.")
            
            registros_salvos = 0
            registros_pulados = 0

            # Iterar sobre as linhas do dataframe e salvar no banco de dados
            for index, row in df.iterrows():
                print(f"Processando linha {index + 1}: {row.to_dict()}")

                # Verifica se o CPF já existe no banco
                if Funcionario.objects.filter(cpf=row['CPF']).exists():
                    print(f"CPF {row['CPF']} já existe. Pulando registro.")
                    registros_pulados += 1
                    continue

                # Criar o novo funcionário
                funcionario = Funcionario(
                    nome_completo=row['NOME COMPLETO'],
                    rg=row['RG'],
                    cpf=row['CPF'],
                    telefone=row['TELEFONE'],
                    email=row['E-MAIL'],
                    cargo=row['CARGO'],
                    lotacao=row['LOTAÇÃO'],
                )

                # Salvando no banco
                funcionario.save()
                registros_salvos += 1
                print(f"Funcionario {funcionario.nome_completo} salvo com sucesso.")

            messages.success(request, f'Arquivo enviado com sucesso! {registros_salvos} registros salvos, {registros_pulados} registros pulados.')
        except Exception as e:
            print(f"Erro ao processar o arquivo: {str(e)}")
            messages.error(request, f'Ocorreu um erro ao processar o arquivo: {e}')

        return redirect('admin_dashboard')

    return render(request, 'admin_dashboard.html')
# *********************************************************************************************************************

def cadastro_usuario(request):
    if request.method == 'POST':
        # Coletando os dados do formulário
        nome_completo = request.POST.get('nome_completo')
        cpf = request.POST.get('cpf')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')
        data_nascimento = request.POST.get('data_nascimento')

        errors = {}

        # Tratamento para CPF duplicado
        if Usuario.objects.filter(cpf=cpf).exists():
            errors['cpf_error'] = f"Este CPF ({cpf}) já está cadastrado."

        # Tratamento para email duplicado
        if Usuario.objects.filter(email=email).exists():
            errors['email_error'] = f"Este email ({email}) já está cadastrado."

        # Tratamento para senhas que não coincidem
        if senha != confirmar_senha:
            errors['password_error'] = "As senhas não coincidem."

        # Se houver erros, retorna a página de erro com todos os detalhes
        if errors:
            return render(request, 'error_page.html', errors)

        # Coletando outros campos para Inscricao
        responsavel_legal = request.POST.get('nome_responsavel')  # Corrigido para corresponder ao nome do campo no HTML
        tipo_responsavel = request.POST.get('tipo_responsavel')  # Corrigido para corresponder ao nome do campo no HTML
        cpf_responsavel = request.POST.get('cpf_responsavel')
        rg_responsavel = request.POST.get('rg_responsavel')
        telefone = request.POST.get('telefone')
        telefone_secundario = request.POST.get('telefone_2')
        endereco = request.POST.get('endereco')
        bairro_id = request.POST.get('bairro')  # Assuming you get 'bairro' ID from a form
        bairro_instance = Bairro.objects.get(id=bairro_id)  # Fetch the Bairro instance by ID
        cidade = request.POST.get('cidade')
        ponto_referencia = request.POST.get('ponto_referencia')
        possui_necessidade_especial = request.POST.get('possui_necessidade_especial')
        tipo_necessidade_especial = request.POST.get('necessidade_especial_detalhe')
        turno_disponivel = request.POST.get('turno_disponivel')
        etapa_pretendida = request.POST.get('etapa_pretendida')
        prova_todas_disciplinas = request.POST.get('prova_todas_disciplinas')
        fez_exame_supletivo = request.POST.get('fez_exame_supletivo')
        # Fixing the variable names to match the database columns
        local_exame = request.POST.get('local_prova')  # This should match the DB field 'local_exame'
        escola = request.POST.get('escola_2024')  # This should match the DB field 'escola'

        # Verifying passwords
        if senha != confirmar_senha:
            messages.error(request, "As senhas não coincidem!")
            return render(request, 'cadastro_usuario.html')

        # Check if CPF already exists
        if Usuario.objects.filter(cpf=cpf).exists():
            messages.error(request, "Este CPF já está cadastrado.")
            return render(request, 'cadastro_usuario.html')

        try:
            # Create user with encrypted password
            usuario = Usuario.objects.create_user(
                username=email,
                nome_completo=nome_completo,
                cpf=cpf,
                email=email,
                password=senha,
                data_nascimento=data_nascimento,
            )

            # Create the corresponding Inscricao and store it in a variable
            inscricao = Inscricao.objects.create(
                candidato=usuario,
                responsavel_legal=responsavel_legal,
                tipo_responsavel=tipo_responsavel,
                cpf_responsavel=cpf_responsavel,
                rg_responsavel=rg_responsavel,
                telefone=telefone,
                telefone_secundario=telefone_secundario,
                endereco=endereco,
                bairro=bairro_instance,  # Assign the Bairro instance
                cidade=cidade,
                ponto_referencia=ponto_referencia,
                necessidade_especial=(possui_necessidade_especial == 'Sim'),
                tipo_necessidade_especial=tipo_necessidade_especial,
                turno_disponivel=turno_disponivel,
                etapa_pretendida=etapa_pretendida,
                prova_todas_disciplinas=prova_todas_disciplinas,
                exame_supletivo=fez_exame_supletivo,
                local_exame=local_exame,  # Now this matches the database column
                escola=escola,  # Now this matches the database column
            )

            # Handle disciplines based on "prova_todas_disciplinas"
            if prova_todas_disciplinas == 'Sim':
                todas_disciplinas = Disciplina.objects.filter(nome__in=[
                    'Matemática', 'Ciências', 'Arte', 'Educação Física',
                    'História', 'Geografia', 'Língua Portuguesa', 'Inglês'
                ])
                inscricao.disciplinas.set(todas_disciplinas)
            else:
                # Adiciona apenas as disciplinas selecionadas pelo usuário
                disciplinas_selecionadas = request.POST.getlist('disciplinas')
                inscricao.disciplinas.set(disciplinas_selecionadas)

            # Log the user in and redirect to the candidate area
            login(request, usuario)
            return redirect('area_do_candidato')

        except IntegrityError as e:
            # Tratamento para outros erros do banco de dados
            errors['db_error'] = "Erro no banco de dados: " + str(e)
            return render(request, 'error_page.html', errors)

        except ValidationError as e:
            # Tratamento para outros erros de validação
            errors['validation_error'] = "Erro de validação: " + str(e)
            return render(request, 'error_page.html', errors)

    # Render the registration page if not a POST request
    return render(request, 'cadastro_usuario.html')

#**********************************************************************************************************

def home(request):
    return render(request, 'home.html')  # Substitua 'home.html' pelo caminho correto do seu template.
#**********************************************************************************************************

def eja_cadastro(request):
    return render(request, 'eja_cadastro.html')  # Substitua pelo caminho correto do seu template.
#**********************************************************************************************************

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'  # Substitua pelo caminho correto do template
    redirect_authenticated_user = True
#**********************************************************************************************************

def logout_confirm(request):
    return render(request, 'logout_confirm.html')

def area_do_candidato(request):
    return render(request, 'area_do_candidato.html')

def get_diagnose_data(request):
    turmas = [
        '401', '403', '404', '406', '408', '409', '410', '413', '414', '415', '417',
        '421', '423', '426', '428', '429', '430', '431', '432', '433', '434', '435',
        '436', '437', '438', '439', '441', '442', '447', '451', '471'
    ]
    
    items = []
    for item in DiagnoseInicProfPort.objects.all():
        responses = {f"professor_{turma}": getattr(item, f"professor_{turma}", "N") for turma in turmas}
        items.append({
            "numero": item.item,
            "habilidade": item.habilidade,
            "descricao_habilidade": item.descricao_habilidade,
            "respostas": responses
        })
    
    return JsonResponse({"items": items, "turmas": turmas})

def get_diagnose_data_inic_alunos_matematica(request):
    # Lista de séries que serão usadas para os alunos
    series = ['3º', '4º', '5º', '6º']

    # Lista para armazenar os itens e suas respostas associadas
    items = []

    # Recupera todos os itens da tabela DiagnoseAlunoMatematica
    dados_db = DiagnoseAlunoMatematica.objects.all()

    # Itera sobre cada item recuperado do banco de dados
    for item in dados_db:
        # Adiciona os dados de cada item (série, habilidade, acertos e erros) na lista
        items.append({
            "serie": item.serie,  # Série do aluno
            "habilidade": item.habilidade,  # Habilidade correspondente
            "acerto": item.acerto,  # Total de acertos
            "erro": item.erro  # Total de erros
        })

    # Retorna os dados em formato JSON
    return JsonResponse({"items": items, "series": series})

def aluno_matematica_view(request):
    # Inicialização das variáveis
    series = ['3º', '4º', '5º', '6º']
    serie_3_corretas = serie_4_corretas = serie_5_corretas = serie_6_corretas = 0
    serie_3_erradas = serie_4_erradas = serie_5_erradas = serie_6_erradas = 0
    serie_3_total = serie_4_total = serie_5_total = serie_6_total = 0
    total_corretas = total_erradas = total_respostas = 0
    itens = []

    # Buscar dados do banco
    itens_db = DiagnoseAlunoMatematica.objects.all()

    for item in itens_db:
        try:
            # Convertendo para float se for uma string antes de arredondar
            acerto = round(float(item.acerto), 2)  # Arredondamento para duas casas decimais
            erro = round(float(item.erro), 2)  # Arredondamento para duas casas decimais
        except ValueError:
            # Se não for possível converter, ignorar a linha ou lidar com o erro conforme necessário
            continue

        total_corretas += acerto
        total_erradas += erro
        total_respostas += 1

        # Acumula os dados por série
        if item.serie == '3º':
            serie_3_corretas += acerto
            serie_3_erradas += erro
            serie_3_total += 1
        elif item.serie == '4º':
            serie_4_corretas += acerto
            serie_4_erradas += erro
            serie_4_total += 1
        elif item.serie == '5º':
            serie_5_corretas += acerto
            serie_5_erradas += erro
            serie_5_total += 1
        elif item.serie == '6º':
            serie_6_corretas += acerto
            serie_6_erradas += erro
            serie_6_total += 1

        itens.append({
            'serie': item.serie,
            'habilidade': item.habilidade,
            'acerto': acerto,
            'erro': erro
        })

    # Cálculo dos percentuais por série
    serie_3_percentual_acertos = round((serie_3_corretas / serie_3_total) * 100, 2) if serie_3_total > 0 else 0
    serie_3_percentual_erros = round((serie_3_erradas / serie_3_total) * 100, 2) if serie_3_total > 0 else 0
    serie_4_percentual_acertos = round((serie_4_corretas / serie_4_total) * 100, 2) if serie_4_total > 0 else 0
    serie_4_percentual_erros = round((serie_4_erradas / serie_4_total) * 100, 2) if serie_4_total > 0 else 0
    serie_5_percentual_acertos = round((serie_5_corretas / serie_5_total) * 100, 2) if serie_5_total > 0 else 0
    serie_5_percentual_erros = round((serie_5_erradas / serie_5_total) * 100, 2) if serie_5_total > 0 else 0
    serie_6_percentual_acertos = round((serie_6_corretas / serie_6_total) * 100, 2) if serie_6_total > 0 else 0
    serie_6_percentual_erros = round((serie_6_erradas / serie_6_total) * 100, 2) if serie_6_total > 0 else 0

    percentual_acertos = round((total_corretas / total_respostas) * 100, 2) if total_respostas > 0 else 0
    percentual_erros = round((total_erradas / total_respostas) * 100, 2) if total_respostas > 0 else 0

    uploaded_file_url = None

    if request.method == 'POST':
        if 'upload_planilha' in request.POST and request.FILES.get('planilha'):
            planilha = request.FILES['planilha']

            fs = FileSystemStorage()
            filename = fs.save(planilha.name, planilha)
            uploaded_file_url = fs.url(filename)

            try:
                # Carrega a planilha com pandas
                df = pd.read_excel(fs.path(filename))

                # Limpa a tabela antes de adicionar novos dados
                DiagnoseAlunoMatematica.objects.all().delete()

                # Itera sobre as linhas da planilha e processa cada uma
                for index, row in df.iterrows():
                    try:
                        serie = row['AI']
                        habilidade = row['Habilidade']
                        acerto = float(str(row['Acerto']).replace(",", "."))
                        erro = float(str(row['Erro']).replace(",", "."))

                        # Validação dos dados antes de salvar
                        if not (0 <= acerto <= 1 and 0 <= erro <= 1):
                            raise ValueError(f"Valores inválidos de acerto/erro na linha {index + 1}")

                        DiagnoseAlunoMatematica.objects.create(
                            serie=serie,
                            habilidade=habilidade,
                            acerto=acerto,
                            erro=erro
                        )
                    except Exception as e:
                        messages.error(request, f"Erro ao processar a linha {index + 1}: {e}")

                messages.success(request, "Planilha carregada e processada com sucesso!")
            except Exception as e:
                messages.error(request, f"Erro ao processar o arquivo: {e}")

            return redirect('aluno_matematica_view')

    return render(request, 'lingua_matematica_aluno.html', {
        'series': series,
        'itens': itens,
        'total_corretas': total_corretas,
        'total_erradas': total_erradas,
        'percentual_acertos': percentual_acertos,
        'percentual_erros': percentual_erros,
        'serie_3_corretas': serie_3_corretas,
        'serie_3_erradas': serie_3_erradas,
        'serie_3_percentual_acertos': serie_3_percentual_acertos,
        'serie_3_percentual_erros': serie_3_percentual_erros,
        'serie_4_corretas': serie_4_corretas,
        'serie_4_erradas': serie_4_erradas,
        'serie_4_percentual_acertos': serie_4_percentual_acertos,
        'serie_4_percentual_erros': serie_4_percentual_erros,
        'serie_5_corretas': serie_5_corretas,
        'serie_5_erradas': serie_5_erradas,
        'serie_5_percentual_acertos': serie_5_percentual_acertos,
        'serie_5_percentual_erros': serie_5_percentual_erros,
        'serie_6_corretas': serie_6_corretas,
        'serie_6_erradas': serie_6_erradas,
        'serie_6_percentual_acertos': serie_6_percentual_acertos,
        'serie_6_percentual_erros': serie_6_percentual_erros,
        'uploaded_file_url': uploaded_file_url
    })


################################################################################################################

def upload_excel_aluno_matematica(request):
    if request.method == "POST" and request.FILES.get("planilha"):
        planilha = request.FILES['planilha']
        fs = FileSystemStorage()
        filename = fs.save(planilha.name, planilha)
        file_path = fs.path(filename)

        # Mapeamento das séries em texto para números
        series_mapping = {
            '3º ano': 3,
            '4º ano': 4,
            '5º ano': 5,
            '6º ano': 6,
            # Adicione mais séries conforme necessário
        }

        try:
            # Verificar se o tipo de arquivo é Excel
            mime_type, _ = mimetypes.guess_type(file_path)
            if mime_type in ['application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']:
                df = pd.read_excel(file_path, engine='openpyxl')

                # Limpar dados existentes
                DiagnoseAlunoMatematica.objects.all().delete()

                # Processar cada linha da planilha
                for index, row in df.iterrows():
                    try:
                        # Ajuste os nomes das colunas com os corretos
                        serie_texto = row.get('AI')  # Supondo que a coluna 'AI' contém a série em texto
                        habilidade = row.get('Habilidade')
                        acerto = float(str(row.get('Acerto')).replace(",", ".")) if not pd.isna(row.get('Acerto')) else 0
                        erro = float(str(row.get('Erro')).replace(",", ".")) if not pd.isna(row.get('Erro')) else 0

                        # Converter a série de texto para número
                        serie = series_mapping.get(serie_texto)
                        if serie is None:
                            raise ValueError(f"Série inválida '{serie_texto}' na linha {index + 1}")

                        # Validação dos valores de acerto/erro
                        if not (0 <= acerto <= 1 and 0 <= erro <= 1):
                            raise ValueError(f"Valores inválidos de acerto/erro na linha {index + 1}")

                        # Salvar no banco de dados
                        DiagnoseAlunoMatematica.objects.create(
                            serie=serie,  # Salvar a série convertida
                            habilidade=habilidade,
                            acerto=acerto,
                            erro=erro
                        )
                    except Exception as e:
                        messages.error(request, f"Erro ao processar a linha {index + 1}: {e}")
                        continue

                messages.success(request, "Planilha carregada e processada com sucesso!")
            else:
                raise ValueError("Formato de arquivo inválido.")

        except Exception as e:
            messages.error(request, f"Erro ao processar o arquivo: {e}")

        return redirect('aluno_matematica_view')

    return render(request, 'upload_page_matematica.html')

################################################################################################################

def get_diagnose_data_inic_alunos_port(request):
    # Lista de séries que serão usadas para os alunos
    series = ['3º', '4º', '5º', '6º']

    # Lista para armazenar os itens e suas respostas associadas
    items = []

    # Recupera todos os itens da tabela DiagnoseAlunoPortugues (ou o modelo equivalente)
    dados_db = DiagnoseAlunoPortugues.objects.all()

    # Itera sobre cada item recuperado do banco de dados
    for item in dados_db:
        # Adiciona os dados de cada item (série, habilidade, acertos e erros) na lista
        items.append({
            "serie": item.serie if item.serie in series else "N/A",  # Verifica se a série está na lista
            "habilidade": item.habilidade if item.habilidade else "N/A",  # Verifica se a habilidade está presente
            "acerto": round(float(item.acerto or 0), 2),  # Formata os acertos e trata valores nulos
            "erro": round(float(item.erro or 0), 2),  # Formata os erros e trata valores nulos
        })

    # Retorna os dados em formato JSON
    return JsonResponse({"items": items, "series": series})
################################################################################################################

def habilidades_portugues_view(request):
    habilidades = HabilidadePortugues.objects.all()  # Buscando todos os dados
    return render(request, 'habilidades_portugues.html', {'habilidades': habilidades})
################################################################################################################

def habilidades_matematica_view(request):
    # Lógica para processar e renderizar as habilidades de Matemática
    habilidades = HabilidadeMatematica.objects.all()  # Buscando todos os dados
    return render(request, 'habilidades_matematica.html', {'habilidades': habilidades})
################################################################################################################

def habilidades_portugues_view(request):
    return render(request, 'diagnosis/eja/habilidades_portugues.html')
################################################################################################################

# View para habilidades de Matemática
def habilidades_matematica_view(request):
    # Dados simulados (você pode buscar isso do banco de dados)
    habilidades = [
        {'serie': '5º Ano', 'topico': 'Números e Operações', 'habilidade': 'H1', 'descricao': 'Resolver problemas envolvendo adição e subtração.'},
        {'serie': '5º Ano', 'topico': 'Geometria', 'habilidade': 'H2', 'descricao': 'Identificar formas geométricas em objetos do cotidiano.'},
        {'serie': '9º Ano', 'topico': 'Álgebra', 'habilidade': 'H3', 'descricao': 'Resolver equações de primeiro grau com uma incógnita.'},
        {'serie': '9º Ano', 'topico': 'Estatística', 'habilidade': 'H4', 'descricao': 'Interpretar gráficos e tabelas.'},
    ]
    return render(request, 'diagnosis/eja/habilidades_matematica.html', {'habilidades': habilidades})
################################################################################################################

# View para a página de Pesquisa
def habilidades_pesquisa_view(request):
    query = request.GET.get('habilidade', '')

    # Simulação de dados (substitua por consulta ao banco de dados)
    todas_habilidades = [
        {'serie': '5º Ano', 'nome': 'Leitura e Interpretação', 'descricao': 'Desenvolver a habilidade de interpretação textual.'},
        {'serie': '9º Ano', 'nome': 'Álgebra Básica', 'descricao': 'Resolver equações lineares simples.'},
    ]

    habilidades = [h for h in todas_habilidades if query.lower() in h['nome'].lower()] if query else todas_habilidades

    return render(request, 'diagnosis/eja/habilidades_pesquisa.html', {'habilidades': habilidades})

def lingua_portuguesa_alunos_iniciais(request):
    return render(request, 'diagnoses/lingua_portuguesa_alunos_iniciais.html')
###***********************************************************************************************************************

def lingua_portuguesa_professores_iniciais(request):
    return render(request, 'diagnoses/lingua_portuguesa_prof.html')
###***********************************************************************************************************************

def lingua_matematica_alunos_iniciais(request):
    return render(request, 'diagnoses/lingua_matematica_alunos_iniciais.html')
###***********************************************************************************************************************

def lingua_matematica_professores_iniciais(request):
    return render(request, 'diagnoses/lingua_matematica_professores_iniciais.html')
###***********************************************************************************************************************

def lingua_portuguesa_alunos_finais(request):
    return render(request, 'diagnoses/lingua_portuguesa_alunos_finais.html')
###***********************************************************************************************************************

def lingua_portuguesa_professores_finais(request):
    return render(request, 'diagnoses/lingua_portuguesa_prof.html')  # Alterado para o template correto
###***********************************************************************************************************************

def lingua_matematica_alunos_finais(request):
    return render(request, 'diagnoses/lingua_matematica_alunos_finais.html')
###***********************************************************************************************************************

def lingua_matematica_professores_finais(request):
    return render(request, 'diagnoses/lingua_matematica_professores_finais.html')
###***********************************************************************************************************************

def lingua_portuguesa_prof_view(request):
    # Definindo as turmas
    turmas = ['401', '403', '404', '406', '408', '409', '410', '413', '414', '415', '417', '421', '423', '426', 
              '428', '429', '430', '431', '432', '433', '434', '435', '436', '437', '438', '439', '441', '442', 
              '447', '451', '471']

    # Definindo os itens e habilidades
    itens = [
        {'numero': 1, 'habilidade': 'D12', 'respostas': {'401': 1, '403': 1, '404': 1, '406': 1}},
        {'numero': 2, 'habilidade': 'D03', 'respostas': {'401': 0, '403': 1, '404': 1, '406': 1}},
        {'numero': 3, 'habilidade': 'D09', 'respostas': {'401': 0, '403': 0, '404': 1, '406': 0}},
        {'numero': 4, 'habilidade': 'D01', 'respostas': {'401': 1, '403': 1, '404': 1, '406': 1}},
        {'numero': 5, 'habilidade': 'D09', 'respostas': {'401': 1, '403': 1, '404': 1, '406': 1}},
        {'numero': 6, 'habilidade': 'D06', 'respostas': {'401': 1, '403': 0, '404': 1, '406': 1}},
        {'numero': 7, 'habilidade': 'D15', 'respostas': {'401': 1, '403': 1, '404': 0, '406': 1}},
        {'numero': 8, 'habilidade': 'D02', 'respostas': {'401': 1, '403': 1, '404': 0, '406': 1}},
        {'numero': 9, 'habilidade': 'D03', 'respostas': {'401': 1, '403': 1, '404': 1, '406': 0}},
        {'numero': 10, 'habilidade': 'D05', 'respostas': {'401': 1, '403': 1, '404': 1, '406': 1}},
        {'numero': 11, 'habilidade': 'D04', 'respostas': {'401': 1, '403': 1, '404': 1, '406': 1}},
        {'numero': 12, 'habilidade': 'D12', 'respostas': {'401': 1, '403': 1, '404': 1, '406': 1}},
        {'numero': 13, 'habilidade': 'D05', 'respostas': {'401': 1, '403': 1, '404': 0, '406': 0}},
        {'numero': 14, 'habilidade': 'D13', 'respostas': {'401': 1, '403': 1, '404': 1, '406': 1}},
        {'numero': 15, 'habilidade': 'D10', 'respostas': {'401': 1, '403': 1, '404': 1, '406': 1}},
        {'numero': 16, 'habilidade': 'D13', 'respostas': {'401': 1, '403': 1, '404': 1, '406': 1}},
        {'numero': 17, 'habilidade': 'D07', 'respostas': {'401': 0, '403': 1, '404': 1, '406': 0}},
        {'numero': 18, 'habilidade': 'D14', 'respostas': {'401': 1, '403': 1, '404': 1, '406': 1}},
        {'numero': 19, 'habilidade': 'D06', 'respostas': {'401': 1, '403': 1, '404': 1, '406': 1}},
        {'numero': 20, 'habilidade': 'D07', 'respostas': {'401': 0, '403': 1, '404': 1, '406': 0}},
        {'numero': 21, 'habilidade': 'D14', 'respostas': {'401': 1, '403': 1, '404': 1, '406': 1}},
        {'numero': 22, 'habilidade': 'D10', 'respostas': {'401': 1, '403': 1, '404': 1, '406': 1}},
        {'numero': 23, 'habilidade': 'D13', 'respostas': {'401': 1, '403': 1, '404': 1, '406': 1}},
        {'numero': 24, 'habilidade': 'D15', 'respostas': {'401': 0, '403': 1, '404': 1, '406': 1}},
        {'numero': 25, 'habilidade': 'D04', 'respostas': {'401': 1, '403': 1, '404': 1, '406': 1}},
        {'numero': 26, 'habilidade': 'D02', 'respostas': {'401': 1, '403': 1, '404': 1, '406': 1}},
    ]

    itens = []
    total_corretas = 0
    total_erradas = 0

    # Carregando os dados salvos no banco de dados
    itens_db = DiagnoseInicProfPort.objects.all()

    for item in itens_db:
        respostas = {}
        for turma in turmas:
            resposta = getattr(item, f'professor_{turma}', 'N')
            respostas[turma] = resposta
            if resposta == 'S':
                total_corretas += 1
            else:
                total_erradas += 1
        itens.append({'numero': item.item, 'habilidade': item.habilidade, 'respostas': respostas})

    uploaded_file_url = None

    if request.method == 'POST':
        if 'upload_planilha' in request.POST and request.FILES.get('planilha'):
            planilha = request.FILES['planilha']
            fs = FileSystemStorage()
            filename = fs.save(planilha.name, planilha)
            uploaded_file_url = fs.url(filename)
            
            # Processar a planilha usando pandas
            df = pd.read_excel(fs.path(filename))

            for index, row in df.iterrows():
                item_num = row['Item']
                habilidade = row['Habilidade']
                
                # Criar ou atualizar o registro no banco de dados
                diagnose, created = DiagnoseInicProfPort.objects.get_or_create(
                    item=item_num,
                    habilidade=habilidade
                )

                for turma in turmas:
                    resposta = row.get(str(turma), 0)
                    # Salva a resposta no banco de dados como 'S' ou 'N'
                    setattr(diagnose, f'professor_{turma}', 'S' if resposta == 1 else 'N')
                
                diagnose.save()

            # Redirecionar de volta para a página de exibição após o salvamento
            return redirect('lingua_portuguesa_prof_view')

        if 'salvar_respostas' in request.POST:
            for item in itens:
                diagnose = DiagnoseInicProfPort.objects.get(item=item['numero'])
                for turma in turmas:
                    nova_resposta = request.POST.get(f'respostas_{item["numero"]}_{turma}', 'N')
                    setattr(diagnose, f'professor_{turma}', nova_resposta)
                diagnose.save()

            # Redirecionar após salvar
            return redirect('lingua_portuguesa_prof_view')

    return render(request, 'diagnoses/lingua_portuguesa_prof.html', {
        'turmas': turmas,
        'itens': itens,
        'total_corretas': total_corretas,
        'total_erradas': total_erradas,
        'uploaded_file_url': uploaded_file_url
    })
###***********************************************************************************************************************

def lingua_matematica_professores_finais(request):
    return render(request, 'diagnoses/lingua_matematica_professores_finais.html')
###***********************************************************************************************************************

def support(request):
    return render(request, 'webapp/support.html')
###***********************************************************************************************************************

def configuracoes_view(request):
    return render(request, 'webapp/configuracoes.html')
###***********************************************************************************************************************

def alterar_senha_view(request):
    if request.method == 'POST':
        # Lógica de alteração de senha
        pass  # Coloque aqui a lógica para alterar a senha
    return render(request, 'webapp/alterar_senha.html')
###***********************************************************************************************************************

def atualizar_preferencias_view(request):
    if request.method == 'POST':
        # Lógica para atualizar as preferências de notificação do usuário
        # Exemplo: request.user.profile.email_notifications = request.POST.get('email_notifications')
        pass  # Coloque aqui a lógica para salvar as preferências de notificação
    return redirect('configuracoes')  # Redireciona de volta para a página de configurações após salvar
###***********************************************************************************************************************

@login_required
def upload_files(request):
    if request.method == 'POST':
        csv_file = request.FILES['file']

        # Detect encoding
        raw_data = csv_file.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        csv_file.seek(0)  # Reset file pointer

        try:
            # Read CSV file with detected encoding and ensure the first row is treated as header
            df = pd.read_csv(csv_file, encoding=encoding, delimiter=';', header=0, on_bad_lines='skip')

            expected_headers = [
                'numero_matricula', 'nome_completo', 'escola', 'data_nascimento', 'sexo', 'turno',
                'telefone', 'nivel_escolaridade', 'endereco', 'bairro', 'cep', 'codigo_rota',
                'email_responsavel', 'cpf_responsavel', 'nome_responsavel', 'parentesco',
                'telefone_responsavel', 'responsavel_legal'
            ]

            # Verify that the CSV file contains the expected headers
            csv_headers = list(df.columns)
            if csv_headers != expected_headers:
                missing_headers = set(expected_headers) - set(csv_headers)
                extra_headers = set(csv_headers) - set(expected_headers)
                error_message = f"Os cabeçalhos dos arquivos CSV não correspondem aos cabeçalhos esperados.\n"
                if missing_headers:
                    error_message += f"Cabeçalhos ausentes: {', '.join(missing_headers)}\n"
                if extra_headers:
                    error_message += f"Cabeçalhos extras: {', '.join(extra_headers)}"
                raise ValueError(error_message)

            # Convert date format
            df['data_nascimento'] = pd.to_datetime(df['data_nascimento'], format='%d/%m/%Y', errors='coerce')

            students_inserted = 0
            students_existing = []

            for _, row in df.iterrows():
                if pd.isna(row['data_nascimento']):
                    raise ValueError(f"Formato de data inválido para linha  : {row.to_dict()}")

                numero_matricula = row['numero_matricula']
                if not Student.objects.filter(numero_matricula=numero_matricula).exists():
                    Student.objects.create(
                        numero_matricula=numero_matricula,
                        nome_completo=row['nome_completo'],
                        escola=row['escola'],
                        data_nascimento=row['data_nascimento'].strftime('%Y-%m-%d'),
                        sexo=row['sexo'],
                        turno=row['turno'],
                        telefone=row['telefone'],
                        nivel_escolaridade=row['nivel_escolaridade'],
                        endereco=row['endereco'],
                        bairro=row['bairro'],
                        cep=row['cep'],
                        codigo_rota=row['codigo_rota'],
                        email_responsavel=row['email_responsavel'],
                        cpf_responsavel=row['cpf_responsavel'],
                        nome_responsavel=row['nome_responsavel'],
                        parentesco=row['parentesco'],
                        telefone_responsavel=row['telefone_responsavel'],
                        responsavel_legal=row['responsavel_legal'],
                    )
                    students_inserted += 1
                else:
                    students_existing.append(row)

            # Generate file with existing students
            if students_existing:
                output = io.StringIO()
                writer = csv.DictWriter(output, fieldnames=expected_headers)
                writer.writeheader()
                writer.writerows(students_existing)
                csv_content = output.getvalue()
                output.close()

                file_name = 'students_existing.csv'
                file_path = default_storage.save(file_name, ContentFile(csv_content))

                students_existing_url = default_storage.url(file_path)
            else:
                students_existing_url = None

            messages.success(request, f'{students_inserted} alunos foram inseridos com sucesso.')
            if students_existing:
                messages.warning(request, f'{len(students_existing)} alunos já existiam no banco de dados.')

            return render(request, 'webapp/upload_files.html', {'students_existing_url': students_existing_url})

        except Exception as e:
            messages.error(request, f'Erro ao processar arquivo CSV: {str(e)}')

    return render(request, 'webapp/upload_files.html')
###***********************************************************************************************************************
def dashboard_transporte(request):
    total_alunos = IndicadoresTransporte.objects.count()
    total_escolas = IndicadoresTransporte.objects.values('escola').distinct().count()
    alunos_ensino_medio = IndicadoresTransporte.objects.filter(
        nivel_escolaridade__icontains='Ensino Médio'
    ).count()
    alunos_ensino_fundamental = IndicadoresTransporte.objects.filter(
        nivel_escolaridade__icontains='Ensino Fundamental'
    ).count()

    alunos_por_escola = (
        IndicadoresTransporte.objects
        .values('escola')
        .annotate(total=Count('id'))
        .order_by('-total')
    )
    escolas = [item['escola'] for item in alunos_por_escola]
    alunos = [item['total'] for item in alunos_por_escola]

    context = {
        'total_alunos': total_alunos,
        'total_escolas': total_escolas,
        'alunos_ensino_medio': alunos_ensino_medio,
        'alunos_ensino_fundamental': alunos_ensino_fundamental,
        'escolas': escolas,
        'alunos': alunos,
    }
    return render(request, 'indicadores/transporte.html', context)

###***********************************************************************************************************************

def transporte_dashboard(request):
    total_alunos = IndicadoresTransporte.objects.count()
    total_escolas = IndicadoresTransporte.objects.values('escola').distinct().count()
    alunos_ensino_medio = IndicadoresTransporte.objects.filter(nivel_escolaridade__icontains='Ensino Médio').count()
    alunos_ensino_fundamental = IndicadoresTransporte.objects.filter(nivel_escolaridade__icontains='Ensino Fundamental').count()

    alunos_por_escola = IndicadoresTransporte.objects.values('escola').annotate(total=Count('id')).order_by('-total')

    context = {
        'total_alunos': total_alunos,
        'total_escolas': total_escolas,
        'alunos_ensino_medio': alunos_ensino_medio,
        'alunos_ensino_fundamental': alunos_ensino_fundamental,
        'alunos_por_escola': list(alunos_por_escola),
    }
    return render(request, 'indicadores/transporte.html', context)
###***********************************************************************************************************************

def transporte_dados_api(request):
    alunos_por_escola = IndicadoresTransporte.objects.values('escola').annotate(total=Count('id')).order_by('-total')
    data = {
        'total_alunos': IndicadoresTransporte.objects.count(),
        'total_escolas': IndicadoresTransporte.objects.values('escola').distinct().count(),
        'alunos_ensino_medio': IndicadoresTransporte.objects.filter(nivel_escolaridade__icontains='Ensino Médio').count(),
        'alunos_ensino_fundamental': IndicadoresTransporte.objects.filter(nivel_escolaridade__icontains='Ensino Fundamental').count(),
        'alunos_por_escola': list(alunos_por_escola),
    }
    return JsonResponse(data)
###***********************************************************************************************************************

def indicadores_canaa(request):
    total_escolas = IndicadoresTransporte.objects.values('escola').distinct().count()
    taxa_alfabetizacao = calcular_taxa_alfabetizacao()
    # total_creches = Creches.objects.filter(ativa=True).count()
    # alunos_creches = Alunos.objects.filter(nivel_escolaridade__icontains='Creche').count()
    media_idade = calcular_media_idade()
    investimento_educacao = calcular_investimento_educacao(2024)
    escolas_com_transporte = IndicadoresTransporte.objects.values('escola').distinct().count()
    taxa_inclusao_digital = calcular_inclusao_digital()

    context = {
        'taxa_alfabetizacao': taxa_alfabetizacao,
        # 'total_creches': total_creches,
        # 'alunos_creches': alunos_creches,
        'media_idade': media_idade,
        'investimento_educacao': investimento_educacao,
        'escolas_com_transporte': escolas_com_transporte,
        'total_escolas': total_escolas,
        'taxa_inclusao_digital': taxa_inclusao_digital,
    }
    return render(request, 'indicadores/canaa.html', context)
###***********************************************************************************************************************

def calcular_taxa_alfabetizacao():
    # Simula o total de crianças alfabetizadas e o total de crianças na faixa etária
    total_criancas = IndicadoresTransporte.objects.filter(data_nascimento__year__gte=2010).count()
    alfabetizadas = total_criancas * 0.95  # Exemplo de taxa fixa de 95%
    return round((alfabetizadas / total_criancas) * 100, 2) if total_criancas > 0 else 0
###***********************************************************************************************************************

def calcular_media_idade():
    hoje = date.today()
    alunos = IndicadoresTransporte.objects.all()
    total_idades = sum([hoje.year - aluno.data_nascimento.year for aluno in alunos])
    total_alunos = alunos.count()
    return round(total_idades / total_alunos, 1) if total_alunos > 0 else 0
###***********************************************************************************************************************

def calcular_investimento_educacao(ano):
    # Simula um investimento baseado em dados fictícios
    investimento = {
        2023: 12000000,
        2024: 15000000,
    }
    return investimento.get(ano, 0)
###***********************************************************************************************************************

def calcular_inclusao_digital():
    escolas_totais = IndicadoresTransporte.objects.values('escola').distinct().count()
    escolas_com_internet = int(escolas_totais * 0.85)  # Exemplo: 85% possuem internet
    return round((escolas_com_internet / escolas_totais) * 100, 2) if escolas_totais > 0 else 0
###***********************************************************************************************************************

# class Creches(models.Model):
#     nome = models.CharField(max_length=255)
#     ativa = models.BooleanField(default=True)


# class Alunos(models.Model):
#     nome_completo = models.CharField(max_length=255)
#     data_nascimento = models.DateField()
#     nivel_escolaridade = models.CharField(max_length=100)
###***********************************************************************************************************************
def gestao_dados(request):
    # Filtragem
    escola_selecionada = request.GET.get('escola', '')
    bairro_selecionado = request.GET.get('bairro', '')
    turno_selecionado = request.GET.get('turno', '')
    sexo_selecionado = request.GET.get('sexo', '')

    # Obter dados únicos para os filtros
    escolas = IndicadoresTransporte.objects.values_list('escola', flat=True).distinct()
    bairros = IndicadoresTransporte.objects.values_list('bairro', flat=True).distinct()

    # Aplicar filtros na consulta
    alunos = IndicadoresTransporte.objects.all()
    if escola_selecionada:
        alunos = alunos.filter(escola=escola_selecionada)
    if bairro_selecionado:
        alunos = alunos.filter(bairro=bairro_selecionado)
    if turno_selecionado:
        alunos = alunos.filter(turno=turno_selecionado)
    if sexo_selecionado:
        alunos = alunos.filter(sexo=sexo_selecionado)

    # Contexto para o template
    context = {
        'alunos': alunos,
        'escolas': escolas,
        'bairros': bairros,
        'escola_selecionada': escola_selecionada,
        'bairro_selecionado': bairro_selecionado,
        'turno_selecionado': turno_selecionado,
        'sexo_selecionado': sexo_selecionado,
    }

    return render(request, 'gestao_dados.html', context)
###***********************************************************************************************************************

def planejamento(request):
    return render(request, 'seppec/planejamento.html')
###***********************************************************************************************************************

def execucao(request):
    return render(request, 'seppec/execucao.html')
###***********************************************************************************************************************

def controle(request):
    return render(request, 'seppec/controle.html')
###***********************************************************************************************************************

def comunicacao(request):
    return render(request, 'seppec/comunicacao.html')
###***********************************************************************************************************************

def quem_somos(request):
    return render(request, 'setor_pedagogico/quem_somos.html')
###***********************************************************************************************************************

def missao_visao(request):
    return render(request, 'setor_pedagogico/missao_visao.html')
###***********************************************************************************************************************

def equipe(request):
    return render(request, 'setor_pedagogico/equipe.html')
###***********************************************************************************************************************

def projetos_especiais(request):
    return render(request, 'setor_pedagogico/projetos_especiais.html')
###***********************************************************************************************************************

def contato_pedagogico(request):
    return render(request, 'setor_pedagogico/contato_pedagogico.html')
###***********************************************************************************************************************

def painel_administrativo(request):
    # Busca todos os registros da tabela
    artigos = RegimentoCadastro.objects.all()  
    return render(request, 'painel_administrativo.html', {'artigos': artigos})
###***********************************************************************************************************************

def admin_dashboard(request):
    # Contar apenas artigos cujo ID seja maior que um valor (exemplo: 10)
    total_artigos = SemedAppRegimentoCadastro.objects.filter(id__gt=10).count()
    
    # Filtrar artigos específicos (caso deseje enviar dados detalhados ao template)
    artigos = SemedAppRegimentoCadastro.objects.filter(id__gte=1).values(
        'id', 'titulo', 'capitulo', 'tipo_alteracao', 'nome_completo',
        'email', 'cpf', 'telefone', 'cargo', 'lotacao', 'data_submissao', 'status'
    )
    
    return render(request, 'adm_site_pedagogico.html', {
        'total_artigos': total_artigos,
        'artigos': list(artigos)  # Enviar artigos ao template (se necessário)
    })
###***********************************************************************************************************************

def get_articles_data(request):
    artigos = SemedAppRegimentoCadastro.objects.all().values(
        'id', 'titulo', 'capitulo', 'tipo_alteracao', 'nome_completo',
        'email', 'cpf', 'telefone', 'cargo', 'lotacao', 'data_submissao', 'status'
    )
    return JsonResponse({'data': list(artigos)})

###***********************************************************************************************************************

def site_pedagogico_view(request):
    # Renderiza a página do Site Pedagógico
    return render(request, 'site_pedagogico.html')
###***********************************************************************************************************************


# def index(request):
#     return render(request, 'banco_curriculos/index.html')
###***********************************************************************************************************************

def vagas(request):
    return render(request, 'banco_curriculos/vagas.html')
###***********************************************************************************************************************

def curriculos(request):
    return render(request, 'banco_curriculos/curriculos.html')
###***********************************************************************************************************************

from django.shortcuts import render, redirect
from semedapp.models import CadastroCandidato
from django.contrib.auth.hashers import check_password
from django.contrib import messages

def login_curriculo(request):
    if request.method == "POST":
        email = request.POST.get("email")
        senha = request.POST.get("password")

        try:
            # Busca o candidato pelo email
            candidato = CadastroCandidato.objects.get(email=email)

            # Verifica a senha
            if check_password(senha, candidato.senha):
                # Login bem-sucedido - cria a sessão do candidato
                request.session['candidato_id'] = candidato.id
                messages.success(request, "Login realizado com sucesso!")
                return redirect("area_candidato")  # Substitua pela URL da área do candidato
            else:
                # Senha incorreta
                messages.error(request, "E-mail ou senha inválidos.")
        except CadastroCandidato.DoesNotExist:
            # Candidato não encontrado
            messages.error(request, "E-mail ou senha inválidos.")

    return render(request, "banco_curriculos/login.html")


###***********************************************************************************************************************

def registrar(request):
    return render(request, 'banco_curriculos/registrar.html')
###***********************************************************************************************************************

def registrar_view(request):
    if request.method == "POST":
        # Lógica de registro
        pass
    return render(request, 'banco_curriculos/registrar.html')
###***********************************************************************************************************************

def login_curriculo_view(request):
    return render(request, 'banco_curriculos/login.html')
###***********************************************************************************************************************

# Página Home para banco de currículos
def banco_curriculos_home(request):
    return render(request, 'banco_curriculos/index.html')  # Template específico
###***********************************************************************************************************************

def upload_planilha_prof(request):#####PRIMEIRO
    if request.method == 'POST':
        form = UploadPlanilhaForm(request.POST, request.FILES)
        if form.is_valid():
            planilha = request.FILES['planilha']
            # Ler o arquivo CSV
            df = pd.read_csv(planilha)

            # Limpa os dados existentes para evitar duplicações
            HabilidadeProf.objects.all().delete()

            # Processar os dados da planilha
            for _, row in df.iterrows():
                HabilidadeProf.objects.create(
                    item=row['Item'],
                    habilidade=row['Habilidade'],
                    turma_401=row.get('401', 0),
                    turma_403=row.get('403', 0),
                    turma_404=row.get('404', 0),
                    turma_406=row.get('406', 0),
                    turma_408=row.get('408', 0),
                    turma_409=row.get('409', 0),
                    turma_410=row.get('410', 0),
                    turma_413=row.get('413', 0),
                    turma_414=row.get('414', 0),
                    turma_415=row.get('415', 0),
                    turma_417=row.get('417', 0),
                    turma_421=row.get('421', 0),
                    turma_423=row.get('423', 0),
                    turma_426=row.get('426', 0),
                    turma_428=row.get('428', 0),
                    turma_429=row.get('429', 0),
                    turma_430=row.get('430', 0),
                    turma_431=row.get('431', 0),
                    turma_432=row.get('432', 0),
                    turma_433=row.get('433', 0),
                    turma_434=row.get('434', 0),
                    turma_435=row.get('435', 0),
                    turma_436=row.get('436', 0),
                    turma_437=row.get('437', 0),
                    turma_438=row.get('438', 0),
                    turma_439=row.get('439', 0),
                    turma_441=row.get('441', 0),
                    turma_442=row.get('442', 0),
                    turma_447=row.get('447', 0),
                    turma_451=row.get('451', 0),
                    turma_471=row.get('471', 0),
                )
            return redirect('listar_habilidades_prof')  # Redireciona para a página de listagem
    else:
        form = UploadPlanilhaForm()

    return render(request, 'upload_planilha_prof.html', {'form': form})

###***********************************************************************************************************************

def listar_habilidades_prof(request):#####PRIMEIRO
    habilidades = HabilidadeProf.objects.all()
    total_acertos = sum(h.calcular_acertos() for h in habilidades)
    total_erros = sum(h.calcular_erros() for h in habilidades)
    
    return render(request, 'listar_habilidades_prof.html', {
        'habilidades': habilidades,
        'total_acertos': total_acertos,
        'total_erros': total_erros,
    })

###***********************************************************************************************************************

def habilidade_prof_view(request):
    habilidades = HabilidadeProf.objects.all()
    
    # Calcular totais
    total_acertos = sum(h.calcular_acertos() for h in habilidades)
    total_erros = sum(h.calcular_erros() for h in habilidades)
    total_respostas = total_acertos + total_erros

    percentual_acertos = (
        round((total_acertos / total_respostas) * 100, 2) if total_respostas > 0 else 0
    )
    percentual_erros = (
        round((total_erros / total_respostas) * 100, 2) if total_respostas > 0 else 0
    )
    
    # Lista de turmas (para garantir que o template receba a estrutura correta)
    turmas = [
        '401', '403', '404', '406', '408', '409', '410', '413', '414', '415',
        '417', '421', '423', '426', '428', '429', '430', '432', '433', '434',
        '435', '436', '437', '438', '439', '441', '442', '447', '451', '471'
    ]

    # Renderizar o template com os dados
    return render(request, 'diagnosis/prof/portugues.html', {
        'habilidades': habilidades,
        'total_corretas': total_acertos,
        'total_erradas': total_erros,
        'percentual_acertos': percentual_acertos,
        'percentual_erros': percentual_erros,
        'turmas': turmas,
    })

###***********************************************************************************************************************

def carregar_dados_habilidades(request):#####PRIMEIRO
    habilidades = HabilidadeProf.objects.all()
    data = []

    # Inicializar variáveis para os totais
    total_acertos = 0
    total_erros = 0

    for h in habilidades:
        # Calcular acertos e erros para cada habilidade
        acertos = h.calcular_acertos()
        erros = h.calcular_erros()

        # Atualizar os totais
        total_acertos += acertos
        total_erros += erros

        # Adicionar habilidade e valores ao JSON
        data.append({
            'item': h.item,
            'habilidade': h.habilidade,
            'turmas': {
                '401': h.turma_401,
                '403': h.turma_403,
                '404': h.turma_404,
                '406': h.turma_406,
                '408': h.turma_408,
                '409': h.turma_409,
                '410': h.turma_410,
                '413': h.turma_413,
                '414': h.turma_414,
                '415': h.turma_415,
                '417': h.turma_417,
                '421': h.turma_421,
                '423': h.turma_423,
                '426': h.turma_426,
                '428': h.turma_428,
                '429': h.turma_429,
                '430': h.turma_430,
                '432': h.turma_432,
                '433': h.turma_433,
                '434': h.turma_434,
                '435': h.turma_435,
                '436': h.turma_436,
                '437': h.turma_437,
                '438': h.turma_438,
                '439': h.turma_439,
                '441': h.turma_441,
                '442': h.turma_442,
                '447': h.turma_447,
                '451': h.turma_451,
                '471': h.turma_471,
            },
            'acertos': acertos,
            'erros': erros,
        })

    # Calcular percentuais gerais
    total_respostas = total_acertos + total_erros
    percentual_acertos = round((total_acertos / total_respostas) * 100, 2) if total_respostas > 0 else 0
    percentual_erros = round((total_erros / total_respostas) * 100, 2) if total_respostas > 0 else 0

    # Retornar os dados com os totais e percentuais
    return JsonResponse({
        'habilidades': data,
        'total_acertos': total_acertos,
        'total_erros': total_erros,
        'percentual_acertos': percentual_acertos,
        'percentual_erros': percentual_erros,
    })
###***********************************************************************************************************************

def carregar_habilidades(request):#####PRIMEIRO
    habilidades = HabilidadeProf.objects.all()
    data = []

    for h in habilidades:
        data.append({
            'item': h.item,
            'habilidade': h.habilidade,
            'turmas': {
                '401': h.turma_401,
                '403': h.turma_403,
                '404': h.turma_404,
                '406': h.turma_406,
                '408': h.turma_408,
                '409': h.turma_409,
                '410': h.turma_410,
                '413': h.turma_413,
                '414': h.turma_414,
                '415': h.turma_415,
                '417': h.turma_417,
                '421': h.turma_421,
                '423': h.turma_423,
                '426': h.turma_426,
                '428': h.turma_428,
                '429': h.turma_429,
                '430': h.turma_430,
                '432': h.turma_432,
                '433': h.turma_433,
                '434': h.turma_434,
                '435': h.turma_435,
                '436': h.turma_436,
                '437': h.turma_437,
                '438': h.turma_438,
                '439': h.turma_439,
                '441': h.turma_441,
                '442': h.turma_442,
                '447': h.turma_447,
                '451': h.turma_451,
                '471': h.turma_471,
            }
        })

    return JsonResponse({'habilidades': data})
###***********************************************************************************************************************

def habilidade_prof_anos_finais_view(request):#####SEGUNDO
    if request.method == 'POST' and 'planilha' in request.FILES:
        planilha = request.FILES['planilha']

        try:
            df = pd.read_csv(planilha, encoding='utf-8')
            df.columns = df.columns.str.strip()

            if 'Item' not in df.columns or 'Habilidade' not in df.columns:
                return render(request, 'diagnosis/prof/anos_finais.html', {
                    'error_message': 'As colunas "Item" e "Habilidade" são obrigatórias.'
                })

            # Limpar dados antigos e salvar novos
            HabilidadeProfAnosFinais.objects.all().delete()
            for _, row in df.iterrows():
                HabilidadeProfAnosFinais.objects.create(
                    item=row['Item'],
                    habilidade=row['Habilidade'],
                    turma_101=row.get('101', 0),
                    turma_102=row.get('102', 0),
                    # Adicione todos os campos conforme necessário
                    turma_171=row.get('171', 0),
                )

        except Exception as e:
            return render(request, 'diagnosis/prof/anos_finais.html', {
                'error_message': f'Erro ao processar a planilha: {str(e)}'
            })

    # Buscar dados do banco
    habilidades = HabilidadeProfAnosFinais.objects.all()

    # Calcular totais para os cards
    total_acertos = sum(h.calcular_acertos() for h in habilidades)
    total_erros = sum(h.calcular_erros() for h in habilidades)
    total_respostas = total_acertos + total_erros
    percentual_acertos = (
        round((total_acertos / total_respostas) * 100, 2) if total_respostas > 0 else 0
    )
    percentual_erros = (
        round((total_erros / total_respostas) * 100, 2) if total_respostas > 0 else 0
    )

    return render(request, 'diagnosis/prof/anos_finais.html', {
        'habilidades': habilidades,
        'total_corretas': total_acertos,
        'total_erradas': total_erros,
        'percentual_acertos': percentual_acertos,
        'percentual_erros': percentual_erros,
    })
###***********************************************************************************************************************

from .models import HabilidadeProfFinal  # Certifique-se de que o modelo está correto
import pandas as pd

def portugues_final_view(request):#####SEGUNDO
    if request.method == 'POST' and 'planilha' in request.FILES:
        planilha = request.FILES['planilha']

        try:
            # Ler a planilha enviada
            df = pd.read_csv(planilha, encoding='utf-8')
            df.columns = df.columns.str.strip()  # Remove espaços extras das colunas

            # Verificar as colunas obrigatórias
            if 'Item' not in df.columns or 'Habilidade' not in df.columns:
                return render(request, 'diagnosis/prof/portugues_finais.html', {
                    'error_message': 'As colunas "Item" e "Habilidade" são obrigatórias na planilha.'
                })

            # Limpar dados antigos e salvar os novos
            HabilidadeProfFinal.objects.all().delete()
            for _, row in df.iterrows():
                HabilidadeProfFinal.objects.create(
                    item=row['Item'],
                    habilidade=row['Habilidade'],
                    turma_101=row.get('101', 0),
                    turma_102=row.get('102', 0),
                    turma_103=row.get('103', 0),
                    turma_104=row.get('104', 0),
                    turma_105=row.get('105', 0),
                    turma_106=row.get('106', 0),
                    turma_107=row.get('107', 0),
                    turma_109=row.get('109', 0),
                    turma_110=row.get('110', 0),
                    turma_112=row.get('112', 0),
                    turma_114=row.get('114', 0),
                    turma_117=row.get('117', 0),
                    turma_119=row.get('119', 0),
                    turma_120=row.get('120', 0),
                    turma_121=row.get('121', 0),
                    turma_124=row.get('124', 0),
                    turma_126=row.get('126', 0),
                    turma_128=row.get('128', 0),
                    turma_129=row.get('129', 0),
                    turma_130=row.get('130', 0),
                    turma_131=row.get('131', 0),
                    turma_134=row.get('134', 0),
                    turma_135=row.get('135', 0),
                    turma_137=row.get('137', 0),
                    turma_138=row.get('138', 0),
                    turma_139=row.get('139', 0),
                    turma_140=row.get('140', 0),
                    turma_142=row.get('142', 0),
                    turma_143=row.get('143', 0),
                    turma_144=row.get('144', 0),
                    turma_145=row.get('145', 0),
                    turma_146=row.get('146', 0),
                    turma_147=row.get('147', 0),
                    turma_171=row.get('171', 0),
                )
        except Exception as e:
            return render(request, 'diagnosis/prof/portugues_finais.html', {
                'error_message': f'Erro ao processar a planilha: {str(e)}'
            })

        return redirect('diagnosis_prof_portugues_finais')

    # Buscar os dados do banco
    habilidades = HabilidadeProfFinal.objects.all()
    total_acertos = sum(h.calcular_acertos() for h in habilidades)
    total_erros = sum(h.calcular_erros() for h in habilidades)
    percentual_acertos = round((total_acertos / (total_acertos + total_erros)) * 100, 2) if (total_acertos + total_erros) > 0 else 0
    percentual_erros = round((total_erros / (total_acertos + total_erros)) * 100, 2) if (total_acertos + total_erros) > 0 else 0

    return render(request, 'diagnosis/prof/portugues_finais.html', {
        'habilidades': habilidades,
        'total_corretas': total_acertos,
        'total_erradas': total_erros,
        'percentual_acertos': percentual_acertos,
        'percentual_erros': percentual_erros,
    })

###***********************************************************************************************************************

def carregar_habilidades_final(request):#####SEGUNDO
    habilidades = HabilidadeProfFinal.objects.all()
    data = []

    for h in habilidades:
        data.append({
            'item': h.item,
            'habilidade': h.habilidade,
            'turmas': {
                '101': h.turma_101,
                '102': h.turma_102,
                '103': h.turma_103,
                '104': h.turma_104,
                '105': h.turma_105,
                '106': h.turma_106,
                '107': h.turma_107,
                '109': h.turma_109,
                '110': h.turma_110,
                '112': h.turma_112,
                '114': h.turma_114,
                '117': h.turma_117,
                '119': h.turma_119,
                '120': h.turma_120,
                '121': h.turma_121,
                '124': h.turma_124,
                '126': h.turma_126,
                '128': h.turma_128,
                '129': h.turma_129,
                '130': h.turma_130,
                '131': h.turma_131,
                '134': h.turma_134,
                '135': h.turma_135,
                '137': h.turma_137,
                '138': h.turma_138,
                '139': h.turma_139,
                '140': h.turma_140,
                '142': h.turma_142,
                '143': h.turma_143,
                '144': h.turma_144,
                '145': h.turma_145,
                '146': h.turma_146,
                '147': h.turma_147,
                '171': h.turma_171,
            }
        })

    return JsonResponse({'habilidades': data})
###***********************************************************************************************************************

def carregar_habilidades(request, tipo):
    # Escolha do modelo com base no tipo
    modelo = HabilidadeProf if tipo == 'inicial' else HabilidadeProfFinal
    habilidades = modelo.objects.all()
    
    # Formatar os dados corretamente
    data = []
    for h in habilidades:
        turmas = {
            '401': h.turma_401,
            '403': h.turma_403,
            '404': h.turma_404,
            '406': h.turma_406,
            '408': h.turma_408,
            '409': h.turma_409,
            '410': h.turma_410,
            '413': h.turma_413,
            '414': h.turma_414,
            '415': h.turma_415,
            '417': h.turma_417,
            '421': h.turma_421,
            '423': h.turma_423,
            '426': h.turma_426,
            '428': h.turma_428,
            '429': h.turma_429,
            '430': h.turma_430,
            '432': h.turma_432,
            '433': h.turma_433,
            '434': h.turma_434,
            '435': h.turma_435,
            '436': h.turma_436,
            '437': h.turma_437,
            '438': h.turma_438,
            '439': h.turma_439,
            '441': h.turma_441,
            '442': h.turma_442,
            '447': h.turma_447,
            '451': h.turma_451,
            '471': h.turma_471,
        }
        data.append({
            'item': h.item,
            'habilidade': h.habilidade,
            'turmas': turmas,
        })
    
    # Retornar os dados no formato esperado pelo JavaScript
    return JsonResponse({'habilidades': data})

###***********************************************************************************************************************
###*****BANCO DE CURRÍCULOS
###***********************************************************************************************************************

def registrar_curriculo(request):
    if request.method == "POST":
        nome = request.POST.get("nome_completo")
        email = request.POST.get("email")
        cpf = request.POST.get("cpf")
        senha = request.POST.get("senha")

        CadastroCandidato.objects.create(
            nome_completo=nome,
            email=email,
            cpf=cpf,
            senha=senha  # Passe em texto plano; será criptografada no método save
        )
        messages.success(request, "Cadastro realizado com sucesso!")
        return redirect("login_candidato")

    return render(request, "banco_curriculos/registrar.html")





###***********************************************************************************************************************

def listar_curriculos(request):
    curriculos = Curriculo.objects.all().order_by('-data_cadastro')
    return render(request, 'curriculos.html', {'curriculos': curriculos})
###***********************************************************************************************************************

def imprimir_curriculo(request, id):
    curriculo = Curriculo.objects.get(pk=id)
    template = get_template('banco_curriculos/curriculo_pdf.html')
    html = template.render({'curriculo': curriculo})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="curriculo_{curriculo.id}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Erro ao gerar o PDF', status=500)
    return response
###***********************************************************************************************************************



FormacaoFormSet = inlineformset_factory(Curriculo, Formacao, form=FormacaoForm, extra=1, can_delete=True)
ExperienciaFormSet = inlineformset_factory(Curriculo, Experiencia, form=ExperienciaForm, extra=1, can_delete=True)

def cadastrar_curriculo(request):
    if request.method == 'POST':
        curriculo_form = CurriculoForm(request.POST, request.FILES)
        formacao_formset = FormacaoFormSet(request.POST, instance=Curriculo())
        experiencia_formset = ExperienciaFormSet(request.POST, instance=Curriculo())

        if curriculo_form.is_valid() and formacao_formset.is_valid() and experiencia_formset.is_valid():
            curriculo = curriculo_form.save()
            formacao_formset.instance = curriculo
            experiencia_formset.instance = curriculo
            formacao_formset.save()
            experiencia_formset.save()
            return redirect('curriculo_sucesso')
    else:
        curriculo_form = CurriculoForm()
        formacao_formset = FormacaoFormSet(instance=Curriculo())
        experiencia_formset = ExperienciaFormSet(instance=Curriculo())

    return render(request, 'cadastrar_curriculo.html', {
        'curriculo_form': curriculo_form,
        'formacao_formset': formacao_formset,
        'experiencia_formset': experiencia_formset,
    })



class CurriculoCreateView(CreateView):
    model = Curriculo
    template_name = 'curriculo_create.html'
    fields = ['nome_completo', 'cpf', 'email', 'telefone', 'data_nascimento']  # Campos específicos
    success_url = '/curriculos/'  # Ajuste o caminho para a listagem de currículos


def curriculo_sucesso(request):
    return render(request, 'curriculo_sucesso.html')



# def cadastrar_curriculo(request):
#     return render(request, 'banco_curriculos/registrar.html')


###***********************************************************************************************************************
###*****CADASTRO DE DEMANDAS
###***********************************************************************************************************************

def tipo_demandas(request):
    return render(request, 'demandas/tipo_demandas.html')
###***********************************************************************************************************************

def cadastro_demandas(request):
    return render(request, 'demandas/cadastro_demandas.html')
###***********************************************************************************************************************

def gestao_demandas(request):
    return render(request, 'demandas/gestao_demandas.html')
###***********************************************************************************************************************

def relatorios_demandas(request):
    return render(request, 'demandas/relatorios_demandas.html')
###***********************************************************************************************************************

def criar_demanda(request):
    if request.method == 'POST':
        form = TipoDemandaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Demanda cadastrada com sucesso!')
            return redirect('criar_demanda')  # Redireciona para evitar reenvio duplicado
        else:
            messages.error(request, 'Erro ao cadastrar demanda. Verifique os dados.')
    else:
        form = TipoDemandaForm()

    # Buscando todas as demandas
    demandas = TipoDemanda.objects.all()
    return render(request, 'demandas/cadastro_demandas.html', {'form': form, 'demandas': demandas})
###***********************************************************************************************************************

def excluir_demanda(request, id):
    demanda = get_object_or_404(TipoDemanda, id=id)
    demanda.delete()
    messages.success(request, 'Demanda excluída com sucesso!')
    return redirect('criar_demanda')  # Redireciona para a página principal
###***********************************************************************************************************************

def editar_demanda(request, id):
    # Recupera a demanda ou retorna 404 se não for encontrada
    demanda = get_object_or_404(TipoDemanda, id=id)
    
    if request.method == 'POST':
        # Atualiza os dados da demanda com os valores do formulário
        form = TipoDemandaForm(request.POST, instance=demanda)
        if form.is_valid():
            form.save()  # Salva as alterações no banco de dados
            messages.success(request, 'Demanda atualizada com sucesso!')
            return redirect('criar_demanda')  # Redireciona para a página principal ou tabela
        else:
            messages.error(request, 'Erro ao atualizar demanda. Verifique os dados.')
    else:
        # Carrega o formulário com os dados da demanda
        form = TipoDemandaForm(instance=demanda)
    
    return render(request, 'demandas/editar_demanda.html', {'form': form, 'demanda': demanda})
###***********************************************************************************************************************

def gestao_demandas(request):
    demandas = TipoDemanda.objects.all()
    total_demandas = demandas.count()
    concluidas = demandas.filter(status="Finalizado").count()
    em_andamento = demandas.filter(status="Em andamento").count()
    pendentes = demandas.filter(status="Pendente").count()
    
    context = {
        'demandas': demandas,
        'total_demandas': total_demandas,
        'concluidas': concluidas,
        'em_andamento': em_andamento,
        'pendentes': pendentes,
    }
    return render(request, 'demandas/gestao_demandas.html', context)
###***********************************************************************************************************************

def relatorios_demandas(request):
    demandas = TipoDemanda.objects.all()

    # Filtros
    status = request.GET.get('status')
    prioridade = request.GET.get('prioridade')
    date_start = request.GET.get('date_start')
    date_end = request.GET.get('date_end')

    if status:
        demandas = demandas.filter(status=status)
    if prioridade:
        demandas = demandas.filter(prioridade=prioridade)
    if date_start and date_end:
        demandas = demandas.filter(data_cadastro__range=[date_start, date_end])

    context = {
        'demandas': demandas,
        'total_demandas': demandas.count(),
        'concluidas': demandas.filter(status="Finalizado").count(),
        'em_andamento': demandas.filter(status="Em andamento").count(),
        'pendentes': demandas.filter(status="Pendente").count(),
    }
    return render(request, 'demandas/relatorios_demandas.html', context)
###***********************************************************************************************************************

from django.http import JsonResponse

def listar_demandas(request):
    demandas = TipoDemanda.objects.values(
        "id",
        "data_cadastro",
        "data_entrega",
        "descricao",
        "responsavel",
        "destinatario",
        "prioridade",
        "status"
    )
    return JsonResponse(list(demandas), safe=False)
###***********************************************************************************************************************

def criar_tipo_demanda(request):
    if request.method == 'POST':
        form = TipoDemandaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tipo de demanda criado com sucesso!')
            return redirect('tipo_demandas')
        else:
            messages.error(request, 'Erro ao criar tipo de demanda. Verifique os dados.')
    else:
        form = TipoDemandaForm()
    
    return render(request, 'demandas/criar_tipo_demanda.html', {'form': form})
###***********************************************************************************************************************

def gerar_relatorio_pdf(request):
    # Filtrar as demandas com base nos filtros aplicados (opcional)
    status = request.GET.get('status', '')
    prioridade = request.GET.get('prioridade', '')
    date_start = request.GET.get('date_start', '')
    date_end = request.GET.get('date_end', '')

    demandas = TipoDemanda.objects.all()

    if status:
        demandas = demandas.filter(status=status)
    if prioridade:
        demandas = demandas.filter(prioridade=prioridade)
    if date_start and date_end:
        demandas = demandas.filter(data_cadastro__range=[date_start, date_end])

    # Renderizar o template para o PDF
    template_path = 'demandas/relatorio_pdf.html'
    context = {'demandas': demandas}
    template = get_template(template_path)
    html = template.render(context)

    # Criar o PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio_demandas.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)

    # Verificar se houve erros
    if pisa_status.err:
        return HttpResponse('Erro ao gerar o PDF', status=500)

    return response
###***********************************************************************************************************************

def editar_escola(request, id):
    escola = get_object_or_404(Escola, id=id)
    if request.method == "POST":
        # Processa o formulário aqui
        pass
    return render(request, 'editar_escola.html', {'escola': escola})
###***********************************************************************************************************************

def adicionar_escola(request):
    if request.method == 'POST':
        form = EscolaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('listar_escolas')  # Certifique-se de ajustar para a URL correta
    else:
        form = EscolaForm()

    return render(request, 'escolas/adicionar_escola.html', {'form': form})
###***********************************************************************************************************************

def cadastrar_professor(request):
    if request.method == 'POST':
        form = ProfessorForm(request.POST, request.FILES)  # Inclua `request.FILES` para arquivos.
        if form.is_valid():
            form.save()
            return redirect('listar_professores')  # Redireciona para a página de listagem.
    else:
        form = ProfessorForm()

    return render(request, 'cadastrar_professor.html', {'form': form})
###***********************************************************************************************************************

def sucesso(request):
    return render(request, 'sucesso.html')
###***********************************************************************************************************************

def curriculo_sucesso(request):
    return render(request, 'semedapp/curriculo_sucesso.html')
###***********************************************************************************************************************

def listar_professores(request):
    professores = Professor.objects.all()
    return render(request, 'semedapp/listar_professores.html', {'professores': professores})
###***********************************************************************************************************************

def editar_professor(request, professor_id):
    professor = get_object_or_404(Professor, id=professor_id)
    if request.method == 'POST':
        form = ProfessorForm(request.POST, request.FILES, instance=professor)
        if form.is_valid():
            form.save()
            return redirect('listar_professores')
    else:
        form = ProfessorForm(instance=professor)
    return render(request, 'semedapp/editar_professor.html', {'form': form, 'professor': professor})
###***********************************************************************************************************************

def excluir_professor(request, professor_id):
    professor = get_object_or_404(Professor, id=professor_id)
    professor.delete()
    messages.success(request, "Professor excluído com sucesso.")
    return redirect('listar_professores')
###***********************************************************************************************************************

# View para relatórios de professores
def relatorios_professores(request):
    professores = Professor.objects.all()
    # Lógica para gerar relatórios (simplesmente listando os professores por enquanto)
    return render(request, 'semedapp/relatorios_professores.html', {'professores': professores})
###***********************************************************************************************************************

def criar_professor(request):
    if request.method == 'POST':
        # Extração de dados do formulário
        nome_completo = request.POST.get('nome_completo')
        cpf = request.POST.get('cpf')
        rg = request.POST.get('rg', None)
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        endereco = request.POST.get('endereco')
        bairro = request.POST.get('bairro', None)
        cidade = request.POST.get('cidade', 'Canaã dos Carajás')  # Valor padrão
        cep = request.POST.get('cep', None)
        estado_civil = request.POST.get('estado_civil')
        sexo = request.POST.get('sexo')
        data_nascimento = request.POST.get('data_nascimento', None)

        # Formação Acadêmica
        formacao_academica = request.POST.get('formacao_academica', None)
        curso = request.POST.get('curso', None)
        instituicao = request.POST.get('instituicao', None)
        ano_conclusao = request.POST.get('ano_conclusao', None)

        # Experiência Profissional
        experiencia_profissional = request.POST.get('experiencia_profissional', None)

        # Arquivos
        foto = request.FILES.get('foto', None)
        curriculo_pdf = request.FILES.get('arquivo_curriculo', None)
        certificados_pdf = request.FILES.get('arquivo_certificados', None)

        # Salvando os dados no banco de dados
        professor = Professor(
            nome_completo=nome_completo,
            cpf=cpf,
            rg=rg,
            email=email,
            telefone=telefone,
            endereco=endereco,
            bairro=bairro,
            cidade=cidade,
            cep=cep,
            estado_civil=estado_civil,
            sexo=sexo,
            data_nascimento=data_nascimento,
            formacao_academica=formacao_academica,
            curso=curso,
            instituicao=instituicao,
            ano_conclusao=ano_conclusao,
            experiencia_profissional=experiencia_profissional,
            foto=foto,
            curriculo_pdf=curriculo_pdf,
            certificados_pdf=certificados_pdf,
        )
        professor.save()  # Salva no banco de dados

        return redirect('listar_professores')  # Redirecione após salvar

    return render(request, 'semedapp/criar_professor.html')
###***********************************************************************************************************************
# View para listar diretores
def listar_diretores(request):
    # Obtem todos os diretores
    diretores = Diretor.objects.all()

    # Calcula o total de currículos
    total_curriculos = diretores.count()

    # Contexto para o template
    context = {
        'diretores': diretores,
        'total_curriculos': total_curriculos,  # Adiciona o total de currículos ao contexto
    }

    return render(request, 'semedapp/listar_diretores.html', context)

###***********************************************************************************************************************
# View para cadastrar diretor


from .forms import DiretorForm, ExperienciaFormSet, FormacaoFormSet, CertificadoFormSet


def cadastrar_diretor(request):
    if request.method == 'POST':
        # Captura os campos do formulário
        nome_completo = request.POST.get('nome_completo')
        cpf = request.POST.get('cpf')
        rg = request.POST.get('rg')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        endereco = request.POST.get('endereco')
        bairro = request.POST.get('bairro')
        cidade = request.POST.get('cidade')
        cep = request.POST.get('cep')
        estado_civil = request.POST.get('estado_civil')
        sexo = request.POST.get('sexo')
        data_nascimento = request.POST.get('data_nascimento') or None
        formacao_academica = request.POST.get('formacao_academica')
        curso = request.POST.get('curso')
        instituicao = request.POST.get('instituicao')
        ano_conclusao = request.POST.get('ano_conclusao')
        experiencia_profissional = request.POST.get('experiencia_profissional')

        # Novos campos de experiência profissional
        empresa = request.POST.get('empresa')
        cargo = request.POST.get('cargo')
        data_inicio = request.POST.get('data_inicio') or None
        data_fim = request.POST.get('data_fim') or None

        # Processa arquivos enviados
        foto = request.FILES.get('foto')
        curriculo_pdf = request.FILES.get('curriculo_pdf')
        certificados_pdf = request.FILES.get('certificados_pdf')

        # Verifica se o CPF ou e-mail já estão cadastrados
        if Diretor.objects.filter(cpf=cpf).exists():
            messages.error(request, 'O CPF informado já está cadastrado.')
            return redirect('cadastrar_diretor')
        
        if Diretor.objects.filter(email=email).exists():
            messages.error(request, 'O e-mail informado já está cadastrado.')
            return redirect('cadastrar_diretor')

        # Cria a instância do modelo e salva no banco de dados
        try:
            diretor = Diretor(
                nome_completo=nome_completo,
                cpf=cpf,
                rg=rg,
                email=email,
                telefone=telefone,
                endereco=endereco,
                bairro=bairro,
                cidade=cidade,
                cep=cep,
                estado_civil=estado_civil,
                sexo=sexo,
                data_nascimento=data_nascimento,
                formacao_academica=formacao_academica,
                curso=curso,
                instituicao=instituicao,
                ano_conclusao=ano_conclusao,
                experiencia_profissional=experiencia_profissional,
                empresa=empresa,
                cargo=cargo,
                data_inicio=data_inicio,
                data_fim=data_fim,
                foto=foto,
                curriculo_pdf=curriculo_pdf,
                certificados_pdf=certificados_pdf,
            )
            diretor.save()
            messages.success(request, f"Currículo de {nome_completo} cadastrado com sucesso!")
            return redirect('cadastrar_diretor')
        except Exception as e:
            messages.error(request, f"Erro ao cadastrar o currículo: {str(e)}")
            return redirect('cadastrar_diretor')

    return render(request, 'semedapp/cadastrar_diretor.html')

###***********************************************************************************************************************

def visualizar_diretor(request, id):
    diretor = get_object_or_404(Diretor, id=id)
    return render(request, 'semedapp/visualizar_diretor.html', {'diretor': diretor})
###***********************************************************************************************************************

class VisualizarDiretorView(DetailView):
    model = Diretor
    template_name = 'semedapp/visualizar_diretor.html'
    context_object_name = 'diretor'
###***********************************************************************************************************************

def editar_diretor(request, id):
    diretor = get_object_or_404(Diretor, id=id)
    
    if request.method == 'POST':
        form = DiretorForm(request.POST, instance=diretor)
        if form.is_valid():
            form.save()
            return redirect('listar_diretores')  # Ajuste o nome da URL para redirecionar após salvar
    else:
        form = DiretorForm(instance=diretor)
    
    return render(request, 'semedapp/editar_diretor.html', {'form': form, 'diretor': diretor})
###***********************************************************************************************************************

def excluir_diretor(request, id):
    diretor = get_object_or_404(Diretor, id=id)
    diretor.delete()
    return redirect('listar_diretores')  # Ajuste o nome para a URL de listagem
###***********************************************************************************************************************

class DiretorDeleteView(DeleteView):
    model = Diretor
    success_url = reverse_lazy('listar_diretores')
    template_name = 'semedapp/confirmar_exclusao.html'
###***********************************************************************************************************************

def imprimir_curriculo(request, diretor_id):
    # Obtém o diretor pelo ID
    try:
        diretor = Diretor.objects.get(id=diretor_id)
    except Diretor.DoesNotExist:
        return HttpResponse("Diretor não encontrado", status=404)

    # Renderiza o template em HTML
    html_string = render_to_string('diretor_curriculo_pdf.html', {'diretor': diretor})

    # Configura o WeasyPrint para gerar o PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="curriculo_{diretor.nome_completo}.pdf"'

    HTML(string=html_string).write_pdf(response)
    return response
###***********************************************************************************************************************

import qrcode
from io import BytesIO
from django.shortcuts import get_object_or_404
from django.core.files.base import ContentFile
from django.http import HttpResponse


def gerar_qrcode(request, diretor_id):
    diretor = get_object_or_404(Diretor, id=diretor_id)
    data = f"https://example.com/curriculo/{diretor.id}"  # URL personalized for the director

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Save QR Code to the diretor's folder
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    filename = f"qrcode_{diretor.id}.png"
    diretor.qr_code.save(filename, ContentFile(buffer.read()))
    buffer.close()

    return HttpResponse(diretor.qr_code.url)


###***********************************************************************************************************************

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import CadastroCandidato

def registrar_candidato(request):
    if request.method == "POST":
        nome_completo = request.POST.get("nome_completo")
        email = request.POST.get("email")
        cpf = request.POST.get("cpf")
        senha = request.POST.get("password")
        confirm_senha = request.POST.get("confirm_password")

        # Verifica se as senhas coincidem
        if senha != confirm_senha:
            messages.error(request, "As senhas não coincidem!")
            return redirect("registrar_candidato")

        try:
            # Cria o usuário no sistema
            user = User.objects.create_user(username=email, email=email, password=senha)
            user.first_name = nome_completo
            user.save()

            # Cria o perfil de candidato
            candidato = CadastroCandidato.objects.create(
                user=user,
                nome_completo=nome_completo,
                cpf=cpf,
            )

            # Autentica e loga o usuário automaticamente
            user = authenticate(request, username=email, password=senha)
            if user is not None:
                login(request, user)
                messages.success(request, "Cadastro realizado com sucesso!")
                return redirect("area_candidato")

        except Exception as e:
            messages.error(request, f"Erro ao cadastrar: {str(e)}")
            return redirect("registrar_candidato")

    return render(request, "banco_curriculos/registrar.html")


###***********************************************************************************************************************

from django.shortcuts import render, redirect
from django.contrib import messages
from semedapp.models import CadastroCandidato

def login_candidato(request):
    if request.method == "POST":
        email = request.POST.get("email")
        senha = request.POST.get("password")

        candidato = CadastroCandidato.objects.filter(email=email).first()
        if candidato and candidato.check_senha(senha):
            # Salve o ID e o nome na sessão para identificar o usuário logado
            request.session["candidato_id"] = candidato.id
            request.session["candidato_nome"] = candidato.nome_completo
            messages.success(request, f"Bem-vindo, {candidato.nome_completo}!")
            return redirect("area_candidato")  # Redirecione para a área do candidato
        else:
            messages.error(request, "E-mail ou senha inválidos.")
    
    return render(request, "banco_curriculos/login.html")




###***********************************************************************************************************************

@login_required
def area_administrativa(request):
    return render(request, "semedapp/area_administrativa.html", {"user": request.user})


###***********************************************************************************************************************
def exportar_excel(request):
    # Cria um workbook e uma planilha
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Diretores"

    # Cabeçalhos da tabela
    ws.append(["Nome", "CPF", "RG", "Email", "Telefone", "Endereço", "Bairro", "Cidade", "Nascimento"])

    # Adiciona os dados dos diretores
    diretores = Diretor.objects.all()
    for diretor in diretores:
        ws.append([
            diretor.nome_completo,
            diretor.cpf,
            diretor.rg,
            diretor.email,
            diretor.telefone,
            diretor.endereco,
            diretor.bairro,
            diretor.cidade,
            diretor.data_nascimento.strftime("%d/%m/%Y") if diretor.data_nascimento else "",
        ])

    # Configura a resposta HTTP
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = 'attachment; filename="diretores.xlsx"'
    wb.save(response)

    return response

###***********************************************************************************************************************
def exportar_pdf(request):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="diretores.pdf"'

    p = canvas.Canvas(response)
    p.setFont("Helvetica", 12)
    y = 800

    p.drawString(100, y, "Lista de Diretores")
    y -= 20

    diretores = Diretor.objects.all()
    for diretor in diretores:
        p.drawString(100, y, f"Nome: {diretor.nome_completo}, CPF: {diretor.cpf}")
        y -= 20

    p.showPage()
    p.save()

    return response

###***********************************************************************************************************************
def exportar_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="diretores.csv"'

    writer = csv.writer(response)
    writer.writerow(["Nome", "CPF", "RG", "Email", "Telefone", "Endereço", "Bairro", "Cidade", "Nascimento"])

    diretores = Diretor.objects.all()
    for diretor in diretores:
        writer.writerow([
            diretor.nome_completo,
            diretor.cpf,
            diretor.rg,
            diretor.email,
            diretor.telefone,
            diretor.endereco,
            diretor.bairro,
            diretor.cidade,
            diretor.data_nascimento.strftime("%d/%m/%Y") if diretor.data_nascimento else "",
        ])

    return response

###***********************************************************************************************************************
def exportar_xls(request):
    response = HttpResponse(content_type="application/ms-excel")
    response["Content-Disposition"] = 'attachment; filename="diretores.xls"'

    wb = xlwt.Workbook(encoding="utf-8")
    ws = wb.add_sheet("Diretores")

    # Cabeçalhos
    columns = ["Nome", "CPF", "RG", "Email", "Telefone", "Endereço", "Bairro", "Cidade", "Nascimento"]
    for col_num, column_title in enumerate(columns):
        ws.write(0, col_num, column_title)

    # Dados
    rows = Diretor.objects.all()
    for row_num, diretor in enumerate(rows, start=1):
        ws.write(row_num, 0, diretor.nome_completo)
        ws.write(row_num, 1, diretor.cpf)
        ws.write(row_num, 2, diretor.rg)
        ws.write(row_num, 3, diretor.email)
        ws.write(row_num, 4, diretor.telefone)
        ws.write(row_num, 5, diretor.endereco)
        ws.write(row_num, 6, diretor.bairro)
        ws.write(row_num, 7, diretor.cidade)
        ws.write(row_num, 8, diretor.data_nascimento.strftime("%d/%m/%Y") if diretor.data_nascimento else "")

    wb.save(response)
    return response
###***********************************************************************************************************************
# Página inicial do Portal da Transparência
def transparencia_index(request):
    return render(request, 'transparencia/index.html')
###***********************************************************************************************************************
# Página de Folha de Pagamento
def transparencia_folha_pagamento(request):
    # Lógica da folha de pagamento
    return render(request, 'transparencia/folha_pagamento.html')
###***********************************************************************************************************************

# Página de Alimentação
def transparencia_alimentacao(request):
    # Lógica para carregar os dados de alimentação
    return render(request, 'transparencia/alimentacao.html')
###***********************************************************************************************************************

# Página de Bens de Consumo
def transparencia_bens_consumo(request):
    # Lógica para carregar os dados de bens e consumo
    return render(request, 'transparencia/bens_consumo.html')
###***********************************************************************************************************************

# Página de Outros Gastos
def outros_gastos(request):
    return render(request, 'transparencia/outros_gastos.html')
###***********************************************************************************************************************

def privacy_policy(request):
    return render(request, 'semedapp/privacy_policy.html')
###***********************************************************************************************************************

def contact_us(request):
    return render(request, 'semedapp/contact_us.html')
###***********************************************************************************************************************

def help(request):
    return render(request, 'semedapp/help.html')
###***********************************************************************************************************************

def pesquisar_curriculos(request):
    return render(request, 'semedapp/pesquisar_curriculos.html')
###***********************************************************************************************************************
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from semedapp.models import FormacaoAcademica
from .forms import FormacaoAcademicaForm


def cadastrar_formacao(request, diretor_id):
    diretor = get_object_or_404(Diretor, id=diretor_id)

    if request.method == 'POST':
        nivel = request.POST.get('nivel')
        instituicao = request.POST.get('instituicao')
        curso = request.POST.get('curso')
        ano_conclusao = request.POST.get('ano_conclusao')

        try:
            FormacaoAcademica.objects.create(
                diretor=diretor,
                nivel=nivel,
                instituicao=instituicao,
                curso=curso,
                ano_conclusao=ano_conclusao,
            )
            messages.success(request, f"Formação adicionada com sucesso para o diretor {diretor.nome_completo}!")
            return redirect('detalhes_diretor', diretor_id=diretor.id)
        except Exception as e:
            messages.error(request, f"Erro ao cadastrar a formação: {str(e)}")
            return redirect('cadastrar_formacao', diretor_id=diretor.id)

    return render(request, 'semedapp/cadastrar_formacao.html', {'diretor': diretor})


from django.shortcuts import render

def registrar_novo_curriculo(request):
    return render(request, 'banco_curriculos/registrar.html')



from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CadastroCandidato


from django.contrib.auth.hashers import make_password
from django.db import IntegrityError

def cadastrar_candidato(request):
    if request.method == "POST":
        nome_completo = request.POST.get("nome_completo")
        email = request.POST.get("email")
        cpf = request.POST.get("cpf")
        senha = request.POST.get("password")
        confirm_senha = request.POST.get("confirm_password")

        if senha != confirm_senha:
            messages.error(request, "As senhas não coincidem!")
            return redirect("registrar_candidato")

        try:
            # Cria o candidato no banco de dados
            candidato = CadastroCandidato.objects.create(
                nome_completo=nome_completo,
                email=email,
                cpf=cpf,
                senha=make_password(senha),  # Criptografa a senha
            )

            # Salva o ID do candidato na sessão para login automático
            request.session["candidato_id"] = candidato.id
            messages.success(request, f"Bem-vindo, {candidato.nome_completo}!")
            return redirect("area_candidato")

        except IntegrityError as e:
            # Mensagem de erro no caso de duplicação de email ou CPF
            messages.error(request, "Já existe um candidato com este e-mail ou CPF.")
            print(f"Erro de integridade: {e}")

        except Exception as e:
            # Tratamento de outros erros
            messages.error(request, "Erro ao cadastrar candidato. Tente novamente.")
            print(f"Erro ao cadastrar candidato: {e}")

    return render(request, "banco_curriculos/registrar.html")







def area_candidato(request):
    candidato_id = request.session.get('candidato_id')

    if not candidato_id:
        # Redireciona para o login se não estiver logado
        messages.error(request, "Você precisa estar logado para acessar esta página.")
        return redirect("login_candidato")

    # Busca os dados do candidato
    candidato = CadastroCandidato.objects.get(id=candidato_id)

    return render(request, "banco_curriculos/area_candidato.html", {"candidato": candidato})




@login_required
def adicionar_curriculo(request):
    """View para adicionar um novo currículo."""
    if request.method == 'POST':
        form = CurriculoForm(request.POST, request.FILES)
        if form.is_valid():
            curriculo = form.save(commit=False)
            curriculo.usuario = request.user  # Associa o currículo ao usuário autenticado
            curriculo.save()
            messages.success(request, 'Currículo cadastrado com sucesso!')
            return redirect('area_candidato')
    else:
        form = CurriculoForm()

    return render(request, 'banco_curriculos/adicionar_curriculo.html', {'form': form})


from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib import messages

def logout_candidato(request):
    # Destroi a sessão
    logout(request)
    # Adiciona uma mensagem de sucesso
    messages.success(request, "Você saiu com sucesso.")
    # Redireciona para a página de login
    return redirect("login_candidato")



from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def minhas_inscricoes(request):
    # Obtém as inscrições relacionadas ao usuário logado
    inscricoes = request.user.inscricoes_usuario.all()  # Use o related_name definido no modelo

    # Renderiza a página com uma mensagem amigável caso não existam inscrições
    contexto = {
        'inscricoes': inscricoes,
        'mensagem': 'Nenhuma inscrição encontrada!' if not inscricoes else None
    }
    return render(request, 'banco_curriculos/minhas_inscricoes.html', contexto)






import qrcode
from django.core.files.base import ContentFile

def gerar_qr_code(diretor):
    data = f"Currículo de {diretor.nome_completo}"
    qr = qrcode.make(data)

    # Salvar o QR Code na pasta correta
    qr_code_path = f"diretores_qrcodes/qr_code_{diretor.id}.png"
    with open(f"{settings.MEDIA_ROOT}/{qr_code_path}", "wb") as qr_file:
        qr.save(qr_file)

    diretor.qr_code.save(qr_code_path, ContentFile(qr_file.read()), save=True)


from django.http import JsonResponse
from semedapp.models import Diretor

def verificar_cpf(request):
    cpf = request.GET.get('cpf')
    if Diretor.objects.filter(cpf=cpf).exists():
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'message': 'CPF não encontrado no sistema!'})


from django.shortcuts import render
from django.http import HttpResponse
from weasyprint import HTML
from .models import Diretor

def imprimir_curriculo(request, cpf):
    try:
        # Buscar o diretor pelo CPF
        diretor = Diretor.objects.get(cpf=cpf)
        
        # Gerar o HTML do currículo
        html_string = render_to_string('semedapp/imprimir_curriculo.html', {'diretor': diretor})
        
        # Gerar o PDF
        pdf = HTML(string=html_string).write_pdf()
        
        # Retornar o PDF como resposta
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="curriculo_{diretor.nome_completo}.pdf"'
        return response

    except Diretor.DoesNotExist:
        # Retornar um alerta caso o CPF não seja encontrado
        return render(request, 'semedapp/imprimir_curriculo.html', {
            'alerta': f'Currículo não encontrado para o CPF: {cpf}.'
        })
    

from django import forms
from .models import Candidato

class FormDeAtualizacao(forms.ModelForm):
    class Meta:
        model = Candidato
        fields = ['nome_completo', 'email', 'cpf']  # Inclua os campos que deseja permitir edição



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required(login_url='login')  # Redireciona para a página de login se o usuário não estiver autenticado
def editar_perfil(request):
    if request.user.is_authenticated:
        try:
            # Lógica para editar perfil
            return render(request, 'editar_perfil.html', {})
        except Exception as e:
            messages.error(request, "Ocorreu um erro ao carregar a página.")
            return redirect('home')
    else:
        messages.error(request, "Você precisa estar autenticado para acessar esta área.")
        return redirect('login')





# from django.contrib.auth.models import User
# from .models import Candidato

# # Exemplo ao criar um novo candidato
# def criar_candidato():
#     user = User.objects.create_user(username='usuario', password='senha123')
#     candidato = Candidato.objects.create(
#         user=user,
#         nome_completo='João da Silva',
#         cpf='123.456.789-00',
#         email='joao@example.com',
#     )



from django.shortcuts import redirect
from functools import wraps

def module_permission_required(module_name):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("login")
            
            # Verificar se o usuário é administrador ou tem permissão para o módulo
            if (
                request.user.role == "Administrador"
                or RoleModulePermission.objects.filter(
                    role=request.user.role,
                    module__module_name=module_name,
                ).exists()
            ):
                return view_func(request, *args, **kwargs)
            return redirect("acesso_negado")
        return _wrapped_view
    return decorator




@module_permission_required("Cadastro Demanda")
def cadastro_demanda_view(request):
    return render(request, "modulos/cadastro_demanda.html")

@module_permission_required("Indicadores")
def indicadores_view(request):
    return render(request, "modulos/indicadores.html")
