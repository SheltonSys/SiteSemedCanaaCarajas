
from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser, BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth import get_user_model
from .managers import UserManager  # Certifique-se de ter um UserManager configurado
from django.conf import settings
from django.core.files.base import ContentFile
import qrcode
from io import BytesIO
import io
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from functools import wraps
from django.apps import apps




from django.db import models
from django.conf import settings

class Module(models.Model):
    """
    Representa um módulo no sistema que pode ser acessado por usuários.
    """
    nome = models.CharField(max_length=100, unique=True)
    url = models.CharField(max_length=191, unique=True)

    class Meta:
        db_table = "semedapp_module"

    def __str__(self):
        return self.nome
# ********************************************************************************************************************************



# ********************************************************************************************************************************

class ModuleAccess(models.Model):
    """
    Registra os acessos dos usuários aos módulos do sistema.
    """
    MODULE_CHOICES = [
        ('configuracao', 'Configuração'),
        ('indicadores', 'Indicadores'),
        ('pedagogico', 'Pedagógico'),
        ('contabilidade', 'Contabilidade'),
        ('curriculos', 'Banco de Currículos'),
        ('site_semed', 'Site Semed'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    module = models.CharField(max_length=50, choices=MODULE_CHOICES)
    accessed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "semedapp_module_access"

    def __str__(self):
        return f"{self.user.username} - {self.get_module_display()}"
# ********************************************************************************************************************************

def module_required(module_name):
    """
    Restringe o acesso a usuários com permissão para determinado módulo.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            module = get_object_or_404(Module, nome=module_name)
            has_permission = UserModulePermission.objects.filter(user=request.user, module=module).exists()

            if not has_permission:
                raise PermissionDenied  # Retorna erro 403 se não tiver acesso

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
# ********************************************************************************************************************************

class Habilidade(models.Model):
    nome = models.CharField(max_length=191)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome
# ********************************************************************************************************************************
    
class Acompanhamento(models.Model):
    aluno = models.ForeignKey('Aluno', on_delete=models.CASCADE)  # Relacione com o modelo de Aluno
    descricao = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Acompanhamento para {self.aluno}"
# ********************************************************************************************************************************

from django.db import models

class Aluno(models.Model):
    pessoa_nome = models.CharField(max_length=191)
    cpf = models.CharField(max_length=25, blank=True, null=True)
    idade = models.IntegerField(blank=True, null=True)
    modalidade = models.CharField(max_length=50, blank=True, null=True)
    avaliado = models.CharField(max_length=10, choices=[('SIM', 'Sim'), ('NAO', 'Não')], default='NAO')
    professor = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.SET_NULL,
    null=True,
    blank=True
)
    turma = models.ForeignKey('Turma', on_delete=models.CASCADE, related_name='alunos')

    def __str__(self):
        return self.pessoa_nome
# ********************************************************************************************************************************

from django.db import models

class Estudante(models.Model):
    nome_completo = models.CharField(max_length=150)
    data_nascimento = models.DateField()
    email = models.EmailField()
    matricula = models.CharField(max_length=20, unique=True)
    turma = models.CharField(max_length=50)

    def __str__(self):
        return self.nome_completo
# ********************************************************************************************************************************

class PDDE(models.Model):
    ano = models.IntegerField()
    escola = models.CharField(max_length=191)
    status = models.CharField(
        max_length=20,
        choices=[('aprovado', 'Aprovado'), ('pendente', 'Pendente')],
        default='pendente',
    )
    detalhes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.ano} - {self.escola} ({self.status})"
# ********************************************************************************************************************************

class Diretoria(models.Model):
    nome = models.CharField(max_length=191)
    cargo = models.CharField(max_length=50, choices=[
        ("Presidente", "Presidente"),
        ("Vice-Presidente", "Vice-Presidente"),
        ("Secretário", "Secretário"),
        ("Tesoureiro", "Tesoureiro"),
    ])
    endereco = models.CharField(max_length=191)
    bairro = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    email = models.EmailField()
    cep = models.CharField(max_length=10)
    cpf = models.CharField(max_length=25)
    vencimento = models.DateField(null=True, blank=True)
    escola = models.ForeignKey('EscolaPdde', on_delete=models.CASCADE, related_name='diretores')
    conselho = models.CharField(max_length=191, blank=True, null=True)  # ✅ Aqui que estava faltando

    def __str__(self):
        return f"{self.nome} - {self.cargo}"



# ********************************************************************************************************************************

class MembroConselho(models.Model):
    inep = models.CharField(max_length=20)
    escola = models.CharField(max_length=191)
    conselho = models.CharField(max_length=191, blank=True, null=True)  # Conselho vinculado
    data_abertura = models.DateField()
    data_vencimento = models.DateField()
    nome = models.CharField(max_length=191)
    funcao = models.CharField(max_length=50, choices=[
        ('Conselho Fiscal - Efetivo', 'Conselho Fiscal - Efetivo'),
        ('Conselho Fiscal - Suplente', 'Conselho Fiscal - Suplente'),
        ('Conselho Deliberativo', 'Conselho Deliberativo'),
    ])
    endereco = models.CharField(max_length=191)
    bairro = models.CharField(max_length=100)
    telefone = models.CharField(max_length=15)
    email = models.EmailField()
    cep = models.CharField(max_length=10)
    cpf = models.CharField(max_length=25)

    def __str__(self):
        return self.nome
# ********************************************************************************************************************************

class LivroCaixa(models.Model):
    ano_base = models.IntegerField()
    escola = models.ForeignKey('EscolaPdde', on_delete=models.CASCADE)
    conselho_escolar = models.CharField(max_length=191)
    cnpj = models.CharField(max_length=20)
    rendimentos_aplicacao = models.DecimalField(max_digits=10, decimal_places=2)
    saldo_anterior = models.DecimalField(max_digits=10, decimal_places=2)
    receita_total = models.DecimalField(max_digits=10, decimal_places=2)
    despesas_manutencao = models.DecimalField(max_digits=10, decimal_places=2)
    despesa_total = models.DecimalField(max_digits=10, decimal_places=2)
    superavit_deficit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.ano_base} - {self.escola.nome}"



# ********************************************************************************************************************************

class EscrituraFiscal(models.Model):
    ano_base = models.IntegerField()
    conselho_escolar = models.CharField(max_length=191)
    cnpj = models.CharField(max_length=18)
    rendimentos_aplicacao = models.DecimalField(max_digits=10, decimal_places=2)
    saldo_anterior = models.DecimalField(max_digits=10, decimal_places=2)
    receita_total = models.DecimalField(max_digits=10, decimal_places=2)
    despesas_manutencao = models.DecimalField(max_digits=10, decimal_places=2)
    despesa_total = models.DecimalField(max_digits=10, decimal_places=2)
    superavit_deficit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.conselho_escolar} - {self.ano_base}"
# ********************************************************************************************************************************

class Relatorio(models.Model):
    tipo = models.CharField(max_length=50)  # Tipo do relatório
    ano = models.IntegerField()  # Ano
    escola = models.CharField(max_length=191)  # Nome da escola
    data_geracao = models.DateTimeField(auto_now_add=True)  # Data de criação
    arquivo = models.FileField(upload_to='manuals/')  # Caminho do arquivo

    def __str__(self):
        return f"{self.tipo} - {self.ano}"
# ********************************************************************************************************************************

class Escola(models.Model):
    # Dados da Unidade
    nome = models.CharField(max_length=191)  # Remova unique=True se estiver
    endereco = models.CharField(max_length=191, blank=True, null=True)  # <-- Aqui
    cep = models.CharField(max_length=9, null=True, blank=True)  # Ex.: 68356-055
    bairro = models.CharField(max_length=191, null=True, blank=True)
    cidade = models.CharField(max_length=191, default="Canaã dos Carajás")
    uf = models.CharField(max_length=2, default="PA")
    tipo = models.CharField(max_length=50, null=True, blank=True)  # Ex.: Escola, Creche
    habilitado = models.BooleanField(default=True)
    segmento = models.CharField(max_length=191, null=True, blank=True)
    zona = models.CharField(max_length=50, choices=[("Rural", "Rural"), ("Urbana", "Urbana")], default="Urbana")
    local_funcionamento = models.CharField(max_length=100, null=True, blank=True)
    ocupacao_predio = models.CharField(max_length=50, null=True, blank=True)
    compartilhado = models.BooleanField(default=False)
    codigo_compartilhado = models.CharField(max_length=50, null=True, blank=True)
    modalidade_ensino = models.CharField(max_length=191, null=True, blank=True)
    autorizacao = models.CharField(max_length=50, null=True, blank=True)
    protocolo = models.CharField(max_length=50, null=True, blank=True)
    codigo_inep = models.CharField(max_length=10, null=True, blank=True)
    cnpj = models.CharField(max_length=18, null=True, blank=True)
    fundacao = models.DateField(null=True, blank=True)
    situacao = models.CharField(max_length=50, null=True, blank=True)
    distrito = models.CharField(max_length=191, null=True, blank=True)
    dependencia_administrativa = models.CharField(max_length=50, null=True, blank=True)
    
    # Dados do Censo
    agua_potavel = models.BooleanField(default=False)
    abastecimento_agua = models.CharField(max_length=50, null=True, blank=True)
    energia = models.CharField(max_length=50, null=True, blank=True)
    esgotamento_sanitario = models.CharField(max_length=50, null=True, blank=True)
    destinacao_lixo = models.CharField(max_length=191, null=True, blank=True)
    tratamento_lixo = models.CharField(max_length=191, null=True, blank=True)
    dependencias_fisicas = models.TextField(null=True, blank=True)  # Lista separada por vírgulas
    acessibilidade = models.TextField(null=True, blank=True)  # Lista separada por vírgulas
    internet = models.BooleanField(default=False)
    internet_banda_larga = models.BooleanField(default=False)
    equipamentos_alunos = models.TextField(null=True, blank=True)
    instrumentos_pedagogicos = models.TextField(null=True, blank=True)
    colegiados = models.TextField(null=True, blank=True)
    equipamentos_ensino = models.TextField(null=True, blank=True)

    # Quantitativo
    quantidade_salas = models.IntegerField(default=0)
    quantidade_turmas = models.IntegerField(default=0)
    quantidade_professores = models.IntegerField(default=0)
    quantidade_alunos = models.IntegerField(default=0)
    capacidade_alunos = models.IntegerField(default=0)
    quantidade_secretaria = models.IntegerField(default=0)
    quantidade_servicos_gerais = models.IntegerField(default=0)
    quantidade_merendeira = models.IntegerField(default=0)
    quantidade_controladores_acesso = models.IntegerField(default=0)

    # Pedagógico
    diretor = models.CharField(max_length=191, null=True, blank=True)
    telefone_diretor = models.CharField(max_length=15, null=True, blank=True)
    email_diretor = models.EmailField(null=True, blank=True)
    vice_diretor = models.CharField(max_length=191, null=True, blank=True)
    telefone_vice_diretor = models.CharField(max_length=15, null=True, blank=True)
    email_vice_diretor = models.EmailField(null=True, blank=True)
    coordenador_pedagogico = models.CharField(
        max_length=191,
        null=True,     # permite NULL no banco de dados
        blank=True     # permite campo vazio no formulário
    )

     # Novidade: Coordenador vinculado
    coordenador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='escolas_unidade'  # 🔹 Nome único para evitar conflitos
    )



    telefone_coordenador_pedagogico = models.CharField(max_length=15, null=True, blank=True)
    email_coordenador_pedagogico = models.EmailField(null=True, blank=True)
    secretario = models.CharField(max_length=191, null=True, blank=True)
    telefone_secretario = models.CharField(max_length=15, null=True, blank=True)
    email_secretario = models.EmailField(null=True, blank=True)

    # Localização
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    # Imagem
    imagem = models.ImageField(upload_to='escolas/', blank=True, null=True)

    def __str__(self):
        return self.nome
# ********************************************************************************************************************************

# models.py

class Escolas(models.Model):
    nome = models.CharField(max_length=191)
    unidade_educacional = models.CharField(max_length=191, blank=True, null=True)
    endereco = models.CharField(max_length=191, blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    diretor = models.CharField(max_length=191, blank=True, null=True)

    codigo_inep = models.CharField(max_length=12, unique=True, verbose_name='Código INEP', blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    uf = models.CharField(
        max_length=2,
        choices=[('PA', 'Pará'), ('MA', 'Maranhão'), ('TO', 'Tocantins')],
        verbose_name='UF',
        blank=True,
        null=True
    )
    dependencia_administrativa = models.CharField(
        max_length=50,
        choices=[
            ('municipal', 'Municipal'),
            ('estadual', 'Estadual'),
            ('privada', 'Privada'),
        ],
        verbose_name='Dependência Administrativa',
        blank=True,
        null=True
    )
    ano = models.PositiveIntegerField(verbose_name="Ano de Referência", blank=True, null=True)

    coordenador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='escolas_geral'  # 🔹 Nome único para evitar conflitos
    )

    def __str__(self):
        return f"{self.nome} ({self.codigo_inep or 'sem INEP'})"




# ********************************************************************************************************************************

class Membro(models.Model):
    nome = models.CharField(max_length=191)
    funcao = models.CharField(max_length=191, null=True, blank=True)
    data_admissao = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.nome
# ********************************************************************************************************************************

class Caixa(models.Model):
    descricao = models.CharField(max_length=191)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_movimento = models.DateField()

    def __str__(self):
        return self.descricao
# ********************************************************************************************************************************

from django.db import models

class Certidao(models.Model):
    nome = models.CharField(max_length=191)
    descricao = models.TextField()
    data_emissao = models.DateField(auto_now_add=True)
    arquivo = models.FileField(upload_to='certidoes/', null=True, blank=True)  # Novo campo

    def __str__(self):
        return self.nome

# ********************************************************************************************************************************

class Legislacao(models.Model):
    titulo = models.CharField(max_length=191)
    descricao = models.TextField()
    data_publicacao = models.DateField()
    categoria = models.CharField(max_length=100)

    def __str__(self):
        return self.titulo
# ********************************************************************************************************************************

class InscricaoPlanetario(models.Model):
    nome = models.CharField(max_length=200)
    email = models.EmailField()
    telefone = models.CharField(max_length=15)
    atividade = models.CharField(max_length=200)
    mensagem = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome
# ********************************************************************************************************************************

class Imagem(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    imagem = models.ImageField(upload_to='galeria/')
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
# ********************************************************************************************************************************

class Conteudo(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    imagem = models.ImageField(upload_to='conteudos/', blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    ultima_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo
# ********************************************************************************************************************************

class Evento(models.Model):
    titulo = models.CharField(max_length=200)
    data = models.DateField()
    local = models.CharField(max_length=300)
    descricao = models.TextField(blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
# ********************************************************************************************************************************

# class Usuario(models.Model):
#     nome = models.CharField(max_length=200)
#     email = models.EmailField(unique=True)
#     senha = models.CharField(max_length=200)
#     data_registro = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.nome
# ********************************************************************************************************************************

class Funcionario(models.Model):
    nome_completo = models.CharField(max_length=191)
    rg = models.CharField(max_length=50)
    cpf = models.CharField(max_length=25, unique=True)
    telefone = models.CharField(max_length=15)
    email = models.EmailField(max_length=191)
    cargo = models.CharField(max_length=100)
    lotacao = models.CharField(max_length=100)  # Lotação refers to the work location or department

    def __str__(self):
        return self.nome_completo
 # ********************************************************************************************************************************   

class Usuario(AbstractUser):
    nome_completo = models.CharField(max_length=191)
    cpf = models.CharField(max_length=25, unique=True)  # CPF único
    email = models.EmailField(unique=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_nascimento = models.DateField()  # Campo de data de nascimento
    telefone = models.CharField(max_length=15, null=True, blank=True)  # Telefone do Candidato
    telefone_contato_2 = models.CharField(max_length=15, null=True, blank=True)  # Telefone de Contato 2
    telefone_secundario = models.CharField(max_length=15, null=True, blank=True)
    endereco = models.CharField(max_length=191, null=True, blank=True)  # Endereço
    bairro = models.CharField(max_length=100, null=True, blank=True)  # Bairro
    ponto_referencia = models.CharField(max_length=191, null=True, blank=True)  # Ponto de Referência
    maior_de_18 = models.BooleanField(default=False)  # O Candidato é maior de 18 anos?

    nome = models.CharField(max_length=191)
    senha = models.CharField(max_length=128)  # Certifique-se de hashar senhas

    # New fields
    responsavel_legal = models.CharField(max_length=191, null=True, blank=True)
    tipo_responsavel = models.CharField(max_length=50, choices=[
        ('Mãe', 'Mãe'),
        ('Pai', 'Pai'),
        ('Responsável Legal', 'Responsável Legal')
    ], null=True, blank=True)

    # New field for special needs
    necessidade_especial = models.BooleanField(default=False)
    tipo_necessidade_especial = models.CharField(max_length=50, choices=[
        ('Baixa Visão', 'Baixa Visão'),
        ('Cegueira', 'Cegueira'),
        ('Auditiva', 'Auditiva'),
        ('Deficiência Física', 'Deficiência Física'),
        ('Deficiência Intelectual', 'Deficiência Intelectual')
    ], null=True, blank=True)

    # New field for Etapa da Matrícula
    etapa_matricula = models.CharField(max_length=50, choices=[
        ('Etapa I Ensino Fundamental I(1º 2º 3º ano)', 'Etapa I Ensino Fundamental I(1º 2º 3º ano)'),
        ('Etapa II Ensino Fundamental I(4º 5º ano)', 'Etapa II Ensino Fundamental I(4º 5º ano)'),
        ('Etapa III', 'Etapa III')
    ], null=True, blank=True)

    nome_responsavel = models.CharField(max_length=191, null=True, blank=True)  # Nome do Responsável Legal
    tipo_responsavel = models.CharField(max_length=50, choices=[('Mãe', 'Mãe'), ('Pai', 'Pai'), ('Responsável Legal', 'Responsável Legal')], null=True, blank=True)  # Tipo de Responsável Legal
    possui_necessidade_especial = models.BooleanField(default=False)  # Possui alguma necessidade especial?
    necessidade_especial_detalhe = models.CharField(
        max_length=50, 
        choices=[
            ('Baixa Visão', 'Baixa Visão'), 
            ('Cegueira', 'Cegueira'), 
            ('Auditiva', 'Auditiva'), 
            ('Deficiência Física', 'Deficiência Física'), 
            ('Deficiência Intelectual', 'Deficiência Intelectual')
        ],
        null=True, blank=True
    )  # Caso possua, favor assinalar
    turno_disponivel = models.CharField(
        max_length=20, 
        choices=[
            ('Manhã', 'Manhã'), 
            ('Tarde', 'Tarde'), 
            ('Noite', 'Noite')
        ],
        null=True, blank=True
    )  # Turno de Estudo Disponível
    etapa_pretendida = models.CharField(
        max_length=100,
        choices=[
            ('Etapa I Ensino Fundamental I (1º 2º 3º ano)', 'Etapa I Ensino Fundamental I (1º 2º 3º ano)'),
            ('Etapa II Ensino Fundamental I (4º 5º ano)', 'Etapa II Ensino Fundamental I (4º 5º ano)'),
            ('Etapa III Ensino Fundamental II', 'Etapa III Ensino Fundamental II')
        ],
        null=True, blank=True
    )  # Etapa pretendida para a matrícula
    
    # Related fields from AbstractUser
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_usuario_set',  # Name to avoid conflict
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_usuario_permissions_set',  # Name to avoid conflict
        blank=True
    )

    def __str__(self):
        return self.nome_completo
#**********************************************************************************************************
class Disciplina(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome
#**********************************************************************************************************

class Inscricao(models.Model):
    #usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inscricoes_usuario')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    candidato = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name="inscricao")
    data_inscricao = models.DateTimeField(auto_now_add=True)
    responsavel_legal = models.CharField(max_length=191, null=True, blank=True)
    tipo_responsavel = models.CharField(max_length=100, null=True, blank=True)
    telefone = models.CharField(max_length=15, null=True, blank=True)
    telefone_secundario = models.CharField(max_length=15, null=True, blank=True)
    endereco = models.CharField(max_length=191, null=True, blank=True)
    bairro = models.ForeignKey('semedapp.Bairro', on_delete=models.CASCADE)
    cidade = models.CharField(max_length=191, null=True, blank=True)  # Optional field
    ponto_referencia = models.CharField(max_length=191, null=True, blank=True)
    necessidade_especial = models.BooleanField(default=False)
    tipo_necessidade_especial = models.CharField(max_length=100, null=True, blank=True)
    turno_disponivel = models.CharField(max_length=100, null=True, blank=True)
    etapa_pretendida = models.CharField(max_length=191, null=True, blank=True)
    prova_realizada = models.BooleanField(default=False)  # Example field definition
    nota = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Add nota field
    aprovado = models.BooleanField(default=False)  # Add this field
    cpf_responsavel = models.CharField(max_length=11, null=True, blank=True)  # Novo campo
    rg_responsavel = models.CharField(max_length=12, null=True, blank=True)   # Novo campo
    disciplinas_aprovadas = models.ManyToManyField(Disciplina, related_name='inscricoes_aprovadas', blank=True)
    nota_prova = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Exemplo de campo de nota
    ativo = models.BooleanField(default=True)  # Define o status como ativo por padrão


    LOCAL_EXAME_CHOICES = [
        ('CMEJA', 'CMEJA Jose de Deus Andrade'),
        ('SEBASTIAO_AGRIPINO', 'EMEF Sebastião Agripino da Silva'),
        ('MARIA_LOURDES', 'EMEF Maria de Lourdes Rocha Rodrigues'),
        ('ADELAIDE_MOLINARI', 'EMEIF Adelaide Molinari'),
        ('RAIMUNDO_OLIVEIRA', 'EMEIF Raimundo de Oliveira'),
        ('TEOTONIO_VILELA', 'EMEIF Teotonio Vilela'),
    ]
    local_exame = models.CharField(max_length=30, choices=LOCAL_EXAME_CHOICES, default='CMEJA')

    ESCOLA_CHOICES = [
        ('NAO_ESTUDANDO', 'NÃO ESTOU ESTUDANDO EM 2024'),
        ('CMEJA_JOSE_DE_DEUS_ANDRADE', 'CMEJA JOSÉ DE DEUS ANDRADE'),
        ('EMEIF_ADELAIDE_MOLINARI', 'EMEIF ADELAIDE MOLINARI'),
        ('EMEIF_CARLOS_HENRIQUE', 'EMEIF CARLOS HENRIQUE'),
        ('EMEIF_JUSCELINO_KUBITSCHEK', 'EMEIF JUSCELINO KUBITSCHEK'),
        ('EMEIF_MAGALHAES_BARATA', 'EMEIF MAGALHÃES BARATA'),
        ('EMEIF_RAIMUNDO_OLIVEIRA', 'EMEIF RAIMUNDO DE OLIVEIRA'),
        ('EMEIF_TEOTONIO_VILELA', 'EMEIF TEOTÔNIO VILELA'),
        ('EMEF_BENEDITA_TORRES', 'EMEF BENEDITA TORRES'),
        ('EMEF_SEBASTIAO_AGRIPINO', 'EMEF SEBASTIÃO AGRIPINO DA SILVA'),
        ('EMEF_ALEXSANDRO_NUNES', 'EMEF ALEXSANDRO NUNES DE SOUZA GOMES'),
        ('EMEF_CARMELO_MENDES', 'EMEF CARMELO MENDES DA SILVA'),
        ('EMEB_LUIS_CARLOS_PRESTES', 'EMEB LUÍS CARLOS PRESTES'),
        ('EMEF_JOAO_NELSON', 'EMEF JOÃO NELSON DOS PRAZERES HENRIQUES'),
        ('EMEF_MARIA_DE_LOURDES', 'EMEF MARIA DE LOURDES ROCHA RODRIGUES'),
        ('EMEB_RONILTON_ARIDAL', 'EMEB RONILTON ARIDAL DA SILVA GRILO'),
        ('EMEB_GERCINO_CORREA', 'EMEB GERCINO CORREA'),
        ('EMEIF_TANCREDO', 'EMEIF TANCREDO DE ALMEIDA NEVES'),
        ('EMEIF_FRANCISCA_ROMANA', 'EMEIF FRANCISCA ROMANA'),
    ]

    local_exame = models.CharField(
        max_length=30,
        choices=LOCAL_EXAME_CHOICES,
        default='CMEJA',
        verbose_name='Local de realização das provas'
    )

    escola = models.CharField(
        max_length=50,
        choices=ESCOLA_CHOICES,
        default='NAO_ESTUDANDO',
        verbose_name='Nome da escola onde está matriculado em 2024'
    )

    dia_realizacao_prova = models.DateField(default='2024-12-01',verbose_name='Dia de realização da prova')

    # Field for "Deseja realizar a prova de todas as disciplinas?"
    PROVA_TODAS_DISCIPLINAS_CHOICES = [('Sim', 'Sim'),('Não', 'Não')]

    prova_todas_disciplinas = models.CharField(
        max_length=3,
        choices=PROVA_TODAS_DISCIPLINAS_CHOICES,
        default='Não',
        verbose_name="Deseja realizar a prova de todas as disciplinas?"
    )

    # Field for selected disciplines if "Não" is chosen
    DISCIPLINAS_CHOICES = [
        ('Matemática', 'Matemática'),
        ('Ciências', 'Ciências'),
        ('Arte', 'Arte'),
        ('Educação Física', 'Educação Física'),
        ('História', 'História'),
        ('Geografia', 'Geografia'),
        ('Língua Portuguesa', 'Língua Portuguesa'),
        ('Inglês', 'Inglês'),
    ]

    disciplinas = models.ManyToManyField(Disciplina, related_name='inscricoes_disciplinas', blank=True)

    EXAME_SUPLETIVO_CHOICES = [('Sim', 'Sim'),('Não', 'Não')]

    exame_supletivo = models.CharField(
        max_length=3, 
        choices=EXAME_SUPLETIVO_CHOICES,
        default='Não',  # Assuming 'Não' is the default choice
        verbose_name="Já fez a prova do exame supletivo anteriormente, ofertado pelo município de Canaã dos Carajás?"
    )

    # New Status Field
    STATUS_CHOICES = [('inscrito', 'Inscrito'),('approved', 'Aprovado'),('analise', 'Analise'),]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Inscrito')

    def __str__(self):
        return f"Inscrição de {self.candidato.nome_completo}"
    
    @property
    def formatted_id(self):
        return str(self.id).zfill(4)  # Isso vai adicionar zeros à esquerda até 4 dígitos

#**********************************************************************************************************

class Candidato(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='candidato')
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nome_completo = models.CharField(max_length=191)
    nome = models.CharField(max_length=191)
    email = models.EmailField()
    cpf = models.CharField(max_length=25)  # Add input mask for CPF in the form later
    data_nascimento = models.DateField()
    maior_de_18 = models.BooleanField()  # Yes or No (Checkbox)
    nome_responsavel = models.CharField(max_length=191, blank=True, null=True)
    
    TIPO_RESPONSAVEL_CHOICES = [
        ('mae', 'Mãe'),
        ('pai', 'Pai'),
        ('responsavel_legal', 'Responsável Legal'),
    ]
    tipo_responsavel = models.CharField(max_length=20, choices=TIPO_RESPONSAVEL_CHOICES, blank=True, null=True)
    
    telefone = models.CharField(max_length=15)
    telefone_2 = models.CharField(max_length=15, blank=True, null=True)
    endereco = models.CharField(max_length=191)
    bairro = models.CharField(max_length=100)
    ponto_referencia = models.CharField(max_length=191, blank=True, null=True)
    
    possui_necessidade_especial = models.BooleanField()  # Checkbox for Yes or No
    
    NECESSIDADE_ESPECIAL_CHOICES = [
        ('baixa_visao', 'Baixa visão'),
        ('cegueira', 'Cegueira'),
        ('auditiva', 'Auditiva'),
        ('fisica', 'Deficiência Física'),
        ('intelectual', 'Deficiência Intelectual'),
    ]
    necessidade_especial = models.CharField(max_length=50, choices=NECESSIDADE_ESPECIAL_CHOICES, blank=True, null=True)

    TURNO_CHOICES = [
        ('manha', 'Manhã'),
        ('tarde', 'Tarde'),
        ('noite', 'Noite'),
    ]
    turno_disponivel = models.CharField(max_length=10, choices=TURNO_CHOICES)
    
    ETAPA_CHOICES = [
        ('etapa_i', 'Etapa I Ensino Fundamental I (1º 2º 3º ano)'),
        ('etapa_ii', 'Etapa II Ensino Fundamental I (4º 5º ano)'),
        ('etapa_iii', 'Etapa III Ensino Fundamental II'),
    ]
    etapa_pretendida = models.CharField(max_length=50, choices=ETAPA_CHOICES)

    def __str__(self):
        return self.nome
#**********************************************************************************************************

class School(models.Model):
    name = models.CharField(max_length=191)
    neighborhood = models.CharField(max_length=191)
    address = models.CharField(max_length=191)
    cep = models.CharField(max_length=10)  # Adding CEP field

    def __str__(self):
        return self.name
#**********************************************************************************************************
class Bairro(models.Model):
    nome = models.CharField(max_length=191)
    logradouro_nome = models.CharField(max_length=191)
    bairro_distrito = models.CharField(max_length=191)
    cep = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.logradouro_nome} - {self.bairro_distrito}'
#**********************************************************************************************************

#**********************************************************************************************************
# class Disciplina(models.Model):
#     nome = models.CharField(max_length=100)

#     def __str__(self):
#         return self.nome
#**********************************************************************************************************
class Prova(models.Model):
    nome = models.CharField(max_length=191)
    data = models.DateField()
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.nome
#**********************************************************************************************************

class DiagnoseInicProfPort(models.Model):
    item = models.CharField(max_length=50)
    habilidade = models.CharField(max_length=191)
    descricao_habilidade = models.TextField(null=True, blank=True)  # Campo para armazenar a des

    # Campos para os números dos professores
    professor_401 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_403 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_404 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_406 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_408 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_409 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_410 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_413 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_414 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_415 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_417 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_421 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_423 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_426 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_428 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_429 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_430 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_431 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_432 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_433 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_434 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_435 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_436 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_437 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_438 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_439 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_441 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_442 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_447 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_451 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_471 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])

    def __str__(self):
        return f'Item {self.item} - {self.habilidade}'
#**********************************************************************************************************

class DiagnoseAlunoMatematica(models.Model):
    SERIE_CHOICES = [
        ('3º', '3º Ano'),
        ('4º', '4º Ano'),
        ('5º', '5º Ano'),
        ('6º', '6º Ano'),
    ]
    
    tipo_usuario = models.CharField(max_length=20, choices=[('aluno', 'Aluno'), ('professor', 'Professor')])
    serie = models.CharField(max_length=10, choices=SERIE_CHOICES)
    habilidade = models.CharField(max_length=100)
    descricao_habilidade = models.TextField(null=True, blank=True)  # Campo para a descrição da habilidade
    acerto = models.FloatField()
    erro = models.FloatField()

    def clean(self):
        if not (0 <= self.acerto <= 1):
            raise ValidationError({'acerto': 'O valor de acerto deve estar entre 0 e 1.'})
        if not (0 <= self.erro <= 1):
            raise ValidationError({'erro': 'O valor de erro deve estar entre 0 e 1.'})

    def __str__(self):
        return f"{self.serie} - {self.habilidade}"

############################################################################################################################

class DiagnoseAlunoPortugues(models.Model):
    SERIE_CHOICES = [
        ('3º', '3º Ano'),
        ('4º', '4º Ano'),
        ('5º', '5º Ano'),
        ('6º', '6º Ano'),
    ]
    
    tipo_usuario = models.CharField(max_length=20, choices=[('aluno', 'Aluno'), ('professor', 'Professor')])
    serie = models.CharField(max_length=10, choices=SERIE_CHOICES)
    habilidade = models.CharField(max_length=100)
    descricao_habilidade = models.TextField(null=True, blank=True)  # Campo para a descrição da habilidade
    acerto = models.FloatField()
    erro = models.FloatField()

    def clean(self):
        if not (0 <= self.acerto <= 1):
            raise ValidationError({'acerto': 'O valor de acerto deve estar entre 0 e 1.'})
        if not (0 <= self.erro <= 1):
            raise ValidationError({'erro': 'O valor de erro deve estar entre 0 e 1.'})

    def __str__(self):
        return f"{self.serie} - {self.habilidade}"
###################################################################################################################

class HabilidadePortugues(models.Model):
    # Campos para habilidades de Português
    habilidade = models.CharField(max_length=100)
    topico = models.CharField(max_length=100)  # Campo para o tópico da habilidade
    descricao = models.TextField()
    serie = models.IntegerField()  # Série correspondente à habilidade
    tipo_ano = models.CharField(
        max_length=10,
        choices=[('inicial', 'Anos Iniciais'), ('final', 'Anos Finais')],
        default='inicial'
    )
    acertos = models.FloatField(default=0.0)  # Percentual de acertos
    erros = models.FloatField(default=0.0)    # Percentual de erros

    def __str__(self):
        return f"{self.habilidade} - {self.descricao[:30]}"  # Retorno amigável no admin
############################################################################################################################


############################################################################################################################
    
class HabilidadeMatematica(models.Model):
    # Campos para habilidades de Matemática
    habilidade = models.CharField(max_length=100)
    topico = models.CharField(max_length=100)  # Campo para o tópico da habilidade
    descricao = models.TextField()
    serie = models.IntegerField()  # Série correspondente à habilidade
    tipo_ano = models.CharField(
        max_length=10,
        choices=[('inicial', 'Anos Iniciais'), ('final', 'Anos Finais')],
        default='inicial'
    )
    acertos = models.FloatField(default=0.0)  # Percentual de acertos
    erros = models.FloatField(default=0.0)    # Percentual de erros

    def __str__(self):
        return f"{self.habilidade} - {self.descricao[:30]}"  # Retorno amigável no admin
############################################################################################################################

class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # Add other profile fields here


    def __str__(self):
        return self.user.username
############################################################################################################################

class PortuguesProfessores(models.Model):
    item = models.PositiveIntegerField()  # Coluna "Item"
    habilidade = models.CharField(max_length=10)  # Coluna "Habilidade"
    
    # Colunas representando as classes, use BooleanField para armazenar 1 ou 0
    _401 = models.BooleanField(default=False)
    _403 = models.BooleanField(default=False)
    _404 = models.BooleanField(default=False)
    _406 = models.BooleanField(default=False)
    _408 = models.BooleanField(default=False)
    _409 = models.BooleanField(default=False)
    _410 = models.BooleanField(default=False)
    _413 = models.BooleanField(default=False)
    _414 = models.BooleanField(default=False)
    _415 = models.BooleanField(default=False)
    _417 = models.BooleanField(default=False)
    _421 = models.BooleanField(default=False)
    _423 = models.BooleanField(default=False)
    _426 = models.BooleanField(default=False)
    _428 = models.BooleanField(default=False)
    _429 = models.BooleanField(default=False)
    _430 = models.BooleanField(default=False)
    _431 = models.BooleanField(default=False)
    _432 = models.BooleanField(default=False)
    _433 = models.BooleanField(default=False)
    _434 = models.BooleanField(default=False)
    _435 = models.BooleanField(default=False)
    _436 = models.BooleanField(default=False)
    _437 = models.BooleanField(default=False)
    _438 = models.BooleanField(default=False)
    _439 = models.BooleanField(default=False)
    _441 = models.BooleanField(default=False)
    _442 = models.BooleanField(default=False)
    _447 = models.BooleanField(default=False)
    _451 = models.BooleanField(default=False)
    _471 = models.BooleanField(default=False)
    
    def __str__(self):
        return f'Item {self.item} - Habilidade {self.habilidade}'
############################################################################################################################

# class DiagnoseInicProfPort(models.Model):
#     item = models.PositiveIntegerField()
#     habilidade = models.CharField(max_length=10)
    
#     # Campos para os números dos professores
#     professor_401 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
#     professor_403 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
#     professor_404 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
#     professor_406 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
#     professor_408 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
#     professor_409 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
#     professor_410 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
#     professor_413 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
#     professor_414 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
#     professor_415 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
#     professor_417 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
#     professor_421 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
#     professor_423 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
#     professor_426 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
#     professor_428 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
#     professor_429 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
#     professor_430 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
#     professor_431 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
#     professor_432 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
#     professor_433 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
#     professor_434 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
#     professor_435 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
#     professor_436 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
#     professor_437 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
#     professor_438 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
#     professor_439 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
#     professor_441 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
#     professor_442 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
#     professor_447 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
#     professor_451 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
#     professor_471 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])

#     def __str__(self):
#         return f'Item {self.item} - {self.habilidade}'
############################################################################################################################

class Student(models.Model):
    numero_matricula = models.CharField(max_length=20, unique=True)
    nome_completo = models.CharField(max_length=191)
    escola = models.CharField(max_length=191)
    data_nascimento = models.DateField()
    sexo = models.CharField(max_length=10)
    turno = models.CharField(max_length=20)
    telefone = models.CharField(max_length=20)
    nivel_escolaridade = models.CharField(max_length=50)
    endereco = models.CharField(max_length=191)
    bairro = models.CharField(max_length=100)
    cep = models.CharField(max_length=10)
    codigo_rota = models.CharField(max_length=20)
    email_responsavel = models.EmailField()
    cpf_responsavel = models.CharField(max_length=20)
    nome_responsavel = models.CharField(max_length=191)
    parentesco = models.CharField(max_length=50)
    telefone_responsavel = models.CharField(max_length=20)
    responsavel_legal = models.CharField(max_length=10)

    def __str__(self):
        return self.nome_completo
############################################################################################################################

from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError("O campo Nome de Usuário é obrigatório")
        if not email:
            raise ValueError("O campo E-mail é obrigatório")
        
        # Certificar-se de que o e-mail esteja em minúsculas
        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)

        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)  # Hash da senha
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser precisa ter is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser precisa ter is_superuser=True.")

        return self.create_user(username, email, password, **extra_fields)

############################################################################################################################

class UploadedFile(models.Model):
    name = models.CharField(max_length=191)
    file = models.FileField(upload_to='uploads/')
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def download_url(self):
        return self.file.urla
############################################################################################################################

############################################################################################################################
## Indicadores
############################################################################################################################

from django.core.validators import RegexValidator

class IndicadoresTransporte(models.Model):
    # Choices para os campos
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    ]

    TURNO_CHOICES = [
        ('Matutino', 'Matutino'),
        ('Vespertino', 'Vespertino'),
        ('Noturno', 'Noturno'),
        ('Integral', 'Integral'),
    ]

    PARENTESCO_CHOICES = [
        ('Pai', 'Pai'),
        ('Mãe', 'Mãe'),
        ('Tio/Tia', 'Tio/Tia'),
        ('Avô/Avó', 'Avô/Avó'),
        ('Outro', 'Outro'),
    ]

    # Campos
    numero_matricula = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Número de Matrícula"
    )
    nome_completo = models.CharField(
        max_length=191,
        verbose_name="Nome Completo"
    )
    escola = models.CharField(
        max_length=191,
        verbose_name="Escola"
    )
    data_nascimento = models.DateField(
        verbose_name="Data de Nascimento"
    )
    sexo = models.CharField(
        max_length=1,
        choices=SEXO_CHOICES,
        verbose_name="Sexo"
    )
    turno = models.CharField(
        max_length=20,
        choices=TURNO_CHOICES,
        verbose_name="Turno"
    )
    telefone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name="Telefone",
        validators=[
            RegexValidator(
                regex=r'^\(\d{2}\) \d{4,5}-\d{4}$',
                message="O telefone deve estar no formato (XX) XXXXX-XXXX."
            )
        ]
    )
    nivel_escolaridade = models.CharField(
        max_length=100,
        verbose_name="Nível de Escolaridade"
    )
    endereco = models.CharField(
        max_length=191,
        verbose_name="Endereço"
    )
    bairro = models.CharField(
        max_length=100,
        verbose_name="Bairro"
    )
    cep = models.CharField(
        max_length=10,
        verbose_name="CEP",
        validators=[
            RegexValidator(
                regex=r'^\d{5}-\d{3}$',
                message="O CEP deve estar no formato XXXXX-XXX."
            )
        ]
    )
    codigo_rota = models.CharField(
        max_length=50,
        verbose_name="Código da Rota"
    )
    email_responsavel = models.EmailField(
        verbose_name="E-mail do Responsável"
    )
    cpf_responsavel = models.CharField(
        max_length=14,
        verbose_name="CPF do Responsável",
        validators=[
            RegexValidator(
                regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$',
                message="O CPF deve estar no formato XXX.XXX.XXX-XX."
            )
        ]
    )
    nome_responsavel = models.CharField(
        max_length=191,
        verbose_name="Nome do Responsável"
    )
    parentesco = models.CharField(
        max_length=50,
        choices=PARENTESCO_CHOICES,
        verbose_name="Parentesco"
    )
    telefone_responsavel = models.CharField(
        max_length=15,
        verbose_name="Telefone do Responsável",
        validators=[
            RegexValidator(
                regex=r'^\(\d{2}\) \d{4,5}-\d{4}$',
                message="O telefone deve estar no formato (XX) XXXXX-XXXX."
            )
        ]
    )
    responsavel_legal = models.BooleanField(
        default=False,
        verbose_name="Responsável Legal"
    )

    # String de representação
    def __str__(self):
        return f"{self.numero_matricula} - {self.nome_completo}"

    # Meta informações
    class Meta:
        verbose_name = "Indicador de Transporte"
        verbose_name_plural = "Indicadores de Transporte"
        db_table = "semedapp_indicadorestransporte"


############################################################################################################################
## Pedagógico
############################################################################################################################

# class Funcionario(models.Model):
#     nome_completo = models.CharField(max_length=191)
#     rg = models.CharField(max_length=20)
#     cpf = models.CharField(max_length=25, unique=True)
#     telefone = models.CharField(max_length=15)
#     email = models.EmailField(max_length=191)
#     cargo = models.CharField(max_length=100)
#     lotacao = models.CharField(max_length=100)  # Lotação refers to the work location or department

#     def __str__(self):
#         return self.nome_completo
#**********************************************************************************************************
class RegimentoCadastro(models.Model):
    TITULO_CHOICES = [
        ('TÍTULO I', 'TÍTULO I - DAS DISPOSIÇÕES PRELIMINARES'),
        ('TÍTULO II', 'TÍTULO II - DAS FINALIDADES E OBJETIVOS DA EDUCAÇÃO BÁSICA'),
        ('TÍTULO III', 'TÍTULO III - DA ORGANIZAÇÃO DA INSTITUIÇÃO'),
        ('TÍTULO IV', 'TÍTULO IV - DOS PAIS OU RESPONSÁVEIS'),
        ('TÍTULO V', 'TÍTULO V - DAS DEMAIS ORGANIZAÇÃO DA INSTITUIÇÃO'),
        ('TÍTULO VI', 'TÍTULO VI - DA ADMINISTRAÇÃO PESSOAL'),
        ('TÍTULO VII', 'TÍTULO VII - DA ORGANIZAÇÃO DIDÁTICA - PEDAGÓGICA'),
        ('TÍTULO VIII', 'TÍTULO VIII - DO REGIME DE FUNCIONAMENTO'),
        ('TÍTULO IX', 'TÍTULO IX - DA VERIFICAÇÃO DO RENDIMENTO E AVALIAÇÃO'),
        ('TÍTULO X', 'TÍTULO X - DO REGIME DISCIPLINAR'),
        ('TÍTULO XI', 'TÍTULO XI - DAS DISPOSIÇÕES GERAIS E TRANSITÓRIAS'),
        # Adicione os outros títulos conforme necessário
    ]

    CAPITULO_CHOICES = [
        ('CAPÍTULO ÚNICO', 'CAPÍTULO ÚNICO - DOS PRINCÍPIOS E FINS DA EDUCAÇÃO'),
        ('CAPÍTULO I', 'CAPÍTULO I - DA EDUCAÇÃO INFANTIL'),
        ('CAPÍTULO II', 'CAPÍTULO II - DO ENSINO FUNDAMENTAL'),
        ('CAPÍTULO III', 'CAPÍTULO III - DA EDUCAÇÃO DE JOVENS E ADULTOS'),
        # Add more as necessary, depending on the `titulo` selected
    ]
    
    TIPO_ALTERACAO_CHOICES = [
        ('supressao', 'Supressão'),
        ('insercao', 'Inserção'),
        ('edicao', 'Alteração'),
        ('exclusao', 'Exclusão'),
    ]

    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('aprovado', 'Aprovado'),
        ('rejeitado', 'Rejeitado'),
    ]
    
    titulo = models.CharField(max_length=191)
    capitulo = models.CharField(max_length=191)
    tipo_alteracao = models.CharField(max_length=50)
    justificativa = models.TextField()
    nome_completo = models.CharField(max_length=191)
    email = models.EmailField()
    cpf = models.CharField(max_length=25)
    telefone = models.CharField(max_length=20)
    cargo = models.CharField(max_length=191)
    lotacao = models.CharField(max_length=191)
    observacoes_adicionais = models.TextField(null=True, blank=True)
    data_submissao = models.DateTimeField(auto_now_add=True)  # Automatic timestamp on creation
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pendente')

    def __str__(self):
        return self.titulo
#**********************************************************************************************************

class Regimento(models.Model):
    titulo = models.CharField(max_length=200)
    capitulo = models.CharField(max_length=200)
    tipo_alteracao = models.CharField(max_length=100)
    justificativa = models.TextField()
    nome_completo = models.CharField(max_length=200)
    cpf = models.CharField(max_length=25)
    email = models.EmailField()
    telefone = models.CharField(max_length=15)
    cargo = models.CharField(max_length=100)
    lotacao = models.CharField(max_length=100)
    observacoes_adicionais = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.titulo
#**********************************************************************************************************

class Registro(models.Model):
    titulo = models.CharField(max_length=191)
    capitulo = models.CharField(max_length=191)
    tipo_alteracao = models.CharField(max_length=100, choices=[('insercao', 'Inserção'), ('alteracao', 'Alteração'), ('supressao', 'Supressão'), ('exclusao', 'Exclusão')])
    justificativa = models.TextField()
    nome_completo = models.CharField(max_length=191)
    email = models.EmailField()
    cpf = models.CharField(max_length=25)  # Mascara de CPF pode ser aplicada no frontend
    telefone = models.CharField(max_length=15)
    cargo = models.CharField(max_length=191)
    lotacao = models.CharField(max_length=191)
    observacoes_adicionais = models.TextField(blank=True, null=True)
    data_submissao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
#**********************************************************************************************************

class SemedAppRegimentoCadastro(models.Model):
    titulo = models.CharField(max_length=191)
    capitulo = models.CharField(max_length=191, null=True, blank=True)  # Certifique-se de que este campo está definido
    tipo_alteracao = models.CharField(max_length=191)
    nome_completo = models.CharField(max_length=191)
    email = models.EmailField()
    cpf = models.CharField(max_length=25)
    telefone = models.CharField(max_length=20)
    cargo = models.CharField(max_length=191)
    lotacao = models.CharField(max_length=191)
    data_submissao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)
#**********************************************************************************************************

class HabilidadeProf(models.Model):
    item = models.IntegerField()
    habilidade = models.CharField(max_length=191)
    turma_401 = models.IntegerField(default=0)
    turma_403 = models.IntegerField(default=0)
    turma_404 = models.IntegerField(default=0)
    turma_406 = models.IntegerField(default=0)
    turma_408 = models.IntegerField(default=0)
    turma_409 = models.IntegerField(default=0)
    turma_410 = models.IntegerField(default=0)
    turma_413 = models.IntegerField(default=0)
    turma_414 = models.IntegerField(default=0)
    turma_415 = models.IntegerField(default=0)
    turma_417 = models.IntegerField(default=0)
    turma_421 = models.IntegerField(default=0)
    turma_423 = models.IntegerField(default=0)
    turma_426 = models.IntegerField(default=0)
    turma_428 = models.IntegerField(default=0)
    turma_429 = models.IntegerField(default=0)
    turma_430 = models.IntegerField(default=0)
    turma_431 = models.IntegerField(default=0)
    turma_432 = models.IntegerField(default=0)
    turma_433 = models.IntegerField(default=0)
    turma_434 = models.IntegerField(default=0)
    turma_435 = models.IntegerField(default=0)
    turma_436 = models.IntegerField(default=0)
    turma_437 = models.IntegerField(default=0)
    turma_438 = models.IntegerField(default=0)
    turma_439 = models.IntegerField(default=0)
    turma_441 = models.IntegerField(default=0)
    turma_442 = models.IntegerField(default=0)
    turma_447 = models.IntegerField(default=0)
    turma_451 = models.IntegerField(default=0)
    turma_471 = models.IntegerField(default=0)

    def calcular_acertos(self):
        return sum([
            self.turma_401, self.turma_403, self.turma_404, self.turma_406,
            self.turma_408, self.turma_409, self.turma_410, self.turma_413,
            self.turma_414, self.turma_415, self.turma_417, self.turma_421,
            self.turma_423, self.turma_426, self.turma_428, self.turma_429,
            self.turma_430, self.turma_431, self.turma_432, self.turma_433,
            self.turma_434, self.turma_435, self.turma_436, self.turma_437,
            self.turma_438, self.turma_439, self.turma_441, self.turma_442,
            self.turma_447, self.turma_451, self.turma_471
        ])

    def calcular_erros(self):
        total_campos = 31  # Atualize para o número total de campos
        return total_campos - self.calcular_acertos()

#**********************************************************************************************************

class HabilidadeProfAnosFinais(models.Model):
    item = models.IntegerField()
    habilidade = models.CharField(max_length=191)
    
    # Campos para as turmas
    turma_101 = models.IntegerField(default=0)
    turma_102 = models.IntegerField(default=0)
    turma_103 = models.IntegerField(default=0)
    turma_104 = models.IntegerField(default=0)
    turma_105 = models.IntegerField(default=0)
    turma_106 = models.IntegerField(default=0)
    turma_107 = models.IntegerField(default=0)
    turma_109 = models.IntegerField(default=0)
    turma_110 = models.IntegerField(default=0)
    turma_112 = models.IntegerField(default=0)
    turma_114 = models.IntegerField(default=0)
    turma_117 = models.IntegerField(default=0)
    turma_119 = models.IntegerField(default=0)
    turma_120 = models.IntegerField(default=0)
    turma_121 = models.IntegerField(default=0)
    turma_124 = models.IntegerField(default=0)
    turma_126 = models.IntegerField(default=0)
    turma_128 = models.IntegerField(default=0)
    turma_129 = models.IntegerField(default=0)
    turma_130 = models.IntegerField(default=0)
    turma_131 = models.IntegerField(default=0)
    turma_134 = models.IntegerField(default=0)
    turma_135 = models.IntegerField(default=0)
    turma_137 = models.IntegerField(default=0)
    turma_138 = models.IntegerField(default=0)
    turma_139 = models.IntegerField(default=0)
    turma_140 = models.IntegerField(default=0)
    turma_142 = models.IntegerField(default=0)
    turma_143 = models.IntegerField(default=0)
    turma_144 = models.IntegerField(default=0)
    turma_145 = models.IntegerField(default=0)
    turma_146 = models.IntegerField(default=0)
    turma_147 = models.IntegerField(default=0)
    turma_171 = models.IntegerField(default=0)

    def calcular_acertos(self):
        return sum([
            self.turma_101, self.turma_102, self.turma_103, self.turma_104,
            self.turma_105, self.turma_106, self.turma_107, self.turma_109,
            self.turma_110, self.turma_112, self.turma_114, self.turma_117,
            self.turma_119, self.turma_120, self.turma_121, self.turma_124,
            self.turma_126, self.turma_128, self.turma_129, self.turma_130,
            self.turma_131, self.turma_134, self.turma_135, self.turma_137,
            self.turma_138, self.turma_139, self.turma_140, self.turma_142,
            self.turma_143, self.turma_144, self.turma_145, self.turma_146,
            self.turma_147, self.turma_171,
        ])

    def calcular_erros(self):
        return 2 * (35 - self.calcular_acertos())  # Supondo um total de 35 campos
#**********************************************************************************************************

class HabilidadeProfFinal(models.Model):
    item = models.IntegerField()
    habilidade = models.CharField(max_length=191)
    turma_101 = models.IntegerField(default=0)
    turma_102 = models.IntegerField(default=0)
    # Continue para todas as turmas...
    turma_171 = models.IntegerField(default=0)

    def calcular_acertos(self):
        # Exemplo: soma de valores iguais a 1
        return sum([
            self.turma_101, self.turma_102, self.turma_103, self.turma_104, self.turma_105,
            self.turma_106, self.turma_107, self.turma_109, self.turma_110, self.turma_112,
            self.turma_114, self.turma_117, self.turma_119, self.turma_120, self.turma_121,
            self.turma_124, self.turma_126, self.turma_128, self.turma_129, self.turma_130,
            self.turma_131, self.turma_134, self.turma_135, self.turma_137, self.turma_138,
            self.turma_139, self.turma_140, self.turma_142, self.turma_143, self.turma_144,
            self.turma_145, self.turma_146, self.turma_147, self.turma_171
        ])

    def calcular_erros(self):
        # Exemplo: soma de valores iguais a 0
        return 0
#**********************************************************************************************************
#**********************************************************************************************************
#*** BANCO DE CURRÍCULOS
#**********************************************************************************************************

class Curriculo(models.Model):
    ano_conclusao = models.PositiveIntegerField(blank=True, null=True)
    nome_completo = models.CharField(max_length=191, null=True, blank=True)
    email = models.EmailField()
    telefone = models.CharField(max_length=15)
    foto = models.ImageField(upload_to='fotos/', null=True, blank=True)
    curriculo_pdf = models.FileField(upload_to='curriculos/', null=True, blank=True)
    cpf = models.CharField(max_length=25, unique=True)  # Corrigido para ser único
    rg = models.CharField(max_length=50, blank=True, null=True)
    data_nascimento = models.DateField(null=True, blank=True)
    genero = models.CharField(
        max_length=15,
        choices=[
            ('Masculino', 'Masculino'),
            ('Feminino', 'Feminino'),
            ('Outro', 'Outro'),
            ('NaoInformar', 'Prefiro não informar')
        ]
    )
    estado_civil = models.CharField(
        max_length=15,
        choices=[
            ('Solteiro', 'Solteiro(a)'),
            ('Casado', 'Casado(a)'),
            ('Divorciado', 'Divorciado(a)'),
            ('Viuvo', 'Viúvo(a)')
        ]
    )
    endereco = models.CharField(max_length=191)
    cidade = models.CharField(max_length=100, default='Canaã dos Carajás')
    bairro = models.CharField(max_length=100, blank=True, null=True)
    cep = models.CharField(max_length=9, blank=True, null=True)
    certificados_pdf = models.FileField(upload_to='certificados/', blank=True, null=True)

    # Campos adicionais
    data_cadastro = models.DateTimeField(auto_now_add=True)
    ano_conclusao = models.PositiveIntegerField(blank=True, null=True)
    formacao_academica = models.CharField(max_length=191, blank=True, null=True)
    instituicao = models.CharField(max_length=191, blank=True, null=True)
    curso = models.CharField(max_length=191, blank=True, null=True)
    experiencias_texto = models.TextField(blank=True, null=True)  # Renomeado para evitar conflitos

    def __str__(self):
        return self.nome_completo or "Currículo sem nome"


# ********************************************************************************************************************************

class Formacao(models.Model):
    curriculo = models.ForeignKey(Curriculo, on_delete=models.CASCADE, related_name='formacoes')
    nivel_educacional = models.CharField(
        max_length=20,
        choices=[
            ('Medio', 'Médio'),
            ('MedioTecnico', 'Médio Técnico'),
            ('Graduado', 'Graduado'),
            ('GraduadoIncompleto', 'Graduação Incompleta'),
            ('Especialista', 'Especialista'),
            ('Mestre', 'Mestre'),
            ('Doutor', 'Doutor'),
        ]
    )
    curso = models.CharField(max_length=191)
    instituicao = models.CharField(max_length=191)
    ano_conclusao = models.DateField()

    def __str__(self):
        return f"{self.nivel_educacional} - {self.curso}"


# ********************************************************************************************************************************

class Experiencia(models.Model):
    curriculo = models.ForeignKey(
        Curriculo,
        on_delete=models.CASCADE,
        related_name='experiencias'  # Nome único para evitar conflitos
    )
    empresa = models.CharField(max_length=191)
    cargo = models.CharField(max_length=191)
    data_inicio = models.DateField()
    data_fim = models.DateField(null=True, blank=True)
    descricao_experiencia = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.cargo} - {self.empresa}'

    def clean(self):
        # Validações personalizadas
        if self.data_fim and self.data_inicio and self.data_fim < self.data_inicio:
            raise ValidationError('A data de término não pode ser anterior à data de início.')


#**********************************************************************************************************
#*** FIM BANCO DE CURRÍCULOS
#**********************************************************************************************************



#**********************************************************************************************************
#*** CADASTRO DE DEMANDAS
#**********************************************************************************************************

from django.utils.timezone import now

class TipoDemanda(models.Model):
    PRIORIDADE_CHOICES = [
        ('Baixa', 'Baixa'),
        ('Média', 'Média'),
        ('Alta', 'Alta'),
        ('Urgente', 'Urgente'),
        ('Imediata', 'Imediata'),
    ]

    STATUS_CHOICES = [
        ('Pendente', 'Pendente'),
        ('Em andamento', 'Em andamento'),
        ('Finalizado', 'Finalizado'),
        ('Cancelado', 'Cancelado'),
        ('Aguardando', 'Aguardando'),
        ('Atrasado', 'Atrasado'),
    ]

    nome = models.CharField(max_length=191, verbose_name="Nome da Demanda")
    descricao = models.TextField(max_length=500, blank=True, null=True, verbose_name="Descrição")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pendente',
        verbose_name="Status"
    )
    destinatario = models.CharField(max_length=100, verbose_name="Destinatário")
    prioridade = models.CharField(
        max_length=10,
        choices=PRIORIDADE_CHOICES,
        default='Média',
        verbose_name="Prioridade"
    )
    responsavel = models.CharField(max_length=100, verbose_name="Responsável")
    data_entrega = models.DateField(verbose_name="Data de Entrega")
    data_cadastro = models.DateTimeField(default=now, editable=False, verbose_name="Data de Cadastro")

    class Meta:
        verbose_name = "Tipo de Demanda"
        verbose_name_plural = "Tipos de Demandas"
        ordering = ['-data_cadastro']

    def __str__(self):
        return f"{self.nome} ({self.status})"
# ********************************************************************************************************************************
import os
from datetime import datetime

def renomear_arquivo(instance, filename):
    # Define um nome baseado no timestamp e extensão
    ext = os.path.splitext(filename)[1]
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    return f"fotos/{timestamp}{ext}"


# class Professor(models.Model):
#     SEXO_CHOICES = [
#         ('Masculino', 'Masculino'),
#         ('Feminino', 'Feminino'),
#         ('Outro', 'Outro'),
#         ('NaoInformar', 'Prefiro não informar'),
#     ]

#     ESTADO_CIVIL_CHOICES = [
#         ('Solteiro', 'Solteiro(a)'),
#         ('Casado', 'Casado(a)'),
#         ('Divorciado', 'Divorciado(a)'),
#         ('Viuvo', 'Viúvo(a)'),
#     ]

#     FORMACAO_CHOICES = [
#         ('FundamentalC', 'Fundamental Completo'),
#         ('FundamentalI', 'Fundamental Incompleto'),
#         ('MedioC', 'Médio Completo'),
#         ('MedioI', 'Médio Incompleto'),
#         ('MedioTecnico', 'Médio e Técnico'),
#         ('TecnicoC', 'Técnico Completo'),
#         ('TecnicoI', 'Técnico Incompleto'),
#         ('TecnologoC', 'Técnólogo Completo'),
#         ('TecnologoI', 'Técnólogo Incompleto'),
#         ('GraduacaoC', 'Graduação Completa'),
#         ('GraduacaoI', 'Graduação Incompleta'),
#         ('PosGraduacaoC', 'Pós-Graduação Completa'),
#         ('PosGraduacaoI', 'Pós-Graduação Incompleta'),
#         ('MestradoC', 'Mestrado Completo'),
#         ('MestradoI', 'Mestrado Incompleto'),
#         ('DoutoradoC', 'Doutorado Completo'),
#         ('DoutoradoI', 'Doutorado Incompleto'),
#         ('phdC', 'PHD Completo'),
#         ('phdI', 'PHD Incompleto'),
#     ]

#     nome_completo = models.CharField(max_length=191)
#     cpf = models.CharField(max_length=25, unique=False)
#     rg = models.CharField(max_length=12, blank=True, null=True)
#     email = models.EmailField(unique=True)
#     telefone = models.CharField(max_length=15)
#     endereco = models.CharField(max_length=191)
#     bairro = models.CharField(max_length=100, blank=True, null=True)
#     cidade = models.CharField(max_length=100, default='Canaã dos Carajás')
#     cep = models.CharField(max_length=9, blank=True, null=True)
#     estado_civil = models.CharField(max_length=15, choices=ESTADO_CIVIL_CHOICES)
#     sexo = models.CharField(max_length=15, choices=SEXO_CHOICES)
#     data_nascimento = models.DateField(null=True, blank=True)
#     formacao_academica = models.CharField(max_length=20, choices=FORMACAO_CHOICES, blank=True, null=True)
#     curso = models.CharField(max_length=191, blank=True, null=True)
#     instituicao = models.CharField(max_length=191, blank=True, null=True)
#     ano_conclusao = models.PositiveIntegerField(blank=True, null=True)
#     foto = models.ImageField(upload_to=renomear_arquivo, max_length=191, blank=True, null=True)
#     curriculo_pdf = models.FileField(upload_to='curriculos/', blank=True, null=True)
#     certificados_pdf = models.FileField(upload_to='certificados/', blank=True, null=True)
#     experiencia_profissional = models.TextField(blank=True, null=True)

#     data_cadastro = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.nome_completo

# ********************************************************************************************************************************

# class Certificado(models.Model):
#     professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
#     arquivo = models.FileField(upload_to='certificados/')
# ********************************************************************************************************************************

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from io import BytesIO
from django.core.files.base import ContentFile
import qrcode


class Diretor(models.Model):
    SEXO_CHOICES = [
        ('Masculino', 'Masculino'),
        ('Feminino', 'Feminino'),
        ('Outro', 'Outro'),
        ('NaoInformar', 'Prefiro não informar'),
    ]

    ESTADO_CIVIL_CHOICES = [
        ('Solteiro', 'Solteiro(a)'),
        ('Casado', 'Casado(a)'),
        ('Divorciado', 'Divorciado(a)'),
        ('Viuvo', 'Viúvo(a)'),
    ]

    FORMACAO_CHOICES = [
        ('FundamentalC', 'Fundamental Completo'),
        ('FundamentalI', 'Fundamental Incompleto'),
        ('MedioC', 'Médio Completo'),
        ('MedioI', 'Médio Incompleto'),
        ('MedioTecnico', 'Médio e Técnico'),
        ('TecnicoC', 'Técnico Completo'),
        ('TecnicoI', 'Técnico Incompleto'),
        ('TecnologoC', 'Tecnólogo Completo'),
        ('TecnologoI', 'Tecnólogo Incompleto'),
        ('GraduacaoC', 'Graduação Completa'),
        ('GraduacaoI', 'Graduação Incompleta'),
        ('PosGraduacaoC', 'Pós-Graduação Completa'),
        ('PosGraduacaoI', 'Pós-Graduação Incompleta'),
        ('MestradoC', 'Mestrado Completo'),
        ('MestradoI', 'Mestrado Incompleto'),
        ('DoutoradoC', 'Doutorado Completo'),
        ('DoutoradoI', 'Doutorado Incompleto'),
        ('phdC', 'PHD Completo'),
        ('phdI', 'PHD Incompleto'),
    ]

    nome_completo = models.CharField(max_length=191)
    cpf = models.CharField(max_length=25, unique=True)
    rg = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=15)
    endereco = models.CharField(max_length=191)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    cidade = models.CharField(max_length=100, default='Canaã dos Carajás')
    cep = models.CharField(max_length=10, blank=True, null=True)
    data_nascimento = models.DateField(null=True, blank=True)
    formacao_academica = models.CharField(max_length=100, blank=True, null=True)
    curso = models.CharField(max_length=191, blank=True, null=True)
    instituicao = models.CharField(max_length=191, blank=True, null=True)
    ano_conclusao = models.DateField(null=True, blank=True)
    foto = models.ImageField(upload_to='fotos_diretores/', blank=True, null=True)
    curriculo_pdf = models.FileField(upload_to='diretores_curriculos/', blank=True, null=True)
    certificados_pdf = models.FileField(upload_to='diretores_certificados/', blank=True, null=True)
    experiencia_profissional = models.TextField(blank=True, null=True)
    estado_civil = models.CharField(max_length=50, choices=ESTADO_CIVIL_CHOICES)
    sexo = models.CharField(max_length=50, choices=SEXO_CHOICES)

    data_cadastro = models.DateTimeField(default=now)
    empresa = models.CharField(max_length=191, blank=True, null=True)
    cargo = models.CharField(max_length=191, blank=True, null=True)
    data_inicio = models.DateField(blank=True, null=True)
    data_fim = models.DateField(blank=True, null=True)
    qr_code = models.ImageField(upload_to='diretores_qrcodes/', null=True, blank=True)

    def clean(self):
        if not self.nome_completo:
            raise ValidationError("O nome completo é obrigatório.")
        if not self.cpf:
            raise ValidationError("O CPF é obrigatório.")
        if not self.email:
            raise ValidationError("O e-mail é obrigatório.")
        if not self.telefone:
            raise ValidationError("O telefone é obrigatório.")
        if len(self.cpf) != 14:
            raise ValidationError("O CPF deve ter 14 caracteres (formato: 000.000.000-00).")

    def generate_qr_code(self):
        if not self.qr_code:
            qr_data = f"https://semedcanaadoscarajas.gov.br/diretor/{self.id}/"
            qr = qrcode.QRCode(box_size=10, border=4)
            qr.add_data(qr_data)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            file_name = f"qr_code_{self.id}.png"
            self.qr_code.save(file_name, ContentFile(buffer.getvalue()), save=False)

    def save(self, *args, **kwargs):
        self.full_clean()  # Valida antes de salvar
        if not self.data_cadastro:
            self.data_cadastro = now()
        self.generate_qr_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome_completo

# ********************************************************************************************************************************

class ExperienciaProfissional(models.Model):
    diretor = models.ForeignKey(Diretor, on_delete=models.CASCADE, related_name='experiencias')
    empresa = models.CharField(max_length=191)
    cargo = models.CharField(max_length=191)
    data_inicio = models.DateField(null=True, blank=True)
    data_fim = models.DateField(null=True, blank=True)
# ********************************************************************************************************************************

class FormacaoAcademica(models.Model):
    diretor = models.ForeignKey(Diretor, on_delete=models.CASCADE, related_name="formacoes")
    nivel = models.CharField(max_length=100)  # Ex.: Graduação Completa
    instituicao = models.CharField(max_length=191)
    curso = models.CharField(max_length=191)
    ano_conclusao = models.DateField()

    def __str__(self):
        return f"{self.nivel} em {self.instituicao}"
    
# ********************************************************************************************************************************

class Certificado(models.Model):
    diretor = models.ForeignKey(Diretor, on_delete=models.CASCADE, related_name='certificados')
    arquivo = models.FileField(upload_to='certificados/')
    descricao = models.CharField(max_length=191, null=True, blank=True)
# ********************************************************************************************************************************

from django.contrib.auth.models import AbstractUser
from django.db import models

class CandidatoD(AbstractUser):
    cpf = models.CharField(max_length=25, unique=True, verbose_name="CPF")
    telefone = models.CharField(max_length=15, blank=True, null=True)
    endereco = models.TextField(blank=True, null=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='candidatod_set',
        blank=True,
        help_text='Os grupos aos quais o usuário pertence.',
        verbose_name='grupos',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='candidatod_set',
        blank=True,
        help_text='Permissões específicas para este usuário.',
        verbose_name='permissões de usuário',
    )

    def __str__(self):
        return self.username
# ********************************************************************************************************************************
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone


class CadastroCandidato(models.Model):
    nome_completo = models.CharField(max_length=191)
    email = models.EmailField(unique=True)
    cpf = models.CharField(max_length=25, unique=True)
    password = models.CharField(max_length=128, null=True, blank=True)
    last_login = models.DateTimeField(null=True, blank=True)

    # Temporariamente recriado
    senha = models.CharField(max_length=128, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith("pbkdf2_"):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def check_senha(self, senha):
        return check_password(senha, self.password)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def get_username(self):
        return self.email

    def get_full_name(self):
        return self.nome_completo

    def get_email_field_name(self):
        return 'email'

    def get_session_auth_hash(self):
        return ''  # Pode implementar hash de sessão se necessário

    def __str__(self):
        return self.nome_completo




# ********************************************************************************************************************************

from django.db import models

class CandidatoCurriculo(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='candidatos_curriculos')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nome_completo = models.CharField(max_length=191)
    email = models.EmailField(unique=True)
    cpf = models.CharField(max_length=25, unique=True)
    password = models.CharField(max_length=191)

    def __str__(self):
        return self.nome_completo
# ********************************************************************************************************************************

from django.db import models

class CandidatoAutenticado(models.Model):
    #user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil_candidato")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cpf = models.CharField(max_length=25, unique=True)  # CPF único para o candidato

    def __str__(self):
        return self.user.first_name
# ********************************************************************************************************************************

class ModulePermission(models.Model):
    """
    Define permissões específicas para os módulos.
    """
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="permissions")
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "semedapp_module_permission"

    def __str__(self):
        return f"{self.module.nome} - {self.description}"
# ********************************************************************************************************************************
    
class UserModulePermission(models.Model):
    """
    Relaciona os usuários aos módulos permitidos.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="module_permissions")
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="user_permissions")

    class Meta:
        db_table = "semedapp_user_module_permission"

    def __str__(self):
        return f"{self.user.username} - {self.module.nome}"
# ********************************************************************************************************************************

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from .managers import UserManager  # Certifique-se de importar o UserManager

class User(AbstractUser):
    ROLE_CHOICES = [
        ("Administrador", "Administrador"),
        ("Gestor", "Gestor"),
        ("Técnico", "Técnico"),
    ]
    
    role = models.CharField(
        max_length=15,
        choices=ROLE_CHOICES,
        default="Técnico",
        verbose_name="Função do Usuário"
    )
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set",
        blank=True,
        verbose_name="Grupos"
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_set",
        blank=True,
        verbose_name="Permissões"
    )

    # Adicionando o UserManager personalizado
    objects = UserManager()

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return f"{self.username} ({self.role})"

# ********************************************************************************************************************************

class RoleModulePermission(models.Model):
    """
    Relaciona funções a permissões específicas de módulos.
    """
    ROLE_CHOICES = [
        ('administrador', 'Administrador'),
        ('coordenador', 'Coordenador'),
        ('professor', 'Professor'),
        ('secretaria', 'Secretaria'),
    ]
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, verbose_name="Função")
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="role_permissions")

    class Meta:
        db_table = "semedapp_role_module_permission"

    def __str__(self):
        return f"{self.get_role_display()} - {self.module.nome}"
# ********************************************************************************************************************************

from django.db import models

class CurriculoAntigo(models.Model):
    id = models.AutoField(primary_key=True)
    cpf = models.CharField(max_length=25, null=True, blank=True)
    nome = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    senha = models.CharField(max_length=100, null=True, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    sexo = models.CharField(max_length=100, null=True, blank=True)
    naturalidade = models.CharField(max_length=100, null=True, blank=True)
    naturalidade_uf = models.CharField(max_length=2, null=True, blank=True)
    pne = models.CharField(max_length=3, null=True, blank=True)
    pne_detalhe = models.CharField(max_length=500, null=True, blank=True)
    curriculo_lattes = models.CharField(max_length=300, null=True, blank=True)
    logradouro = models.CharField(max_length=300, null=True, blank=True)
    numero = models.CharField(max_length=10, null=True, blank=True)
    bairro = models.CharField(max_length=100, null=True, blank=True)
    cep = models.CharField(max_length=10, null=True, blank=True)
    complemento = models.CharField(max_length=500, null=True, blank=True)
    uf = models.CharField(max_length=2, null=True, blank=True)
    municipio = models.IntegerField(null=True, blank=True)
    fone1 = models.CharField(max_length=100, null=True, blank=True)
    fone2 = models.CharField(max_length=100, null=True, blank=True)
    formacao_nivel = models.IntegerField(null=True, blank=True)
    formacao_instituicao = models.CharField(max_length=200, null=True, blank=True)
    formacao_curso = models.CharField(max_length=200, null=True, blank=True)
    formacao_situacao = models.CharField(max_length=50, null=True, blank=True)
    formacao_inicio = models.CharField(max_length=10, null=True, blank=True)
    formacao_conclusao = models.CharField(max_length=10, null=True, blank=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_update = models.DateTimeField(auto_now=True)
    ip = models.CharField(max_length=50, null=True, blank=True)
    cargo = models.CharField(max_length=100, null=True, blank=True)  # ✅ Adicionamos a coluna CARGO

    class Meta:
        db_table = 'curriculo_antigo'
# ********************************************************************************************************************************

    def get_cargo_utf8(self):
        """
        Método seguro para exibir o cargo corrigindo caracteres com problema de codificação.
        """
        if self.cargo:
            try:
                return self.cargo.encode("latin-1").decode("utf-8")
            except UnicodeDecodeError:
                return self.cargo.encode("utf-8", "ignore").decode("utf-8")
        return ""

    def __str__(self):
        """
        Converte o nome para UTF-8 se necessário.
        """
        return self.nome.encode('utf-8').decode('utf-8') if self.nome else "Sem Nome"
# ********************************************************************************************************************************

class Resposta(models.Model):
    aluno = models.ForeignKey('Aluno', on_delete=models.CASCADE)
    conceito = models.CharField(max_length=100, choices=[
        ('CERTO', 'Certo'),
        ('ERRADO', 'Errado'),
        ('PARCIAL', 'Parcial'),
        ('BRANCO', 'Branco'),
        ('LAUDO', 'Criança com Laudo')
    ])
    data_resposta = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.aluno.nome} - {self.conceito}"
# ********************************************************************************************************************************

class Conceito(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    habilidade = models.CharField(max_length=50)  # EI05CMH1, EI05LGH1 etc.
    conceito = models.CharField(max_length=50, choices=[('CERTO', 'Certo'), ('ERRADO', 'Errado'), ('PARCIAL', 'Parcial')])
    data_resposta = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.aluno.nome} - {self.habilidade} - {self.conceito}"
    
#     from django.db import models

# class Aluno(models.Model):
#     nome = models.CharField(max_length=191)
#     turma = models.CharField(max_length=50)

#     def __str__(self):
#         return f"{self.nome} - {self.turma}"
# essa classe ja existe
# ********************************************************************************************************************************

# models.py
from django.db import models

class ConceitoLancado(models.Model):
    aluno = models.CharField(max_length=191)
    turma = models.CharField(max_length=100)
    ano = models.CharField(max_length=4)
    modalidade = models.CharField(max_length=100)
    conceito_matematica = models.CharField(max_length=50, choices=[
        ('Excelente', 'Excelente'),
        ('Bom', 'Bom'),
        ('Regular', 'Regular'),
        ('Necessita Melhorar', 'Necessita Melhorar'),
    ], null=True, blank=True)
    conceito_linguagem = models.CharField(max_length=50, choices=[
        ('Excelente', 'Excelente'),
        ('Bom', 'Bom'),
        ('Regular', 'Regular'),
        ('Necessita Melhorar', 'Necessita Melhorar'),
    ], null=True, blank=True)
    data_lancamento = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.aluno} - {self.turma} - {self.ano}"
# ********************************************************************************************************************************

from django.db import models

class AtendimentoSOE(models.Model):
    estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE)
    data = models.DateTimeField()
    descricao = models.TextField()
    nome_unidade_ensino = models.CharField(max_length=191)
    ano_serie = models.CharField(max_length=100, blank=True, null=True)
    nome_turma = models.CharField(max_length=100, blank=True, null=True)
    classificacao_nome = models.CharField(max_length=100)
    tipo_ocorrencia_nome = models.CharField(max_length=191)
    registro = models.DateTimeField()
    status_descricao = models.CharField(max_length=50)
    fonte_dado = models.CharField(max_length=50, choices=[
        ('SIGE', 'SIGE'),
        ('Synaptic', 'Synaptic'),
        ('Orientadores', 'Orientadores'),
        ('SOE', 'SOE'),
        ('AutoKee', 'AutoKee')
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'atendimento_soe'  # Nome correto da tabela no banco de dados

    def __str__(self):
        return f"{self.nome_unidade_ensino} - {self.tipo_ocorrencia_nome}"

# ********************************************************************************************************************************

class SynapticAtendimento(models.Model):
    nome_unidade_ensino = models.CharField(max_length=191)
    ano_serie = models.CharField(max_length=191)
    nome_turma = models.CharField(max_length=191)
    classificacao_nome = models.CharField(max_length=191)
    tipo_ocorrencia_nome = models.CharField(max_length=191)
    registro = models.DateTimeField()
    status_descricao = models.CharField(max_length=191)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'synaptic_atendimento'  # Confirme o nome aqui

# ********************************************************************************************************************************
from django.db import models

class SIGEAtendimento(models.Model):
    nome_unidade_ensino = models.CharField(max_length=191)
    ano_serie = models.CharField(max_length=100, blank=True, null=True)
    nome_turma = models.CharField(max_length=100, blank=True, null=True)
    classificacao_nome = models.CharField(max_length=100)
    tipo_ocorrencia_nome = models.CharField(max_length=191)
    registro = models.DateTimeField()
    status_descricao = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sige_atendimento'
        verbose_name = 'SIGE Atendimento'
        verbose_name_plural = 'SIGE Atendimentos'

    def __str__(self):
        return f"{self.nome_unidade_ensino} - {self.classificacao_nome}"


# ********************************************************************************************************************************

class AutoKeeAtendimento(models.Model):
    nome_unidade_ensino = models.CharField(max_length=191)
    ano_serie = models.CharField(max_length=100, blank=True, null=True)
    nome_turma = models.CharField(max_length=100, blank=True, null=True)
    classificacao_nome = models.CharField(max_length=100)
    tipo_ocorrencia_nome = models.CharField(max_length=191)
    registro = models.DateTimeField()
    status_descricao = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'autokee_atendimento'  # Atualize com o nome correto

# ********************************************************************************************************************************

from django.db import models

class OrientadoresAtendimento(models.Model):
    nome_orientador = models.CharField(max_length=191)
    escola = models.CharField(max_length=191)
    ocorrencias_conselho_tutelar = models.IntegerField(default=0)
    ameaca = models.IntegerField(default=0)
    agressao_fisica = models.IntegerField(default=0)
    assedio = models.IntegerField(default=0)
    violencia_sexual = models.IntegerField(default=0)
    exploracao_sexual = models.IntegerField(default=0)
    bullying = models.IntegerField(default=0)
    infrequencia = models.IntegerField(default=0)
    evasao = models.IntegerField(default=0)
    repetencia = models.IntegerField(default=0)
    furtos = models.IntegerField(default=0)
    gravidez_adolescencia = models.IntegerField(default=0)
    explosivos = models.IntegerField(default=0)
    trafico_drogas = models.IntegerField(default=0)
    uso_alcool_drogas = models.IntegerField(default=0)
    vandalismo = models.IntegerField(default=0)
    posse_armas = models.IntegerField(default=0)
    delegacia_civil = models.IntegerField(default=0)
    deaca = models.IntegerField(default=0)
    escuta_especializada = models.IntegerField(default=0)
    creas = models.IntegerField(default=0)
    cras = models.IntegerField(default=0)
    viver_conviver = models.IntegerField(default=0)
    ministerio_publico = models.IntegerField(default=0)
    policia_militar = models.IntegerField(default=0)
    busca_ativa = models.IntegerField(default=0)
    centro_tea = models.IntegerField(default=0)
    caps = models.IntegerField(default=0)
    saude = models.IntegerField(default=0)
    total_geral = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.nome_orientador} - {self.escola}"

# ********************************************************************************************************************************

class SOEAtendimento(models.Model):
    nome_unidade_ensino = models.CharField(max_length=191)
    ano_serie = models.CharField(max_length=50)
    nome_turma = models.CharField(max_length=100)
    classificacao_nome = models.CharField(max_length=100)
    tipo_ocorrencia_nome = models.CharField(max_length=100)
    registro = models.DateTimeField()
    status_descricao = models.CharField(max_length=50)
    fonte_dado = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'soe_atendimento'  # Atualize com o nome correto
# ********************************************************************************************************************************

class Indicador(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    meta = models.IntegerField()
    resultado = models.IntegerField()
# ********************************************************************************************************************************

# models.py

class ProfessorEI(models.Model):
    unidade_ensino = models.CharField(max_length=191)
    ano = models.IntegerField()
    modalidade = models.CharField(max_length=191)
    formato_letivo = models.CharField(max_length=191)
    turma = models.CharField(max_length=191)
    nome_professor = models.CharField(max_length=191)
    cpf_professor = models.CharField(max_length=14)
    email_professor = models.EmailField()

    def __str__(self):
        return self.nome_professor
############################################################################################################################

class Coordenador(models.Model):
    unidade_ensino = models.CharField(max_length=191)
    ano = models.IntegerField()
    modalidade = models.CharField(max_length=191)
    formato_letivo = models.CharField(max_length=191)
    nome_Coordenadora = models.CharField(max_length=191)
    cpf_professor = models.CharField(max_length=14)
    email_Coordenadora = models.EmailField()

    def __str__(self):
        return self.nome_Coordenadora
############################################################################################################################

class CoordenadorEI(models.Model):
    unidade_ensino = models.CharField(max_length=191)
    ano = models.CharField(max_length=20)
    modalidade = models.CharField(max_length=100)
    formato_letivo = models.CharField(max_length=100)
    nome_Coordenadora = models.CharField(max_length=191)
    cpf_professor = models.CharField(max_length=14)
    email_Coordenadora = models.EmailField()

    def __str__(self):
        return self.nome_Coordenadora
############################################################################################################################

from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import BaseUserManager

class CustomUserProfManager(BaseUserManager):
    def create_user(self, username, cpf, first_name, last_name, password=None, **extra_fields):
        if not username:
            raise ValueError("O nome de usuário é obrigatório")
        if not cpf:
            raise ValueError("O CPF é obrigatório")

        user = self.model(
            username=username,
            cpf=cpf,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, cpf, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, cpf, first_name, last_name, password, **extra_fields)

    def get_by_natural_key(self, username):
        return self.get(username=username)


############################################################################################################################

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from .managers import UserManager


class CustomUserProf(AbstractUser):
    # Papéis do usuário
    is_coordenador = models.BooleanField(default=False, verbose_name="Coordenador")
    is_professor = models.BooleanField(default=False, verbose_name="Professor")

    # Relações com escolas
    escola = models.ForeignKey(
        'semedapp.Escolas',  # Certo: string e não objeto
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='usuarios_vinculados',
        verbose_name="Escola Principal"
    )


    escolas = models.ManyToManyField(
        'semedapp.EscolaPdde',  # nome do modelo referenciado
        related_name='usuarios',
        blank=True,
        verbose_name="Escolas PDDE Vinculadas"
    )

    # Identificação e contato
    matricula = models.CharField(max_length=15, unique=True, verbose_name="Matrícula")
    telefone = models.CharField(max_length=15, blank=True, null=True, verbose_name="Telefone")
    especializacao = models.CharField(max_length=100, blank=True, null=True, verbose_name="Especialização")

    # Credenciais e dados pessoais
    username = models.CharField(max_length=150, unique=True, verbose_name="Nome de Usuário")
    cpf = models.CharField(max_length=25, unique=True, verbose_name="CPF")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    first_name = models.CharField(max_length=30, blank=True, null=True, verbose_name="Nome")
    last_name = models.CharField(max_length=30, blank=True, null=True, verbose_name="Sobrenome")

    # Estado e controle
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    # Permissões personalizadas
    groups = models.ManyToManyField(
        Group,
        related_name='customuserprof_set',
        blank=True,
        verbose_name="Grupos"
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuserprof_permissions',
        blank=True,
        verbose_name="Permissões"
    )

    # Manager e configurações do AbstractUser
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['cpf', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name or ''} {self.last_name or ''} ({self.username})"


############################################################################################################################

class Permissao(models.Model):
    """ Define permissões personalizadas para os usuários """
    nome = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nome
############################################################################################################################

class UserPermissao(models.Model):
    """ Relaciona usuários com permissões específicas """
    usuario = models.ForeignKey(CustomUserProf, on_delete=models.CASCADE)
    permissao = models.ForeignKey(Permissao, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.usuario.username} - {self.permissao.nome}"
############################################################################################################################

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

from django.db import models

class UnidadeEscolar(models.Model):
    nome = models.CharField(max_length=191)
    endereco = models.CharField(max_length=191, blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.nome
############################################################################################################################

# models.py
from django.db import models
alunos = Aluno
class Professor(models.Model):
    nome = models.CharField(max_length=191)
    cpf = models.CharField(max_length=25, unique=True)
    email = models.EmailField()
############################################################################################################################

class Turma(models.Model):
    nome = models.CharField(max_length=191)  # <-- Removido unique=True
    ano_letivo = models.IntegerField(default=2025)  # Garante que tenha um valor padrão
    professor = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.SET_NULL,
    null=True,
    blank=True
)

    escola = models.ForeignKey(Escolas, on_delete=models.CASCADE)
    ano = models.IntegerField()
    modalidade = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nome} - {self.escola.nome}"
############################################################################################################################
    
class CadastroEscola(models.Model):
    unidade_ensino = models.CharField(max_length=191)
    formato_letivo = models.CharField(max_length=50)
    cpf = models.CharField(max_length=25)
    data_nascimento = models.DateField()
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name="escolas")
    professor = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.SET_NULL,
    null=True,
    blank=True
)
    ano = models.IntegerField()
    modalidade = models.CharField(max_length=50)
    pessoa_nome = models.CharField(max_length=191)
    idade = models.IntegerField()
    avaliado = models.CharField(max_length=3, choices=[("SIM", "Sim"), ("NÃO", "Não")])

    def __str__(self):
        return self.unidade_ensino
############################################################################################################################


class ProfessorEscola(models.Model):
    professor = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.SET_NULL,
    null=True,
    blank=True
)
    escolas = models.ForeignKey(Escolas, on_delete=models.CASCADE)  # Verifique o nome aqui
    turmas = models.ManyToManyField(Turma)
    


    def __str__(self):
        return f"{self.professor.username} - {self.escolas.nome}"
############################################################################################################################

class CadastroEI(models.Model):
    professor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    id_matricula = models.AutoField(primary_key=True)
    unidade_ensino = models.CharField(max_length=191)
    formato_letivo = models.CharField(max_length=191, null=True, blank=True)
    cpf = models.CharField(max_length=25)
    data_nascimento = models.DateField(null=True, blank=True)
    ano = models.CharField(max_length=4)
    modalidade = models.CharField(max_length=100)
    pessoa_nome = models.CharField(max_length=191)
    idade = models.IntegerField()
    avaliado = models.CharField(
        max_length=3, choices=[("SIM", "Sim"), ("NAO", "Não")], default="NAO"
    )

    turma = models.ForeignKey(Turma, on_delete=models.SET_NULL, null=True, blank=True)

    id_coordenador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cadastros_como_id_coordenador'
    )

    coordenador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cadastros_como_coordenador'
    )

    # Campos para as questões de Matemática e Linguagem
    questao_matematica_1 = models.CharField(max_length=50, null=True, blank=True)
    questao_matematica_2 = models.CharField(max_length=50, null=True, blank=True)
    questao_matematica_3 = models.CharField(max_length=50, null=True, blank=True)
    questao_matematica_4 = models.CharField(max_length=50, null=True, blank=True)
    questao_matematica_5 = models.CharField(max_length=50, null=True, blank=True)
    questao_matematica_6 = models.CharField(max_length=50, null=True, blank=True)
    questao_matematica_7 = models.CharField(max_length=50, null=True, blank=True)
    questao_matematica_8 = models.CharField(max_length=50, null=True, blank=True)
    questao_matematica_9 = models.CharField(max_length=50, null=True, blank=True)
    questao_matematica_10 = models.CharField(max_length=50, null=True, blank=True)

    questao_linguagem_11 = models.CharField(max_length=50, null=True, blank=True)
    questao_linguagem_12 = models.CharField(max_length=50, null=True, blank=True)
    questao_linguagem_13 = models.CharField(max_length=50, null=True, blank=True)
    questao_linguagem_14 = models.CharField(max_length=50, null=True, blank=True)
    questao_linguagem_15 = models.CharField(max_length=50, null=True, blank=True)
    questao_linguagem_16 = models.CharField(max_length=50, null=True, blank=True)
    questao_linguagem_17 = models.CharField(max_length=50, null=True, blank=True)
    questao_linguagem_18 = models.CharField(max_length=50, null=True, blank=True)
    questao_linguagem_19 = models.CharField(max_length=50, null=True, blank=True)
    questao_linguagem_20 = models.CharField(max_length=50, null=True, blank=True)

    # Campos para as questões de Matemática e Linguagem
    for i in range(1, 11):
        locals()[f"questao_matematica_{i}"] = models.CharField(max_length=50, null=True, blank=True)

    for i in range(11, 21):
        locals()[f"questao_linguagem_{i}"] = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.pessoa_nome} - {self.unidade_ensino}"

# ********************************************************************************************************************************


# ********************************************************************************************************************************

class NotaAluno(models.Model):
    aluno = models.ForeignKey(CadastroEI, on_delete=models.CASCADE)
    disciplina = models.CharField(max_length=100)
    nota = models.DecimalField(max_digits=4, decimal_places=2)  # Exemplo: 9.5
    bimestre = models.IntegerField(choices=[(1, "1º Bimestre"), (2, "2º Bimestre"), (3, "3º Bimestre"), (4, "4º Bimestre")])

    def __str__(self):
        return f"{self.aluno.pessoa_nome} - {self.disciplina} - {self.nota}"
# ********************************************************************************************************************************

from django.db import models
from semedapp.models import CustomUserProf  # 🔹 Confirme que este é o modelo correto

class ModuleModulosPermitidos(models.Model):
    customuserprof = models.ForeignKey(
        CustomUserProf,  # 🔹 Referenciando corretamente o modelo CustomUserProf
        on_delete=models.CASCADE,
        db_column="customuserprof_id",  # 🔹 Ajustado para o nome correto da coluna no banco de dados
        related_name="modulos_permitidos"  # 🔹 Evita conflitos no relacionamento reverso
    )
    module = models.ForeignKey(
        Module, 
        on_delete=models.CASCADE,
        db_column="module_id"  # 🔹 Define explicitamente a referência correta ao módulo
    )

    class Meta:
        db_table = "semedapp_modulemodulospermitidos"  # 🔹 Nome correto da tabela no banco

    def __str__(self):
        return f"{self.customuserprof.username} - {self.module.nome}"  # 🔹 Melhor debug
# ********************************************************************************************************************************
# ********************************************************************************************************************************
# *****************************************************SEPECC*********************************************************************
# ********************************************************************************************************************************

from decimal import Decimal
from django.db import models

class ReceitaDespesa(models.Model):
    TIPO_CHOICES = [
        ("receita", "Receita"),
        ("despesa", "Despesa"),
    ]

    escola = models.ForeignKey('EscolaPdde', on_delete=models.CASCADE, related_name="receitadespesa")
    programa = models.CharField(max_length=191)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default="receita")
    periodo_execucao = models.IntegerField()

    # 🏦 **Saldos Anteriores**
    saldo_anterior_custeio = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    saldo_anterior_capital = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))

    # 📌 **Valores Creditados**
    valor_creditado_custeio = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    valor_creditado_capital = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))

    # ✅ **Novos Campos**
    recursos_proprios_custeio = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    recursos_proprios_capital = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))

    # 💰 **Rendimento e Devoluções**
    rendimento_aplicacao_custeio = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    rendimento_aplicacao_capital = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))

    devolucao_fnde_custeio = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    devolucao_fnde_capital = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))

    # 📌 **Receitas e Despesas**
    total_receita = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    total_despesa = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))

    # 📌 **Saldos Reprogramados e Devolvidos**
    saldo_reprogramar_custeio = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    saldo_reprogramar_capital = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))

    saldo_devolvido_custeio = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    saldo_devolvido_capital = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))

    escolas_atendidas = models.IntegerField(default=0)

    # ✅ **Campo para armazenar o saldo disponível**
    saldo_disponivel = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))

    ## 🔹 **Propriedades para cálculo dinâmico**
    @property
    def saldo_reprogramado_custeio(self):
        return (self.saldo_anterior_custeio + self.valor_creditado_custeio +
                self.recursos_proprios_custeio + self.rendimento_aplicacao_custeio -
                self.devolucao_fnde_custeio - self.total_despesa - self.saldo_devolvido_custeio)

    @property
    def saldo_reprogramado_capital(self):
        return (self.saldo_anterior_capital + self.valor_creditado_capital +
                self.recursos_proprios_capital + self.rendimento_aplicacao_capital -
                self.devolucao_fnde_capital - self.total_despesa - self.saldo_devolvido_capital)

    ## 🔹 **Cálculo do Saldo Disponível**
    def calcular_saldo_disponivel(self):
        receita_total = (
            self.saldo_anterior_custeio + self.saldo_anterior_capital +
            self.valor_creditado_custeio + self.valor_creditado_capital +
            self.recursos_proprios_custeio + self.recursos_proprios_capital +
            self.rendimento_aplicacao_custeio + self.rendimento_aplicacao_capital
        )

        return receita_total - (self.total_despesa + self.devolucao_fnde_custeio + self.devolucao_fnde_capital +
                                self.saldo_devolvido_custeio + self.saldo_devolvido_capital)

    ## 🔹 **Salva e recalcula o saldo disponível**
    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)

        self.saldo_disponivel = self.calcular_saldo_disponivel()
        super().save(update_fields=["saldo_disponivel"])

    def __str__(self):
        return f"{self.escola.nome} - {self.programa} ({self.periodo_execucao})"

# ********************************************************************************************************************************

from django.db import models

class Receita(models.Model):
    escola = models.ForeignKey('EscolaPdde', on_delete=models.CASCADE, related_name="receitas")
    programa = models.CharField(max_length=191)
    data_inicio = models.DateField()
    data_fim = models.DateField(default="2025-12-31")

    saldo_anterior_custeio = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    saldo_anterior_capital = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    valor_creditado_custeio = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    valor_creditado_capital = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    # 🔹 Renomeamos para recursos_proprios_custeio e recursos_proprios_capital
    recursos_proprios_custeio = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    recursos_proprios_capital = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    rendimento_aplicacao_custeio = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    rendimento_aplicacao_capital = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    devolucao_fnde_custeio = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    devolucao_fnde_capital = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    saldo_reprogramar_custeio = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    saldo_reprogramar_capital = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    saldo_devolvido_custeio = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    saldo_devolvido_capital = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    valor_total_receita_custeio = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    valor_total_receita_capital = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    valor_despesa_realizada_custeio = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    valor_despesa_realizada_capital = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    escolas_atendidas = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.escola} - {self.programa} ({self.data_inicio} a {self.data_fim})"
# ********************************************************************************************************************************

from django.db import models

class Programa(models.Model):
    nome = models.CharField(max_length=191, unique=True, verbose_name="Nome do Programa")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição do Programa")
    resolucao = models.CharField(max_length=191, blank=True, null=True, verbose_name="Resolução")
    data_inicio = models.DateField(verbose_name="Data de Início", null=True, blank=True)
    data_fim = models.DateField(verbose_name="Data de Fim", null=True, blank=True)

    def __str__(self):
        return self.nome
# ********************************************************************************************************************************
from django.db import models
from django.conf import settings  # ✅ Corrigida a importação

class EscolaPdde(models.Model):
    NIVEIS_ENSINO = [
        ("Educação Infantil", "Educação Infantil"),
        ("Ensino Fundamental", "Ensino Fundamental"),
        ("Ensino Médio", "Ensino Médio"),
        ("Educação de Jovens e Adultos (EJA)", "Educação de Jovens e Adultos (EJA)"),
        ("Técnico Profissionalizante", "Técnico Profissionalizante"),
    ]

    # 📌 Identificação da Escola
    nome = models.CharField(max_length=191)
    ano = models.IntegerField(default=2025)
    status = models.CharField(
        max_length=20,
        choices=[
            ("aprovado", "Aprovado"),
            ("pendente", "Pendente"),
            ("reprovado", "Reprovado"),
        ],
        default="pendente"
    )
    cnpj = models.CharField(max_length=18, unique=True)
    endereco = models.CharField(max_length=191, null=True, blank=True)
    cep = models.CharField(max_length=9, null=True, blank=True)
    bairro = models.CharField(max_length=191, null=True, blank=True)
    cidade = models.CharField(max_length=191, default="Canaã dos Carajás")
    uf = models.CharField(max_length=2, default="PA")

    # 🔗 Programas vinculados
    programas = models.ManyToManyField('Programa', blank=True, related_name="escolas")

    # 📌 Dados Administrativos
    tipo = models.CharField(max_length=50, null=True, blank=True)
    dependencia_administrativa = models.CharField(max_length=50, null=True, blank=True)
    codigo_inep = models.CharField(max_length=10, unique=True)

    # 🗺️ Localização
    zona = models.CharField(
        max_length=10,
        choices=[("Rural", "Rural"), ("Urbana", "Urbana")],
        default="Urbana"
    )

    # 📁 Documentação
    procuracao = models.FileField(upload_to="procuracoes/", null=True, blank=True)
    validade_procuracao = models.DateField(null=True, blank=True)

    # 🏫 Níveis de Ensino
    ensino = models.CharField(
        max_length=191,
        null=True,
        blank=True,
        help_text="Informe os níveis de ensino disponíveis na escola"
    )

    # 🏗️ Estrutura Física
    quantidade_salas = models.IntegerField(default=0)
    quantidade_turmas = models.IntegerField(default=0)
    quantidade_professores = models.IntegerField(default=0)
    quantidade_alunos = models.IntegerField(default=0)

    # 👥 Conselho Escolar
    nome_conselho = models.CharField(
        max_length=191,
        null=True,
        blank=True,
        help_text="Nome do Conselho Escolar"
    )

    # 👤 Coordenador Responsável
    coordenador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='escolas_pdde'
    )


    def __str__(self):
        return self.nome

# ********************************************************************************************************************************

class SemedAppEscolaPddeProgramas(models.Model):
    escolapdde = models.ForeignKey(EscolaPdde, on_delete=models.CASCADE)
    programa = models.ForeignKey(Programa, on_delete=models.CASCADE)

# ********************************************************************************************************************************

class EscolaPrograma(models.Model):
    escola = models.ForeignKey(EscolaPdde, on_delete=models.CASCADE, related_name="programas_escola", verbose_name="Escola")
    programa = models.ForeignKey(Programa, on_delete=models.CASCADE, related_name="escolas_participantes", verbose_name="Programa")
    data_inicio = models.DateField(verbose_name="Data de Início", null=True, blank=True)
    data_fim = models.DateField(verbose_name="Data de Fim", null=True, blank=True)

    def __str__(self):
        return f"{self.escola.nome} - {self.programa.nome}"
# ********************************************************************************************************************************

class EscolaPddeProgramas(models.Model):
    escolapdde = models.ForeignKey(EscolaPdde, on_delete=models.CASCADE)
    programa = models.ForeignKey(Programa, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.escolapdde.nome} - {self.programa.nome}"
# ********************************************************************************************************************************

# 🚀 **Pagamentos Efetuados**
from django.db import models
from django.db.models import F, DecimalField
from django.core.exceptions import ObjectDoesNotExist

class Pagamento(models.Model):
    escola = models.ForeignKey("EscolaPdde", on_delete=models.CASCADE)
    programa = models.CharField(max_length=191)
    nome_favorecido = models.CharField(max_length=191)
    cnpj_cpf = models.CharField(max_length=25, blank=True, null=True)
    tipo_pagamento = models.CharField(
        max_length=50,
        choices=[("Custeio", "Custeio"), ("Capital", "Capital")]
    )
    tipo_bem_servico = models.TextField()
    origem = models.CharField(max_length=50, default="FNDE")

    tipo_documento = models.CharField(
        max_length=50,
        choices=[
            ("NF", "Nota Fiscal"),
            ("Cupom", "Cupom Fiscal"),
            ("PIX", "PIX"),
            ("Boleto", "Boleto"),
            ("Outros", "Outros"),
        ]
    )
    numero_documento = models.CharField(max_length=100)
    data_documento = models.DateField()

    tipo_pagamento_efetuado = models.CharField(
        max_length=50,
        choices=[
            ("Dinheiro", "Dinheiro"),
            ("PIX", "PIX"),
            ("TED", "TED"),
            ("Cartão de Crédito", "Cartão de Crédito"),
            ("Cartão de Débito", "Cartão de Débito"),
            ("Cheque", "Cheque"),
            ("Outros", "Outros"),
        ]
    )
    numero_documento_pagamento = models.CharField(max_length=100)
    data_pagamento = models.DateField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    exercicio = models.IntegerField()

    def save(self, *args, **kwargs):
        """
        Atualiza os valores de `valor_despesa_realizada_custeio`, `valor_despesa_realizada_capital`
        e os saldos reprogramados ao salvar um pagamento.
        """
        super().save(*args, **kwargs)  # Salva o pagamento primeiro

        try:
            receita = Receita.objects.get(escola=self.escola, programa=self.programa)

            if self.tipo_pagamento == "Custeio":
                # Atualiza a despesa realizada (soma o novo pagamento)
                Receita.objects.filter(id=receita.id).update(
                    valor_despesa_realizada_custeio=F("valor_despesa_realizada_custeio") + self.valor
                )

                # Atualiza o saldo reprogramado após salvar a despesa corretamente
                Receita.objects.filter(id=receita.id).update(
                    saldo_reprogramar_custeio=(
                        F("saldo_anterior_custeio") + F("valor_creditado_custeio") + F("recursos_proprios_custeio") 
                        + F("rendimento_aplicacao_custeio")
                        - F("devolucao_fnde_custeio") - F("valor_despesa_realizada_custeio") - F("saldo_devolvido_custeio")
                    )
                )

            else:  # Caso seja "Capital"
                # Atualiza a despesa realizada (soma o novo pagamento)
                Receita.objects.filter(id=receita.id).update(
                    valor_despesa_realizada_capital=F("valor_despesa_realizada_capital") + self.valor
                )

                # Atualiza o saldo reprogramado após salvar a despesa corretamente
                Receita.objects.filter(id=receita.id).update(
                    saldo_reprogramar_capital=(
                        F("saldo_anterior_capital") + F("valor_creditado_capital") + F("recursos_proprios_capital") 
                        + F("rendimento_aplicacao_capital")
                        - F("devolucao_fnde_capital") - F("valor_despesa_realizada_capital") - F("saldo_devolvido_capital")
                    )
                )

        except ObjectDoesNotExist:
            print(f"⚠️ Nenhuma Receita encontrada para a Escola {self.escola.nome} e Programa {self.programa}")

    def __str__(self):
        return f"{self.nome_favorecido} - R$ {self.valor}"
# ********************************************************************************************************************************
from django.db import models

class ContaBancaria(models.Model):
    escola = models.ForeignKey(
        "EscolaPdde", 
        on_delete=models.CASCADE, 
        related_name="contas"
    )
    conselho = models.CharField(
        max_length=191, 
        blank=True, 
        null=True,
        help_text="Conselho vinculado à escola."
    )
    programa = models.ForeignKey(
        "Programa",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text="Programa vinculado à conta bancária."
    )
    nome = models.CharField(
        max_length=100, 
        help_text="Nome da conta bancária (ex: Conta Principal)",
    )
    banco = models.CharField(
        max_length=100, 
        help_text="Nome do banco da conta."
    )
    agencia = models.CharField(
        max_length=20, 
        help_text="Número da agência bancária."
    )
    conta = models.CharField(
        max_length=20, 
        help_text="Número da conta bancária."
    )
    saldo = models.DecimalField(
        max_digits=15, decimal_places=2, 
        default=0.00, 
        help_text="Saldo atual da conta bancária."
    )
    tipo_conta = models.CharField(
        max_length=10,
        choices=[("Corrente", "Corrente"), ("Poupança", "Poupança")],
        default="Corrente",
        help_text="Tipo da conta bancária."
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["escola", "banco", "agencia", "conta"], 
                name="unique_conta_bancaria_por_escola"
            )
        ]
        ordering = ["escola", "banco"]

    def save(self, *args, **kwargs):
        """Ao salvar a conta, automaticamente adiciona o conselho vinculado à escola."""
        if self.escola:
            self.conselho = self.escola.nome_conselho
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.banco} - {self.agencia}/{self.conta} ({self.escola.nome})"


# ********************************************************************************************************************************

from django.conf import settings  # Importando configuração do usuário customizado
from django.db import models
from decimal import Decimal

class LancamentoBancario(models.Model):
    TIPOS = [
        ("Entrada", "Entrada"),
        ("Saída", "Saída"),
    ]
    TIPO_CHOICES = [
        ('credito', 'Entrada'),
        ('debito', 'Saída'),
    ]

    data = models.DateField(verbose_name="Data do Lançamento")
    descricao = models.CharField(max_length=191, verbose_name="Descrição")
    tipo = models.CharField(max_length=7, choices=TIPO_CHOICES, verbose_name="Tipo de Lançamento")
    valor = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Valor (R$)")
    conta_bancaria = models.ForeignKey(
        "ContaBancaria",
        on_delete=models.CASCADE,
        related_name='lancamentos',
        verbose_name="Conta Bancária"
    )
    origem_destino = models.CharField(max_length=191, blank=True, null=True, verbose_name="Origem/Destino")
    
    # 🔹 Atualizando a referência para o usuário customizado
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Correto para usuários customizados
        on_delete=models.CASCADE,
        verbose_name="Usuário"
    )

    comprovante = models.FileField(upload_to='comprovantes/', blank=True, null=True, verbose_name="Comprovante")
    categoria = models.CharField(max_length=100, blank=True, null=True, verbose_name="Categoria")
    escola = models.ForeignKey("EscolaPdde", on_delete=models.CASCADE, verbose_name="Escola")

    def save(self, *args, **kwargs):
        """ Atualiza saldo da conta ao salvar lançamento """

        # 🔹 Converte `valor` para Decimal caso seja string
        if isinstance(self.valor, str):
            self.valor = Decimal(self.valor.replace(",", "."))

        # 🔹 Verifica se a transação é de débito e há saldo suficiente
        if self.tipo == 'debito' and self.valor > self.conta_bancaria.saldo:
            raise ValueError("Saldo insuficiente para essa transação.")

        # 🔹 Atualiza saldo da conta ANTES de salvar o lançamento
        if self.pk is None:  # Se for um novo lançamento
            if self.tipo == 'credito':
                self.conta_bancaria.saldo += self.valor
            else:
                self.conta_bancaria.saldo -= self.valor
        else:  # Caso esteja editando um lançamento existente
            lancamento_antigo = LancamentoBancario.objects.get(pk=self.pk)
            diferenca = self.valor - lancamento_antigo.valor

            if self.tipo == 'credito':
                self.conta_bancaria.saldo += diferenca
            else:
                self.conta_bancaria.saldo -= diferenca

        self.conta_bancaria.save()  # Salva a conta bancária primeiro
        super().save(*args, **kwargs)  # Salva o lançamento em seguida

    def __str__(self):
        return f"{self.descricao} - R$ {self.valor} ({self.tipo})"

# ********************************************************************************************************************************
# *****************************************************PESQUISA DE PREÇOS*********************************************************
# ********************************************************************************************************************************

from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=191)

    def __str__(self):
        return self.nome
# ********************************************************************************************************************************

class Subcategoria(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    nome = models.CharField(max_length=191)

    def __str__(self):
        return f"{self.categoria.nome} - {self.nome}"
# ********************************************************************************************************************************

from django.db import models
from django.contrib.auth import get_user_model
from semedapp.models import EscolaPdde, Programa, Categoria, Subcategoria

class Item(models.Model):
    nome = models.CharField(max_length=191)
    descricao = models.TextField(blank=True, null=True)
    unidade_medida = models.CharField(max_length=50)

    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, related_name="itens")
    subcategoria = models.ForeignKey(Subcategoria, on_delete=models.SET_NULL, null=True, related_name="itens")
    usuario = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="itens_cadastrados")

    escola = models.ForeignKey(EscolaPdde, on_delete=models.CASCADE, null=True, blank=True, related_name="itens")
    programa = models.ForeignKey(Programa, on_delete=models.SET_NULL, null=True, blank=True, related_name="itens")

    def __str__(self):
        return self.nome



# ********************************************************************************************************************************

from django.db import models

class Proponente(models.Model):
    nome = models.CharField(max_length=191)
    cpf_cnpj = models.CharField(max_length=18, unique=True)  # Aceita CPF ou CNPJ
    email = models.EmailField(max_length=191, unique=True)
    telefone = models.CharField(max_length=50)
    endereco = models.CharField(max_length=191)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2, choices=[
        ("AC", "Acre"), ("AL", "Alagoas"), ("AP", "Amapá"), ("AM", "Amazonas"),
        ("BA", "Bahia"), ("CE", "Ceará"), ("DF", "Distrito Federal"), ("ES", "Espírito Santo"),
        ("GO", "Goiás"), ("MA", "Maranhão"), ("MT", "Mato Grosso"), ("MS", "Mato Grosso do Sul"),
        ("MG", "Minas Gerais"), ("PA", "Pará"), ("PB", "Paraíba"), ("PR", "Paraná"),
        ("PE", "Pernambuco"), ("PI", "Piauí"), ("RJ", "Rio de Janeiro"), ("RN", "Rio Grande do Norte"),
        ("RS", "Rio Grande do Sul"), ("RO", "Rondônia"), ("RR", "Roraima"), ("SC", "Santa Catarina"),
        ("SP", "São Paulo"), ("SE", "Sergipe"), ("TO", "Tocantins")
    ])
    cep = models.CharField(max_length=9)
    tipo_proponente = models.CharField(max_length=20, choices=[
        ("Pessoa Física", "Pessoa Física"),
        ("Pessoa Jurídica", "Pessoa Jurídica")
    ])
    representante_legal = models.CharField(max_length=191, blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)


    # 👇 Campos novos
    escola = models.ForeignKey(EscolaPdde, on_delete=models.CASCADE)
    programa = models.CharField(max_length=191, blank=True, null=True)

    def __str__(self):
        return f"{self.nome} ({self.cpf_cnpj})"

# ********************************************************************************************************************************

from django.db import models

class Proposta(models.Model):
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    proponente = models.ForeignKey('Proponente', on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)  # Campo para quantidade
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    valor_total = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)  # Campo para valor total
    data_proposta = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """ Calcula o valor total antes de salvar a proposta """
        self.valor_total = self.preco_unitario * self.quantidade
        super(Proposta, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.item.nome} - {self.proponente.nome} - {self.quantidade}x R${self.preco_unitario}"

# ********************************************************************************************************************************

from django.db import models
from .models import Item, Proponente

class ApuracaoResultado(models.Model):
    STATUS_CHOICES = [
        ("Pendente", "Pendente"),
        ("Adjudicado", "Adjudicado"),
        ("Revogado", "Revogado"),
    ]

    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="apuracoes")
    proponente_vencedor = models.ForeignKey(Proponente, on_delete=models.CASCADE, related_name="apuracoes_vencidas")
    quantidade = models.PositiveIntegerField(default=1)
    preco_vencedor = models.DecimalField(max_digits=10, decimal_places=2)
    valor_total = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    data_apuracao = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pendente")

    def save(self, *args, **kwargs):
        if self.quantidade and self.preco_vencedor:
            self.valor_total = self.quantidade * self.preco_vencedor
        else:
            self.valor_total = 0
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.item.nome} - {self.proponente_vencedor.nome} ({self.status})"




# ********************************************************************************************************************************

from django.db import models

class Orcamento(models.Model):
    item = models.ForeignKey("Item", on_delete=models.CASCADE)
    proponente = models.ForeignKey("Proponente", on_delete=models.CASCADE)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item} - {self.proponente} - R$ {self.preco}"
############################################################################################################################


from django.db import models

class Documento(models.Model):
    TIPO_DOCUMENTO = [
        ('NF', 'Nota Fiscal'),
        ('RC', 'Recibo'),
        ('CT', 'Contrato'),
        ('OT', 'Outros'),
    ]

    escola = models.ForeignKey(
        'EscolaPdde',
        on_delete=models.CASCADE,
        related_name="documentos",
        verbose_name="Escola"
    )

    tipo = models.CharField(
        max_length=2,
        choices=TIPO_DOCUMENTO,
        verbose_name="Tipo do Documento"
    )

    numero = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Número do Documento"
    )

    data_emissao = models.DateField(
        verbose_name="Data de Emissão"
    )

    descricao = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descrição do Documento"
    )

    arquivo = models.FileField(
        upload_to="documentos_prestacao_contas/",
        null=True,
        blank=True,
        verbose_name="Arquivo Anexado"
    )

    valor_total = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True, 
        verbose_name="Valor Total (R$)"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Criado em"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Última atualização"
    )

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.numero} ({self.escola.nome})"
############################################################################################################################

class BemAdquirido(models.Model):
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE, related_name="bens")
    especificacao = models.CharField(max_length=191)
    quantidade = models.IntegerField()
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def valor_total(self):
        return self.quantidade * self.valor_unitario

    def __str__(self):
        return self.especificacao
############################################################################################################################

from django.db import models

class RepresentanteLegal(models.Model):
    nome = models.CharField(max_length=191)
    cpf = models.CharField(max_length=25, unique=True)  # Confirme se existe
    email = models.EmailField(unique=True)  # Confirme se existe
    telefone = models.CharField(max_length=15)  # Confirme se existe
    cargo = models.CharField(max_length=191)

    escola = models.ForeignKey(EscolaPdde, on_delete=models.CASCADE, related_name="representantes")

    def __str__(self):
        return self.nome
############################################################################################################################

from django.db import models

class Bem(models.Model):
    escola = models.ForeignKey(
        'EscolaPdde',
        on_delete=models.CASCADE,
        verbose_name="Escola"
    )

    nome_conselho = models.CharField(
        max_length=191,
        blank=True,
        null=True,
        verbose_name="Nome do Conselho"
    )

    nome = models.CharField(max_length=191, verbose_name="Nome do Bem")
    documento = models.FileField(upload_to="documentos_bens/", verbose_name="Documento de Aquisição")
    quantidade = models.PositiveIntegerField(verbose_name="Quantidade")
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Unitário (R$)")
    valor_total = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name="Valor Total (R$)")
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name="Data de Cadastro")

    def save(self, *args, **kwargs):
        if self.quantidade and self.valor_unitario:
            self.valor_total = self.quantidade * self.valor_unitario
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nome} - {self.escola.nome}"
############################################################################################################################

# models.py
from django.db import models

class TermoDoacao(models.Model):
    escola = models.ForeignKey('EscolaPdde', on_delete=models.CASCADE)
    conselho = models.CharField(max_length=191)
    bem = models.ForeignKey('BemDoado', on_delete=models.CASCADE, null=True, blank=True)
    data_emissao = models.DateField(auto_now_add=True)
############################################################################################################################

class BemDoado(models.Model):
    escola = models.ForeignKey('EscolaPdde', on_delete=models.CASCADE, verbose_name="Escola")
    conselho = models.CharField(max_length=191, verbose_name="Conselho Escolar")
    descricao = models.CharField(max_length=191, verbose_name="Descrição do Bem")
    quantidade = models.PositiveIntegerField()
    numero_nota = models.CharField(max_length=50, verbose_name="Nº Nota Fiscal")
    data_nota = models.DateField(verbose_name="Data da Nota Fiscal")
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    valor_total = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    data_doacao = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.valor_total = self.quantidade * self.valor_unitario
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.descricao} - {self.escola.nome}"

##########################################################################################################################################
##########################################################################################################################################
################################################GESTÃO ESCOLA#################################################################
##########################################################################################################################################

from django.db import models

STATUS_CHOICES = (
    ('enviado', 'Enviado'),
    ('deferido', 'Deferido'),
    ('indeferido', 'Indeferido'),
)

class PlanoGestaoEscolar(models.Model):
    unidade_ensino = models.CharField(max_length=191)
    cargo = models.CharField(max_length=100, default='Diretor')
    servidor = models.CharField(max_length=191)
    telefone = models.CharField(max_length=20)
    arquivo = models.FileField(upload_to='pge_planos/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Não Enviado')  # <- aqui
    enviado = models.BooleanField(default=False)
    data_envio = models.DateTimeField(auto_now_add=True)
    deferido_indeferido = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.servidor} - {self.unidade_ensino}"
############################################################################################################################

from django.db import models

class PGEPlanoGestaoEscolar(models.Model):
    unidade_ensino = models.CharField(max_length=191)
    cargo = models.CharField(max_length=50)
    servidor = models.CharField(max_length=191)
    telefone = models.CharField(max_length=20)
    arquivo = models.FileField(upload_to='pge/', blank=True, null=True)
    enviado = models.BooleanField(default=False)
    deferido_indeferido = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.unidade_ensino} - {self.servidor}"
############################################################################################################################

from django.db import models

class Conselho(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()

    def __str__(self):
        return self.nome
############################################################################################################################



from django.db import models

class LancamentoDiario(models.Model):
    data = models.DateField()
    historico = models.CharField(max_length=191)
    recebimento = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    pagamento = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.data} - {self.historico}"
############################################################################################################################



from django.db import models

class MotivoIndeferimento(models.Model):
    plano = models.ForeignKey('PlanoGestaoEscolar', on_delete=models.CASCADE, related_name='motivos')
    motivo = models.TextField()
    prazo_reenvio = models.DateField()
    parecer_direcao = models.CharField(max_length=50, choices=[('Diretor', 'Diretor de Ensino'), ('Vice-Diretor', 'Coordenador(a)')])
    orientacoes = models.TextField(blank=True, null=True)
    anexo_parecer = models.FileField(upload_to='indeferimentos/', blank=True, null=True)
    data_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Indeferimento - {self.plano.unidade_ensino}"
############################################################################################################################


class ConselhoMembro(models.Model):
    nome = models.CharField(max_length=191)
    escola = models.ForeignKey(EscolaPdde, on_delete=models.CASCADE)
    cargo = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nome} - {self.cargo}"
############################################################################################################################

class Noticia(models.Model):
    titulo = models.CharField(max_length=200)
    imagem = models.ImageField(upload_to='noticias/')
    conteudo = models.TextField()
    publicado = models.BooleanField(default=False)
    criado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    publicado_em = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.titulo



class ProgramaEscola(models.Model):
    escola = models.ForeignKey(EscolaPdde, on_delete=models.CASCADE)
    nome = models.CharField(max_length=255)
    coordenador = models.ForeignKey('semedapp.CustomUserProf', on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return f"{self.nome} ({self.escola})"
    



from django.db import models
from .models import EscolaPdde  # ou ajuste conforme a importação no seu projeto

class CertidaoEmitida(models.Model):
    TIPO_CERTIDAO_CHOICES = [
        ('regularidade', 'Regularidade'),
        ('prestacao_contas', 'Prestação de Contas'),
        ('outro', 'Outro'),
    ]

    escola = models.ForeignKey(EscolaPdde, on_delete=models.CASCADE, related_name='certidoes')
    tipo = models.CharField(max_length=100, choices=TIPO_CERTIDAO_CHOICES)
    descricao = models.TextField(blank=True)
    data_emissao = models.DateField()
    arquivo = models.FileField(upload_to='certidoes/', blank=True, null=True)

    class Meta:
        verbose_name = "Certidão Emitida"
        verbose_name_plural = "Certidões Emitidas"
        ordering = ['-data_emissao']

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.escola.nome} ({self.data_emissao})"
