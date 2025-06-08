# forms.py
from django import forms
from .models import UserModulePermission
from .models import LivroCaixa
from .models import EscrituraFiscal
from .models import Legislacao
from .models import PortuguesProfessores
from django.shortcuts import render, redirect
from .models import DiagnoseInicProfPort
from .models import Imagem, Conteudo, Evento, Usuario
from .models import Funcionario
from .models import RegimentoCadastro
from .models import Regimento
from .models import Curriculo
from .models import TipoDemanda
from .models import Curriculo
from .models import Diretor
from .models import Professor
from .models import Escola
from .models import Formacao
from .models import Curriculo, Formacao, Experiencia

from django.forms import inlineformset_factory
from .models import Diretor, ExperienciaProfissional, FormacaoAcademica, Certificado


class UserModulePermissionForm(forms.ModelForm):
    class Meta:
        model = UserModulePermission
        fields = ['user', 'module']
# *******************************************************************************************************************

from .models import LivroCaixa

class LivroCaixaForm(forms.ModelForm):
    class Meta:
        model = LivroCaixa
        fields = [
            'ano_base', 'conselho_escolar', 'cnpj',
            'rendimentos_aplicacao', 'saldo_anterior',
            'receita_total', 'despesas_manutencao',
            'despesa_total', 'superavit_deficit'
        ]

# *******************************************************************************************************************

class EscrituraFiscalForm(forms.ModelForm):
    class Meta:
        model = EscrituraFiscal
        fields = [
            'ano_base', 'conselho_escolar', 'cnpj',
            'rendimentos_aplicacao', 'saldo_anterior', 'receita_total',
            'despesas_manutencao', 'despesa_total', 'superavit_deficit'
        ]
        widgets = {
            'ano_base': forms.NumberInput(attrs={'class': 'form-control'}),
            'conselho_escolar': forms.TextInput(attrs={'class': 'form-control'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-control'}),
            'rendimentos_aplicacao': forms.NumberInput(attrs={'class': 'form-control'}),
            'saldo_anterior': forms.NumberInput(attrs={'class': 'form-control'}),
            'receita_total': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}),
            'despesas_manutencao': forms.NumberInput(attrs={'class': 'form-control'}),
            'despesa_total': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}),
            'superavit_deficit': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}),
        }
# *******************************************************************************************************************

class LegislacaoForm(forms.ModelForm):
    class Meta:
        model = Legislacao
        fields = ['titulo', 'descricao', 'data_publicacao', 'categoria']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control'}),
            'data_publicacao': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'categoria': forms.TextInput(attrs={'class': 'form-control'}),
        }

# *******************************************************************************************************************

class ImagemForm(forms.ModelForm):
    class Meta:
        model = Imagem
        fields = ['titulo', 'descricao', 'imagem']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o título'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Digite a descrição'}),
            'imagem': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
# *******************************************************************************************************************

class ConteudoForm(forms.ModelForm):
    class Meta:
        model = Conteudo
        fields = ['titulo', 'descricao', 'imagem']
# *******************************************************************************************************************

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['titulo', 'data', 'local', 'descricao']
# *******************************************************************************************************************

from django import forms
from .models import Usuario  # Certifique-se de que o modelo esteja correto

class UsuarioForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control shadow-sm p-3',
            'placeholder': 'Confirme a senha'
        }),
        label="Confirmar Senha"
    )

    class Meta:
        model = Usuario
        fields = ['nome', 'email', 'senha']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control shadow-sm p-3',
                'placeholder': 'Digite o nome'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control shadow-sm p-3',
                'placeholder': 'Digite o e-mail'
            }),
            'senha': forms.PasswordInput(attrs={
                'class': 'form-control shadow-sm p-3',
                'placeholder': 'Digite a senha'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get('senha')
        confirm_password = cleaned_data.get('confirm_password')

        if senha and confirm_password and senha != confirm_password:
            self.add_error('confirm_password', "As senhas não coincidem.")
        
        return cleaned_data

# *******************************************************************************************************************

class PortuguesProfessoresForm(forms.ModelForm):
    class Meta:
        model = PortuguesProfessores
        fields = '__all__'
# *******************************************************************************************************************

def lingua_portuguesa_prof_view(request):
    turmas = ['401', '403', '404', '406', '408', '409', '410', '413', '414', '415', '417', '421', '423', '426', '428', '429', '430', '431', '432', '433', '434', '435', '436', '437', '438', '439', '441', '442', '447', '451', '471']
    itens = [
        {'numero': 1, 'habilidade': 'D12'},
        {'numero': 2, 'habilidade': 'D03'},
        # Continue com os outros itens...
    ]

    if request.method == 'POST':
        for item in itens:
            numero = item['numero']
            habilidade = item['habilidade']
            
            # Criar uma instância de DiagnoseInicProfPort
            diagnose = DiagnoseInicProfPort(
                item=numero,
                habilidade=habilidade,
            )
            
            # Preencher os campos dos professores
            for turma in turmas:
                resposta = request.POST.get(f'respostas_{numero}_{turma}')
                setattr(diagnose, f'professor_{turma}', resposta)
            
            # Salvar a instância no banco de dados
            diagnose.save()

        return redirect('alguma_view_de_confirmacao')  # Redirecionar para uma página de confirmação ou outro lugar

    return render(request, 'diagnoses/lingua_portuguesa_prof.html', {'turmas': turmas, 'itens': itens})
# *******************************************************************************************************************

class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = '__all__'
# *******************************************************************************************************************

class RegimentoCadastroForm(forms.ModelForm):
    class Meta:
        model = RegimentoCadastro
        fields = '__all__'
# *******************************************************************************************************************

class RegimentoForm(forms.ModelForm):
    class Meta:
        model = Regimento
        fields = '__all__'
# *******************************************************************************************************************

class UploadPlanilhaForm(forms.Form):
    planilha = forms.FileField(label="Upload da Planilha")
    
# *******************************************************************************************************************
# **** BANCO DE CURRÍCUOS
# *******************************************************************************************************************

class CurriculoForm(forms.ModelForm):
    class Meta:
        model = Curriculo
        fields = [
            'nome_completo', 'email', 'telefone', 'foto', 'curriculo_pdf', 
            'cpf', 'rg', 'data_nascimento', 'genero', 'estado_civil',
            'endereco', 'cidade', 'bairro', 'cep', 'certificados_pdf',
            'formacao_academica', 'curso', 'instituicao', 'ano_conclusao', 
            'experiencias_texto'  # Use o nome correto do campo no modelo
        ]
        widgets = {
            'nome_completo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu nome completo'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu CPF'}),
            'rg': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu RG'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu e-mail'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(XX) XXXXX-XXXX'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu endereço'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu bairro'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite sua cidade'}),
            'cep': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu CEP'}),
            'estado_civil': forms.Select(attrs={'class': 'form-control'}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'formacao_academica': forms.Select(attrs={'class': 'form-control'}),
            'curso': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o curso'}),
            'instituicao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite a instituição'}),
            'ano_conclusao': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Digite o ano de conclusão'}),
            'experiencias': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Descreva suas experiências profissionais'}),
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'curriculo_pdf': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'certificados_pdf': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
# *******************************************************************************************************************

class FormacaoForm(forms.ModelForm):
    class Meta:
        model = Formacao
        fields = ['nivel_educacional', 'curso', 'instituicao', 'ano_conclusao']
        widgets = {
            'ano_conclusao': forms.DateInput(attrs={'type': 'date'}),
        }
# *******************************************************************************************************************

class ExperienciaForm(forms.ModelForm):
    class Meta:
        model = Experiencia
        fields = ['empresa', 'cargo', 'data_inicio', 'data_fim', 'descricao_experiencia']
        widgets = {
            'data_inicio': forms.DateInput(attrs={'type': 'date'}),
            'data_fim': forms.DateInput(attrs={'type': 'date'}),
        }
# *******************************************************************************************************************

# class FormacaoForm(forms.ModelForm):
#     class Meta:
#         model = Formacao
#         fields = ['nivel_educacional', 'instituicao', 'curso', 'ano_conclusao']

# class ExperienciaForm(forms.ModelForm):
#     class Meta:
#         model = Experiencia
#         fields = ['empresa', 'cargo', 'data_inicio', 'data_fim', 'descricao']
#         widgets = {
#             'data_inicio': forms.DateInput(attrs={'type': 'date'}),
#             'data_fim': forms.DateInput(attrs={'type': 'date'}),
#         }

# *******************************************************************************************************************

class TipoDemandaForm(forms.ModelForm):
    class Meta:
        model = TipoDemanda
        fields = ['data_entrega', 'descricao', 'responsavel', 'destinatario', 'prioridade', 'status']
        widgets = {
            'data_entrega': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite a descrição'}),
            'responsavel': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o responsável'}),
            'destinatario': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o destinatário'}),
            'prioridade': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
# *******************************************************************************************************************

class EscolaForm(forms.ModelForm):
    class Meta:
        model = Escola
        fields = '__all__'  # Inclui todos os campos do modelo
        widgets = {
            'dependencias_fisicas': forms.Textarea(attrs={'rows': 3}),
            'acessibilidade': forms.Textarea(attrs={'rows': 3}),
            'instrumentos_pedagogicos': forms.Textarea(attrs={'rows': 3}),
            'equipamentos_alunos': forms.Textarea(attrs={'rows': 3}),
        }
# *******************************************************************************************************************

# class ProfessorForm(forms.ModelForm):
#     class Meta:
#         model = Professor
#         fields = [
#             'nome_completo', 'cpf', 'rg', 'email', 'telefone', 'endereco', 'bairro', 'cidade',
#             'cep', 'estado_civil', 'sexo', 'data_nascimento', 'formacao_academica', 'curso',
#             'instituicao', 'ano_conclusao', 'foto', 'curriculo_pdf', 'certificados_pdf',
#             'experiencia_profissional'
#         ]


from django import forms
from .models import Professor

class ProfessorForm(forms.ModelForm):
    class Meta:
        model = Professor
        fields = ['nome', 'cpf', 'email']  # Inclua apenas os campos existentes no modelo Professor

# *******************************************************************************************************************

class DiretorForm(forms.ModelForm):
    class Meta:
        model = Diretor
        fields = [
            'nome_completo', 'cpf', 'rg', 'email', 'telefone', 'endereco', 'bairro', 'cidade', 
            'estado_civil', 'sexo', 'data_nascimento', 'curso', 'instituicao', 
            'foto', 'curriculo_pdf', 'certificados_pdf', 'experiencia_profissional', 
            'empresa', 'cargo', 'data_inicio', 'data_fim'
        ]
# *******************************************************************************************************************

class ExperienciaProfissionalForm(forms.ModelForm):
    class Meta:
        model = ExperienciaProfissional
        fields = ['empresa', 'cargo', 'data_inicio', 'data_fim']
# *******************************************************************************************************************

from django import forms
from django.forms import modelformset_factory
from .models import FormacaoAcademica

class FormacaoAcademicaForm(forms.ModelForm):
    class Meta:
        model = FormacaoAcademica
        fields = ['nivel', 'instituicao', 'curso', 'ano_conclusao']

# Criação do formset
FormacaoFormSet = modelformset_factory(
    FormacaoAcademica,
    form=FormacaoAcademicaForm,
    extra=1,  # Número de formulários extras para entrada
    can_delete=True  # Permite exclusão de registros existentes
)

# *******************************************************************************************************************

class CertificadoForm(forms.ModelForm):
    class Meta:
        model = Certificado
        fields = ['arquivo', 'descricao']
# *******************************************************************************************************************

ExperienciaFormSet = inlineformset_factory(Diretor, ExperienciaProfissional, form=ExperienciaProfissionalForm, extra=1)
FormacaoFormSet = inlineformset_factory(Diretor, FormacaoAcademica, form=FormacaoAcademicaForm, extra=1)
CertificadoFormSet = inlineformset_factory(Diretor, Certificado, form=CertificadoForm, extra=1)

from django import forms
from django.contrib.auth.models import User

class EditarPerfilForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
# *******************************************************************************************************************

from django import forms
from .models import Candidato  # Certifique-se de que o modelo Candidato existe

class FormDeAtualizacao(forms.ModelForm):
    class Meta:
        model = Candidato  # Substitua por seu modelo
        fields = ['nome_completo', 'email', 'cpf']  # Ajuste os campos conforme necessário
# *******************************************************************************************************************

from django import forms

class UploadCSVForm(forms.Form):
    file = forms.FileField(label="Selecione um arquivo CSV")
# *******************************************************************************************************************

from django import forms
from .models import Resposta

class RespostaForm(forms.ModelForm):
    class Meta:
        model = Resposta
        fields = ['aluno', 'conceito', 'data_resposta']
        widgets = {
            'data_resposta': forms.DateInput(attrs={'type': 'date'}),
        }
# *******************************************************************************************************************

# forms.py
from django import forms
from .models import Conceito, Aluno

class LancamentoConceitoForm(forms.ModelForm):
    aluno = forms.ModelChoiceField(queryset=Aluno.objects.all(), label="Aluno", widget=forms.Select(attrs={'class': 'form-select'}))
    habilidade = forms.ChoiceField(
        choices=[
            ('EI05CMH1', 'EI05CMH1 - Identificar os numerais e grafar até 10'),
            ('EI05CMH2', 'EI05CMH2 - Associar uma quantidade de objetos a um número natural'),
            ('EI05LGH1', 'EI05LGH1 - Grafar o nome próprio completo com auxílio do crachá'),
            ('EI05LGH2', 'EI05LGH2 - Identificar as letras do nome no alfabeto'),
            # Adicione todas as habilidades aqui...
        ],
        label="Habilidade",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    conceito = forms.ChoiceField(
        choices=[('CERTO', 'Certo'), ('ERRADO', 'Errado'), ('PARCIAL', 'Parcial')],
        label="Conceito",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Conceito
        fields = ['aluno', 'habilidade', 'conceito']
# *******************************************************************************************************************

from django import forms

class ConceitoForm(forms.Form):
    conceito_matematica = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 3, "class": "form-control"}), 
        label="Conceitos de Matemática", 
        required=True
    )
    conceito_linguagem = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 3, "class": "form-control"}), 
        label="Conceitos de Linguagem", 
        required=True
    )
# *******************************************************************************************************************

# forms.py
from django import forms
from .models import Professor, Coordenador,ProfessorEI

class ProfessorEIForm(forms.ModelForm):
    class Meta:
        model = ProfessorEI
        fields = ['unidade_ensino', 'ano', 'modalidade', 'formato_letivo', 'turma', 'nome_professor', 'cpf_professor', 'email_professor']
        widgets = {
            'unidade_ensino': forms.TextInput(attrs={'class': 'form-control'}),
            'ano': forms.TextInput(attrs={'class': 'form-control'}),
            'modalidade': forms.TextInput(attrs={'class': 'form-control'}),
            'formato_letivo': forms.TextInput(attrs={'class': 'form-control'}),
            'turma': forms.TextInput(attrs={'class': 'form-control'}),
            'nome_professor': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf_professor': forms.TextInput(attrs={'class': 'form-control'}),
            'email_professor': forms.EmailInput(attrs={'class': 'form-control'}),
        }
# *******************************************************************************************************************

class CoordenadorForm(forms.ModelForm):
    class Meta:
        model = Coordenador
        fields = ['unidade_ensino', 'ano', 'modalidade', 'formato_letivo', 'nome_Coordenadora', 'cpf_professor', 'email_Coordenadora']
        widgets = {
            'unidade_ensino': forms.TextInput(attrs={'class': 'form-control'}),
            'ano': forms.TextInput(attrs={'class': 'form-control'}),
            'modalidade': forms.TextInput(attrs={'class': 'form-control'}),
            'formato_letivo': forms.TextInput(attrs={'class': 'form-control'}),
            'nome_Coordenadora': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf_professor': forms.TextInput(attrs={'class': 'form-control'}),
            'email_Coordenadora': forms.EmailInput(attrs={'class': 'form-control'}),
        }
# *******************************************************************************************************************

from django import forms
from django.contrib.auth.forms import AuthenticationForm

class ProfessorLoginForm(AuthenticationForm):
    username = forms.CharField(label='Nome de Usuário', max_length=150)
    password = forms.CharField(widget=forms.PasswordInput, label='Senha')
# *******************************************************************************************************************

from django import forms
from .models import CustomUserProf

class CustomUserProfCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUserProf
        fields = ['username', 'email', 'matricula', 'telefone', 'especializacao', 'password']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
# *******************************************************************************************************************

from django import forms
from .models import Aluno

class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ['pessoa_nome', 'cpf', 'idade', 'modalidade', 'avaliado', 'professor']  # Use apenas os campos corretos

# *******************************************************************************************************************
# ***************************************************SEPECC**********************************************************
# *******************************************************************************************************************

from django import forms
from .models import EscolaPdde, Programa
import re

class EscolaPddeForm(forms.ModelForm):
    programas = forms.ModelMultipleChoiceField(
        queryset=Programa.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check-input"}),
        required=False,
        label="Programas"
    )

    procuracao = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={"class": "form-control"}),
        label="Procuração (Upload)"
    )

    validade_procuracao = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        label="Validade da Procuração"
    )

    class Meta:
        model = EscolaPdde
        fields = [
            "nome", "endereco", "zona", "ensino", "cep", "bairro", "cidade", "uf", "tipo",
            "dependencia_administrativa", "codigo_inep", "cnpj", "nome_conselho",
            "quantidade_salas", "quantidade_turmas", "quantidade_professores", "quantidade_alunos",
            "procuracao", "validade_procuracao", "programas"
        ]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "cnpj": forms.TextInput(attrs={"class": "form-control", "placeholder": "99.999.999/9999-99"}),
            "endereco": forms.TextInput(attrs={"class": "form-control"}),
            "codigo_inep": forms.TextInput(attrs={"class": "form-control", "maxlength": "10"}),
            "zona": forms.Select(attrs={"class": "form-control"}),
            "ensino": forms.Select(attrs={"class": "form-control"}),
            "cep": forms.TextInput(attrs={"class": "form-control"}),
            "bairro": forms.TextInput(attrs={"class": "form-control"}),
            "cidade": forms.TextInput(attrs={"class": "form-control"}),
            "uf": forms.TextInput(attrs={"class": "form-control", "maxlength": "2"}),
            "tipo": forms.TextInput(attrs={"class": "form-control"}),
            "dependencia_administrativa": forms.TextInput(attrs={"class": "form-control"}),
            "nome_conselho": forms.TextInput(attrs={"class": "form-control"}),
            "quantidade_salas": forms.NumberInput(attrs={"class": "form-control"}),
            "quantidade_turmas": forms.NumberInput(attrs={"class": "form-control"}),
            "quantidade_professores": forms.NumberInput(attrs={"class": "form-control"}),
            "quantidade_alunos": forms.NumberInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        """ Garante que os programas vinculados à escola sejam carregados corretamente. """
        super().__init__(*args, **kwargs)
        if self.instance.pk:  # Se for uma edição, carrega os programas já vinculados
            self.fields["programas"].initial = self.instance.programas.all()

    def clean_codigo_inep(self):
        """ Validação do Código INEP: Exatamente 10 dígitos numéricos """
        codigo_inep = self.cleaned_data.get("codigo_inep", "")
        if not codigo_inep.isdigit() or len(codigo_inep) != 10:
            raise forms.ValidationError("O Código INEP deve ter exatamente 10 dígitos numéricos.")
        return codigo_inep

    def clean_cnpj(self):
        """ Validação do CNPJ: Deve estar no formato 99.999.999/9999-99 """
        cnpj = self.cleaned_data.get("cnpj", "")
        cnpj_numerico = re.sub(r"[^\d]", "", cnpj)  # Remove pontos, barras e traços
        
        if len(cnpj_numerico) != 14 or not cnpj_numerico.isdigit():
            raise forms.ValidationError("CNPJ inválido! O formato correto é: 99.999.999/9999-99.")
        
        return cnpj
# *******************************************************************************************************************

from django import forms
from .models import Receita

class ReceitaForm(forms.ModelForm):
    class Meta:
        model = Receita
        fields = [
            "escola",
            "data_inicio",
            "data_fim",
            "saldo_anterior_custeio",
            "saldo_anterior_capital",
            "valor_creditado_custeio",
            "valor_creditado_capital",
            "recursos_proprios_custeio",  # ✅ Campo atualizado
            "recursos_proprios_capital",  # ✅ Campo atualizado
            "rendimento_aplicacao_custeio",
            "rendimento_aplicacao_capital",
            "devolucao_fnde_custeio",
            "devolucao_fnde_capital",
            "valor_total_receita_custeio",
            "valor_total_receita_capital",
            "valor_despesa_realizada_custeio",
            "valor_despesa_realizada_capital",
            "saldo_reprogramar_custeio",
            "saldo_reprogramar_capital",
            "saldo_devolvido_custeio",
            "saldo_devolvido_capital",
            "escolas_atendidas",
        ]
        widgets = {
            "escola": forms.Select(attrs={"class": "form-control"}),
            "data_inicio": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "data_fim": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "saldo_anterior_custeio": forms.NumberInput(attrs={"class": "form-control"}),
            "saldo_anterior_capital": forms.NumberInput(attrs={"class": "form-control"}),
            "valor_creditado_custeio": forms.NumberInput(attrs={"class": "form-control"}),
            "valor_creditado_capital": forms.NumberInput(attrs={"class": "form-control"}),
            "recursos_proprios_custeio": forms.NumberInput(attrs={"class": "form-control"}),  # ✅ Corrigido
            "recursos_proprios_capital": forms.NumberInput(attrs={"class": "form-control"}),  # ✅ Corrigido
            "rendimento_aplicacao_custeio": forms.NumberInput(attrs={"class": "form-control"}),
            "rendimento_aplicacao_capital": forms.NumberInput(attrs={"class": "form-control"}),
            "devolucao_fnde_custeio": forms.NumberInput(attrs={"class": "form-control"}),
            "devolucao_fnde_capital": forms.NumberInput(attrs={"class": "form-control"}),
            "valor_total_receita_custeio": forms.NumberInput(attrs={"class": "form-control"}),
            "valor_total_receita_capital": forms.NumberInput(attrs={"class": "form-control"}),
            "valor_despesa_realizada_custeio": forms.NumberInput(attrs={"class": "form-control"}),
            "valor_despesa_realizada_capital": forms.NumberInput(attrs={"class": "form-control"}),
            "saldo_reprogramar_custeio": forms.NumberInput(attrs={"class": "form-control"}),
            "saldo_reprogramar_capital": forms.NumberInput(attrs={"class": "form-control"}),
            "saldo_devolvido_custeio": forms.NumberInput(attrs={"class": "form-control"}),
            "saldo_devolvido_capital": forms.NumberInput(attrs={"class": "form-control"}),
            "escolas_atendidas": forms.NumberInput(attrs={"class": "form-control"}),
        }
# *******************************************************************************************************************

from django import forms
from .models import ReceitaDespesa

class ReceitaDespesaForm(forms.ModelForm):
    class Meta:
        model = ReceitaDespesa
        fields = [
            "escola",
            "periodo_execucao",
            "saldo_anterior_custeio",
            "saldo_anterior_capital",
            "valor_creditado_custeio",
            "valor_creditado_capital",
            "recursos_proprios_custeio",
            "recursos_proprios_capital",
            "rendimento_aplicacao_custeio",
            "rendimento_aplicacao_capital",
            "devolucao_fnde_custeio",
            "devolucao_fnde_capital",
            "saldo_reprogramar_custeio",
            "saldo_reprogramar_capital",
            "saldo_devolvido_custeio",
            "saldo_devolvido_capital",
            "total_receita",
            "total_despesa",
            "saldo_disponivel",
            "escolas_atendidas",
        ]
# *******************************************************************************************************************

from django import forms
from .models import LancamentoBancario

class LancamentoBancarioForm(forms.ModelForm):
    data = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"})
    )  # ✅ Garante que o campo "data" seja editável

    class Meta:
        model = LancamentoBancario
        fields = ["data", "descricao", "tipo", "categoria", "valor", "escola", "conta_bancaria"]  # 🔥 Removidos campos inexistentes
        widgets = {
            "descricao": forms.TextInput(attrs={"class": "form-control"}),
            "tipo": forms.Select(attrs={"class": "form-control"}),
            "valor": forms.NumberInput(attrs={"class": "form-control"}),
            "escola": forms.Select(attrs={"class": "form-control"}),  # 🔥 Corrigido para incluir "escola"
            "conta_bancaria": forms.Select(attrs={"class": "form-control"}),
        }
# *******************************************************************************************************************

from django import forms
from .models import ContaBancaria

class ContaBancariaForm(forms.ModelForm):
    class Meta:
        model = ContaBancaria
        fields = [
            'escola',
            'programa',
            'nome',
            'banco',
            'agencia',
            'conta',           # ✅ campo que agora será exibido normalmente
            'saldo',
            'tipo_conta'
        ]
        widgets = {
            'escola': forms.Select(attrs={'class': 'form-control'}),
            'programa': forms.Select(attrs={'class': 'form-control'}),
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Conta Principal'}),
            'banco': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Banco do Brasil'}),
            'agencia': forms.TextInput(attrs={'class': 'form-control'}),
            'conta': forms.TextInput(attrs={'class': 'form-control'}),
            'saldo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'tipo_conta': forms.Select(attrs={'class': 'form-control'}),
        }

# *******************************************************************************************************************

from django import forms
from .models import EscolaPdde, ContaBancaria

class ConferenciaForm(forms.Form):
    data_inicial = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    data_final = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    escola = forms.ModelChoiceField(queryset=EscolaPdde.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    conta = forms.ModelChoiceField(queryset=ContaBancaria.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    tipo_conferencia = forms.ChoiceField(
        choices=[
            ('extrato_vs_lancamentos', 'Extrato Bancário vs Lançamentos'),
            ('lancamentos_vs_pagamentos', 'Lançamentos vs Pagamentos Internos')
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
# *******************************************************************************************************************

from django import forms
from .models import Programa

class ProgramaForm(forms.ModelForm):
    class Meta:
        model = Programa
        fields = ["nome", "descricao", "resolucao", "data_inicio", "data_fim"]  # Removemos 'escola'
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "descricao": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "resolucao": forms.TextInput(attrs={"class": "form-control"}),
            "data_inicio": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "data_fim": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }
# *******************************************************************************************************************

from django import forms
from .models import EscolaPdde, Programa, CustomUserProf

class VincularEscolaProgramaForm(forms.Form):
    escola = forms.ModelChoiceField(
        queryset=EscolaPdde.objects.all(),
        label="Escolha a Escola"
    )
    programas = forms.ModelMultipleChoiceField(
        queryset=Programa.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Programas"
    )
    coordenador = forms.ModelChoiceField(
        queryset=CustomUserProf.objects.filter(is_coordenador=True),
        required=False,
        label="Coordenador Responsável"
    )



# *******************************************************************************************************************
# ***************************************************PESQUISA DE PREÇOS**********************************************
# *******************************************************************************************************************

from django import forms
from .models import Item, Proponente, Proposta

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'

from django import forms
from .models import Proponente

class ProponenteForm(forms.ModelForm):
    class Meta:
        model = Proponente
        fields = [
            "nome", "cpf_cnpj", "email", "telefone", "endereco",
            "bairro", "cidade", "estado", "cep", "tipo_proponente",
            "representante_legal", "observacoes"
        ]
        widgets = {
            "observacoes": forms.Textarea(attrs={"rows": 3}),
            "tipo_proponente": forms.Select(),
            "estado": forms.Select(),
        }
# *******************************************************************************************************************

class PropostaForm(forms.ModelForm):
    class Meta:
        model = Proposta
        fields = '__all__'

# *******************************************************************************************************************

from django import forms
from .models import Documento

class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ["escola", "tipo", "numero", "data_emissao", "arquivo"]
        widgets = {
            'escola': forms.Select(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'data_emissao': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'arquivo': forms.FileInput(attrs={'class': 'form-control'}),
        }
# *******************************************************************************************************************

from .models import BemAdquirido

class BemAdquiridoForm(forms.ModelForm):
    class Meta:
        model = BemAdquirido
        fields = ["documento", "especificacao", "quantidade", "valor_unitario"]
        widgets = {
            'documento': forms.Select(attrs={'class': 'form-control'}),
            'especificacao': forms.TextInput(attrs={'class': 'form-control'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control'}),
            'valor_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
# *******************************************************************************************************************

from django import forms
from .models import RepresentanteLegal

class RepresentanteLegalForm(forms.ModelForm):
    class Meta:
        model = RepresentanteLegal
        exclude = ['escola']  # Remove o campo escola do formulário
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'cargo': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
        }

# *******************************************************************************************************************

from .models import Bem

class BemForm(forms.ModelForm):
    class Meta:
        model = Bem
        fields = ['escola', 'nome_conselho', 'nome', 'documento', 'quantidade', 'valor_unitario']
        widgets = {
            'escola': forms.Select(attrs={'class': 'form-control'}),
            'nome_conselho': forms.TextInput(attrs={'class': 'form-control'}),
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'documento': forms.Select(attrs={'class': 'form-control'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control'}),
            'valor_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
# *******************************************************************************************************************

# forms.py
from django import forms
from .models import TermoDoacao, EscolaPdde

class TermoDoacaoForm(forms.ModelForm):
    class Meta:
        model = TermoDoacao
        fields = ['escola', 'conselho', 'bem']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Estilo Bootstrap para todos os campos
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        # Lógica de filtragem por usuário
        if user:
            if user.is_superuser:
                self.fields['escola'].queryset = EscolaPdde.objects.all()
            elif hasattr(user, 'escolas'):
                self.fields['escola'].queryset = user.escolas.all()



# *******************************************************************************************************************

from .models import BemDoado

class BemDoadoForm(forms.ModelForm):
    class Meta:
        model = BemDoado
        fields = ['escola', 'conselho', 'descricao', 'quantidade', 'numero_nota', 'data_nota', 'valor_unitario']
        widgets = {
            'escola': forms.Select(attrs={'class': 'form-control'}),
            'conselho': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control'}),
            'numero_nota': forms.TextInput(attrs={'class': 'form-control'}),
            'data_nota': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'valor_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
# *******************************************************************************************************************

from django import forms
from .models import PlanoGestaoEscolar

class PlanoGestaoEscolarForm(forms.ModelForm):
    class Meta:
        model = PlanoGestaoEscolar
        fields = ['unidade_ensino', 'cargo', 'servidor', 'telefone', 'arquivo']
        widgets = {
            'unidade_ensino': forms.TextInput(attrs={'class': 'form-control'}),
            'cargo': forms.TextInput(attrs={'class': 'form-control'}),
            'servidor': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'arquivo': forms.FileInput(attrs={'class': 'form-control'}),
        }
# *******************************************************************************************************************
from django.utils.html import strip_tags


def clean_descricao(self):
    data = self.cleaned_data['descricao']
    return strip_tags(data)


from django import forms
from .models import EscolaPdde

class TrocarEscolaForm(forms.Form):
    nova_escola = forms.ModelChoiceField(
        queryset=EscolaPdde.objects.all(),
        label="Selecione a nova escola",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
