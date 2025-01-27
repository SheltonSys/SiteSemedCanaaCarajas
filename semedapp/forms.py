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

class LivroCaixaForm(forms.ModelForm):
    class Meta:
        model = LivroCaixa
        fields = ['descricao', 'tipo', 'valor']
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control'}),
        }
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

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nome', 'email', 'senha']
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

class ProfessorForm(forms.ModelForm):
    class Meta:
        model = Professor
        fields = [
            'nome_completo', 'cpf', 'rg', 'email', 'telefone', 'endereco', 'bairro', 'cidade',
            'cep', 'estado_civil', 'sexo', 'data_nascimento', 'formacao_academica', 'curso',
            'instituicao', 'ano_conclusao', 'foto', 'curriculo_pdf', 'certificados_pdf',
            'experiencia_profissional'
        ]
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


from django import forms
from .models import Candidato  # Certifique-se de que o modelo Candidato existe

class FormDeAtualizacao(forms.ModelForm):
    class Meta:
        model = Candidato  # Substitua por seu modelo
        fields = ['nome_completo', 'email', 'cpf']  # Ajuste os campos conforme necessário
