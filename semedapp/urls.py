from django.urls import include, path
from django.shortcuts import render
from . import views
from django.views.generic import TemplateView
from .views import configure_access_view
from .views import configure_access_view, configuracao_view, indicadores_view
from .views import access_user_modules
from .views import dashboard_view
from .views import configure_user_modules
# Remova 'logout_confirm' das importações
from .views import home, eja_cadastro, CustomLoginView, logout_view, cadastro_usuario, verificar_cpf_ajax, area_do_candidato
from django.conf import settings
from django.conf.urls.static import static
from .views import logout_view
from .views import logout_confirm
from .views import admin_login_view
from .views import (
    aluno_matematica_view,
    get_diagnose_data_inic_alunos_matematica,
    upload_excel_aluno_matematica
)
from .views import (
    registrar_curriculo,
    listar_curriculos,
    cadastrar_curriculo,
    curriculo_sucesso,
    CurriculoCreateView,
)
from .views import (
    conciliacao_extrato,
    conciliacao_lancamento,
    conciliacao_saldo,
    conciliacao_conferencia,
    conciliacao_relatorios,
)
from .views import habilidades_matematica_view
from .views import habilidades_pesquisa_view
from semedapp.views import dashboard_transporte
from .views import get_articles_data
from django.urls import path
from semedapp import views  # Substitua 'semedapp' pelo nome do seu app
from semedapp.views import login_candidato
from .views import CurriculoCreateView
from semedapp.views import editar_curriculo
from semedapp.views import visualizar_curriculo
from semedapp.views import editar_perfil
from django.contrib.auth.views import LogoutView
from .views import recuperar_senha, resetar_senha
from semedapp.views import enviar_link_recuperacao  # Importe a view correta
from .views import enviar_email_recuperacao
from .views import listar_curriculos_antigos
from .views import educacao_infantil
from .views import upload_cadastro_ei
from .views import cadastro_escola, excluir_escola  # Importa as views necessárias
from .views import editar_escola
from .views import cadastro_escola, get_turmas
from .views import cadastro_turma, get_turmas
from .views import cadastro_turma, editar_turma
from .views import visualizar_avaliacao
from .views import salvar_avaliacao
from .views import gestao_relatorios, get_turmas
from .views import lancamento_conceitos
from .views import gestao_relatorios, gerar_pdf_relatorio
from .views import buscar_turmas
from .views import ocorrencias_synaptic, ocorrencias_synaptic_pdf
from .views import ocorrencias_autokee
from .views import ocorrencias_orientadores
from .views import login_prof, logout_prof
from .views import login_prof, modulo_pedagogico
from .views import carregar_turmas_por_escola
from semedapp.views import editar_curriculo
from .views import imprimir_curriculo_alternativo
from .views import imprimir_curriculo_alternativo
from .views import listar_diretores
from .views import EscolaPddeListView, EscolaPddeCreateView, EscolaPddeDeleteView, EscolaPddeDetailView, EscolaPddeUpdateView
from .views import get_escola_pdde
from .views import get_escola_pdde_modal
from .views import EscolaPddeModalView
from .views import get_escola_pdde, get_receita_despesa
from .views import pddereceita_despesa_view
from .views import get_pagamentos
from .views import pdde_list
from .views import get_dados_financeiros
from .views import lancamento_pagamento
from .views import get_pagamentos_pdde
from .views import get_dados_pagamentos_pdde
from .views import pddelancar_pagamento
from .views import get_escolas
from .views import pdde_gerar_pdf
from .views import listar_lancamentos, criar_lancamento, editar_lancamento, excluir_lancamento
from .views import conciliacao_lancamento, editar_lancamento
from .views import listar_pdde
from .views import criar_conta_bancaria, listar_contas
from .views import listar_contas, excluir_conta
from .views import get_escolas, get_contas_por_escola
from .views import consultar_saldo, api_escolas, api_contas, api_saldos
from .views import api_escolas, api_contas, api_conferencia
from .views import api_extrato
from .views import listar_programas, criar_programa
from .views import cadastrar_programa
from .views import listar_escolas
from .views import editar_escola_pdde
from .views import get_programas_vinculados
from .views import vincular_escola_programa
from semedapp.views import get_programas_escola
from semedapp.views import get_programas_por_escola
from .views import listar_programas_por_escola  # Importa a função correta da view
from .views import get_dados_receita_despesa_pdde
from .views import get_dados_receita
from .views import get_receita, get_pagamentos
from .views import pddelancar_pagamento, editar_pagamento  # Certifique-se de importar a view correta
from .views import editar_conta
from .views import emitir_conciliacao, gerar_conciliacao_pdf
from .views import cadastrar_propostas  # Importe a view corretamente
from .views import apuracao_resultados
from .views import (
    pesquisa_precos, cadastrar_item, cadastrar_proponente, listar_proponentes,
    cadastrar_propostas, apuracao_resultado, get_subcategorias, listar_itens,
    gerar_pdf_orcamento, gerar_excel_orcamento, cadastrar_subcategoria, cadastrar_categoria
)

from .views import apuracao_resultados_view, detalhes_proponente
from .views import cadastrar_documento, cadastrar_bem, cadastrar_representante
from .views import gerar_prestacao_contas_pdf
from .views import listar_documentos, cadastrar_documento  # ✅ Importe a função correta
from .views import cadastrar_bem, listar_bens
from .views import get_escola_dados
from .views import enviar_plano_gestao
from .views import listar_pge_planos
from .views import plano_gestao_escolar_admin
from .views import gerar_cotacao
from semedapp.views import relatorio_saida_rede
from .views import gerar_pdf_saida_rede
from .views import exportar_pptx_saida_rede
from .views import gerar_pdf_relatorio_geral
from .views import relatorio_saida_matematica_view





from .views import (
    pddereceita_despesa, 
    pddelancar_receita, 
    pddelancar_despesa, 
    pddelancar_pagamento
)

# app_name = 'contabilidade'
# app_name = 'banco_curriculos'

urlpatterns = [

    path("banco-curriculos/login-curriculo/", views.login_candidato, name="login_candidato"),

    path("banco-curriculos/area-candidato/", views.area_candidato, name="area_candidato"),  # Área de candidato

    path('', home, name='home'),  # Configuração correta do URL
    # Página Inicial
    path('', views.BASE, name='BASE'),  # Página inicial do sistema
    path('index/', TemplateView.as_view(template_name='index.html'), name='index'),  # Página principal do site Semed
    # path('login/', CustomLoginView.as_view(), name='login'),
    path('logout-confirm/', logout_confirm, name='logout_confirm'),
    # Dashboard
    path('dashboardadmin/', views.dashboard_admin, name='dashboardadmin'),
    # Configuração Geral
    path('definir-permissoes/', views.definir_permissoes, name='definir_permissoes'),
    path('vinculacoes/', views.vinculacoes, name='vinculacoes'),
    path('controle-usuarios/', views.controle_usuarios, name='controle_usuarios'),
    path('adicionar-usuario/', views.adicionar_usuario, name='adicionar_usuario'),
    # Indicadores
    path('indicadores/', TemplateView.as_view(template_name='indicadores.html'), name='indicadores'),
    path('indicadores/transporte/', views.transporte_indicadores, name='indicadores_transporte'),
    path('indicadores/upload/', views.upload_arquivos, name='indicadores_upload'),
    path('indicadores/gestao/', views.gestao_dados, name='indicadores_gestao'),
    # Pedagógico
    path('pedagogico/', views.pedagogico, name='pedagogico'),
    path('pedagogico/diagnosis/', views.diagnosis, name='pedagogico_diagnosis'),
    path('pedagogico/orientacao/', views.orientacao_educacional, name='pedagogico_orientacao'),
    path('pedagogico/legislacao/', views.legislacao, name='pedagogico_legislacao'),
    # Contabilidade
    path('contabilidade/', views.contabilidade, name='contabilidade'),
    path('contabilidade/escolas/', views.escolas, name='contabilidade_escolas'),
    path('contabilidade/conselho/', views.conselho, name='contabilidade_conselho'),
    path('contabilidade/contas/', views.contas, name='contabilidade_contas'),
    # Transporte
    path('transporte/', views.transporte, name='transporte'),
    path('transporte/dashboard/', views.transporte_dashboard, name='transporte_dashboard'),
    path('transporte/escolar/', views.transporte_escolar, name='transporte_escolar'),

    # Banco de Currículos
    path('site-curriculos/', views.site_curriculos, name='site_curriculos'),
    path('cadastro-curriculo/', views.cadastro_curriculo, name='cadastro_curriculo'),
    path('gestao-curriculo/', views.gestao_curriculo, name='gestao_curriculo'),
    path('gestao-conteudo/', views.gestao_conteudo, name='gestao_conteudo'),
    
    path('registrar/', views.registrar_curriculo, name='registrar_curriculo'),
    path('curriculos/', views.listar_curriculos, name='curriculos'),

    # Site Semed
    path('site-semed/', TemplateView.as_view(template_name='sitesemed.html'), name='site_semed'),
    # Outros
    path('logout/', logout_view, name='logout'),
    path('logout/', views.logout_view, name='logout'),
    path('upload/', views.upload_arquivos, name='upload'),

    path('gestao-escolar/', views.gestao_escolar, name='gestao_escolar'),  # Defina a rota e nomeie-a como 'gestao_escolar'
    path('financeiro/', views.financeiro, name='financeiro'),  # Certifique-se de adicionar esta linha
    path('soe/', views.soe, name='soe'),  # Adicione esta linha
    path('legislacao/', views.legislacao, name='legislacao'),  # Adicione esta linha
    path('upload-arquivos/', views.upload_arquivos, name='upload_arquivos'),  # Adicione esta linha
    path('gestao-dados/', views.gestao_dados, name='gestao_dados'),  # Adicione esta linha
    path('diagnosis/', views.diagnosis, name='diagnosis'),  # Definição correta da rota
    path('orientacao-educacional/', views.orientacao_educacional, name='orientacao_educacional'),
    path('escolas/', views.escolas, name='escolas'),  # Adicione esta linha
    path('conselho/', views.conselho, name='conselho'),  # Adicione esta linha
    path('contas/', views.contas, name='contas'),  # Rota para Contas

    path('cadastro-imagens/', views.cadastro_imagens, name='cadastro_imagens'),
    path('cadastro-conteudo/', views.cadastro_conteudo, name='cadastro_conteudo'),
    path('gestao-noticias/', views.gestao_noticias, name='gestao_noticias'),
    path('gestao-eventos/', views.gestao_eventos, name='gestao_eventos'),
    path('configuracoes-site/', views.configuracoes_site, name='configuracoes_site'),
    path('estatisticas-site/', views.estatisticas_site, name='estatisticas_site'),
    path('gestao-usuarios-site/', views.gestao_usuarios_site, name='gestao_usuarios_site'),
    path('gestao-processos/', views.gestao_processos, name='gestao_processos'),
    path('relatorios/', views.relatorios, name='relatorios'),

    path('setor-pedagogico/', views.setor_pedagogico, name='setor_pedagogico'),
    path('setor-pedagogico/gestao-habilidades/', views.gestao_habilidades, name='gestao_habilidades'),
    path('setor-pedagogico/indicadores-educacionais/', views.indicadores_educacionais, name='indicadores_educacionais'),
    path('setor-pedagogico/relatorios-pedagogicos/', views.relatorios_pedagogicos, name='relatorios_pedagogicos'),

    path('setor-pedagogico/indicadores/', views.indicadores_setor_pedagogico, name='indicadores_setor_pedagogico'),

    path('diagnosis/prof/portugues/', views.diagnosis_prof_portugues, name='diagnosis_prof_portugues'),
    path('diagnosis/prof/matematica/', views.diagnosis_prof_matematica, name='diagnosis_prof_matematica'),
    path('diagnosis/aluno/portugues/', views.diagnosis_aluno_portugues, name='diagnosis_aluno_portugues'),
    path('diagnosis/aluno/matematica/', views.diagnosis_aluno_matematica, name='diagnosis_aluno_matematica'),
    path('diagnosis/eja/site/', views.diagnosis_eja_site, name='diagnosis_eja_site'),
    path('diagnosis/eja/adm/', views.diagnosis_eja_adm, name='diagnosis_eja_adm'),
    path('diagnosis/eja/admin/noticias/', views.admin_eja_noticias, name='admin_eja_noticias'),
    path('diagnosis/eja/admin/eventos/', views.admin_eja_eventos, name='admin_eja_eventos'),
    path('diagnosis/eja/admin/relatorios/', views.admin_eja_relatorios, name='admin_eja_relatorios'),
    path('diagnosis/eja/admin/', views.admin_site_eja, name='admin_site_eja'),
    path('diagnosis/emcceja/', views.diagnosis_emcceja, name='diagnosis_emcceja'),

    path('gerenciar_permissoes/', views.gerenciar_permissoes, name='gerenciar_permissoes'),
    path('manage_permissions/', views.manage_permissions, name='manage_permissions'),  # Adicione esta linha
    path('edit_permissions/<int:user_id>/', views.edit_permissions, name='edit_permissions'),
    path('add_user/', views.add_user, name='add_user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),

    path('add-group/', views.add_group, name='add_group'),
    path('add-permission/', views.add_permission, name='add_permission'),
    path('configurar_acesso/', configure_access_view, name='configure_access'),

    # Páginas dos módulos
    path('configuracao/', configuracao_view, name='configuracao'),
    path('indicadores/', indicadores_view, name='indicadores'),
    # Página de acesso negado
    path('no_access/', lambda request: render(request, 'no_access.html'), name='no_access'),
    path('acessar_modulos/<int:user_id>/', views.access_user_modules, name='access_user_modules'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('configurar_modulos/<int:user_id>/', configure_user_modules, name='configure_user_modules'),
    path('curriculos/', views.curriculos_view, name='curriculos'),
    path('modulo/<slug:slug>/', views.modulo_view, name='nome_da_view_modulo'),

    path('update-habilidades/', views.update_habilidades, name='update_habilidades'),
    path('relatorios/download/<str:tipo_relatorio>/', views.download_relatorio, name='download_relatorio'),
    path('agenda-educacional/', views.agenda_educacional, name='agenda_educacional'),
    path('acompanhamento-individual/', views.acompanhamento_individual, name='acompanhamento_individual'),
    path('registrar-acompanhamento/', views.registrar_acompanhamento, name='registrar_acompanhamento'),

    path('cadastro_diretoria/', views.cadastro_diretoria, name='cadastro_diretoria'),
    path('conselho/diretoria/editar/<int:id>/', views.editar_diretoria, name='editar_diretoria'),
    path('conselho/diretoria/excluir/<int:id>/', views.excluir_diretoria, name='excluir_diretoria'),

    path('contabilidade/pdde/', views.pdde_view, name='contabilidade_pdde'),
    path('conselho/diretoria/', views.conselho_diretoria, name='conselho_diretoria'),
    path('conselho/membros/', views.conselho_membros, name='conselho_membros'),
    path('conselho/membros/cadastrar/', views.cadastrar_membro, name='cadastrar_membro'),
    path('conselho/membros/', views.listar_membros, name='listar_membros'),
    path('conselho/membros/editar/<int:id>/', views.editar_membro, name='editar_membro'),
    path('conselho/membros/excluir/<int:id>/', views.excluir_membro, name='excluir_membro'),

    #livro caixa
    path('download/<str:file_name>/', views.download_manual, name='download_manual'),

    path('livro-caixa/', views.listar_livro_caixa, name='listar_livro_caixa'),
    path('livro-caixa/cadastrar/', views.adicionar_livro_caixa, name='adicionar_livro_caixa'),
    path('livro-caixa/editar/<int:id>/', views.editar_livro_caixa, name='editar_livro_caixa'),
    path('livro-caixa/excluir/<int:id>/', views.excluir_livro_caixa, name='excluir_livro_caixa'),
    path('livro-caixa/escola-info/<int:escola_id>/', views.escola_info, name='get_escola_info'),





    path('pdde/', views.pdde, name='contabilidade_pdde'),
    path('pdde/', views.pdde_view, name='pdde'),
    path('pdde/<int:pdde_id>/', views.view_pdde, name='view_pdde'),
    path('download/<str:file_name>/', views.download_manual, name='download_manual'),
    path("cadastro_diretoria/", views.cadastro_diretoria, name="cadastro_diretoria"),
    # Listar o Livro Caixa
    path('contabilidade/caixa/', views.listar_livro_caixa, name='listar_livro_caixa'),
    path('contabilidade/caixa/adicionar/', views.adicionar_escritura_fiscal, name='adicionar_escritura_fiscal'),
    path('contabilidade/caixa/adicionar/', views.adicionar_escritura_fiscal, name='adicionar_escrituracao'),

    

    path('caixa/adicionar/', views.adicionar_escrituracao, name='adicionar_escrituracao'),
    path('gestao_escolar/', views.gestao_escolar, name='gestao_escolar'),
    path('downloads/', views.download_page, name='download_page'),
    path('downloads/manual/<str:file_name>/', views.download_manual, name='download_manual'),

    path('relatorios/pdde/', views.listar_relatorios_pdde, name='listar_livro_caixa'),

    path('emissao-certidoes/', views.emissao_certidoes, name='emissao_certidoes'),

    path('dashboard/', views.dashboard, name='seppec_dashboard'),
    path('dashboard/', views.dashboard_view, name='escolas'),

    path('documentos/', views.listar_documentos, name='listar_documentos'),
    path('categorias/', views.gerenciar_categorias, name='gerenciar_categorias'),
    path('relatorio-atualizacoes/', views.relatorio_atualizacoes, name='relatorio_atualizacoes'),
    path('legislacao/adicionar/', views.adicionar_legislacao, name='adicionar_legislacao'),

    path('planetario/', views.planetario, name='planetario'),
    path('planetario/inscricao/', views.planetario_inscricao, name='planetario_inscricao'),
    # Gestão de Imagens
    path('imagens/', views.gerenciar_imagens, name='gerenciar_imagens'),
    path('imagens/adicionar/', views.adicionar_imagem, name='adicionar_imagem'),
    path('cadastro-imagens/', views.cadastro_imagens, name='cadastro_imagens'),

    path('adicionar-imagem/', views.adicionar_imagem, name='adicionar_imagem'),
    path('galeria-imagens/', views.lista_imagens, name='lista_imagens'),
    path('galeria/', views.galeria, name='galeria'),
    path('galeria/adicionar/', views.adicionar_imagem, name='adicionar_imagem'),
    # Gestão de Conteúdo
    path('conteudo/', views.gerenciar_conteudo, name='gerenciar_conteudo'),
    path('conteudo/adicionar/', views.adicionar_conteudo, name='adicionar_conteudo'),
    path('cadastro-conteudo/', views.cadastro_conteudo, name='cadastro_conteudo'),
    path('gestao-conteudo/', views.gestao_conteudo, name='gestao_conteudo'),
    # Gestão de Eventos
    path('eventos/', views.gerenciar_eventos, name='gerenciar_eventos'),
    path('eventos/adicionar/', views.adicionar_evento, name='adicionar_evento'),
    path('gestao-eventos/', views.gestao_eventos, name='gestao_eventos'),
    # Gestão de Usuários
    path('usuarios/', views.gerenciar_usuarios, name='gerenciar_usuarios'),
    path('usuarios/adicionar/', views.adicionar_usuario, name='adicionar_usuario'),
    path('gestao-usuarios/', views.gestao_usuarios_site, name='gestao_usuarios_site'),

    path('gestao-noticias/', views.gestao_noticias, name='gestao_noticias'),
    path('configuracoes-site/', views.configuracoes_site, name='configuracoes_site'),
    path('estatisticas-relatorios/', views.estatisticas_site, name='estatisticas_site'),

    path('apresentacao/', views.apresentacao, name='apresentacao'),  # Apresentação
    path('atribuicoes/', views.atribuicoes, name='atribuicoes'),    # Atribuições
    path('contatos/', views.contatos, name='contatos'),  # Contatos

    path('organograma/', views.organograma, name='organograma'),

    path('escolas/', views.escolas, name='escolas'),
    path('escola/', views.escola, name='escola'),
    path('centro-viver-e-conviver/', views.centro_viver_conviver, name='centro_viver_conviver'),
    path('centro-formacao/', views.centro_formacao, name='centro_formacao'),
    path('diretoria-ensino-superior/', views.diretoria_ensino_superior, name='diretoria_ensino_superior'),
    path('centro-midias-educacionais/', views.centro_midias_educacionais, name='centro_midias_educacionais'),

    path('conselho-municipal-educacao/', views.conselho_municipal_educacao, name='conselho_municipal_educacao'),
    path('cacs-fundeb/', views.cacs_fundeb, name='cacs_fundeb'),
    path('conselho-alimentacao-escolar/', views.conselho_alimentacao_escolar, name='conselho_alimentacao_escolar'),
    path('forum-municipal-educacao/', views.forum_municipal_educacao, name='forum_municipal_educacao'),

    path('faleconosco/', views.fale_conosco, name='fale_conosco'),

    path('repositorio/', views.repositorio, name='repositorio'),
    path('curriculo-ensino/', views.curriculo_ensino, name='curriculo_ensino'),
    path('programas-projetos/', views.programas_projetos, name='programas_projetos'),
    path('calendario-escolar/', views.calendario_escolar, name='calendario_escolar'),
    path('portal-aluno/', views.portal_aluno, name='portal_aluno'),
    path('sige/', views.sige, name='sige'),
    path('consulta-publica/', views.consulta_publica, name='consulta_publica'),

    path('jornal-escolar/', views.jornal_escolar, name='jornal_escolar'),
    path('noticia-unifesspa/', views.noticia_unifesspa, name='noticia_unifesspa'),
    path('noticia-eja/', views.noticia_eja, name='noticia_eja'),
    path('noticia-planetario/', views.noticia_planetario, name='noticia_planetario'),

    path('programas-projetos/', views.programas_projetos, name='programas_projetos'),
    path('portal-aluno/', views.portal_aluno, name='portal_aluno'),

    path('escolas/emeb-gercino-correa/', views.emeb_gercino_correa, name='emeb_gercino_correa'),
    path('escolas/emeb-luis-carlos-prestes/', views.emeb_luis_carlos_prestes, name='emeb_luis_carlos_prestes'),
    path('escola/emeb-ronilton-aridal/', views.emeb_ronilton, name='emeb_ronilton'),
    path('emef-alexandro-nunes/', views.emef_alexandro_nunes, name='emef_alexandro_nunes'),
    path('escolas/emef-benedita-torres/', views.emef_benedita_torres, name='emef_benedita_torres'),
    path('emef_carmelo_mendes/', views.emef_carmelo_mendes, name='emef_carmelo_mendes'),
    path('emef_francisca_romana/', views.emef_francisca_romana, name='emef_francisca_romana'),
    path('escolas/emef_joao_nelson/', views.emef_joao_nelson, name='emef_joao_nelson'),
    path('escolas/emef_maria_lourdes/', views.emef_maria_lourdes, name='emef_maria_lourdes'),
    path('escolas/sebastiao_agripino/', views.sebastiao_agripino, name='sebastiao_agripino'),
    path('adelaide-molinari/', views.adelaide_molinari, name='adelaide_molinari'),
    path('carlos-henrique/', views.carlos_henrique, name='carlos_henrique'),
    path('escolas/juscelino_kubitschek/', views.juscelino_kubitschek, name='juscelino_kubitschek'),
    path('escola/magalhaes_barata/', views.magalhaes_barata, name='magalhaes_barata'),
    path('emeif-magalhaes-barata/', views.emeif_magalhaes_barata, name='emeif_magalhaes_barata'),
    path('emeif-raimundo-oliveira/', views.emeif_raimundo_oliveira, name='emeif_raimundo_oliveira'),
    path('escola/tancredo_almeida/', views.tancredo_almeida, name='tancredo_almeida'),
    path('escolas/teotonio_vilela/', views.teotonio_vilela, name='teotonio_vilela'),
    path('escolas/<int:escola_id>/', views.detalhes_escola, name='detalhes_escola'),
    path('escolas/adicionar/', views.adicionar_escola, name='adicionar_escola'),

    path('agenda/', views.agenda_view, name='agenda'),
    path('inscricoes/', views.inscricoes_view, name='inscricoes'),
    path('certificado/', views.certificado_view, name='certificado'),
    path('encontro-pedagogico/', views.encontro_pedagogico, name='encontro_pedagogico'),

    path('noticia/unifesspa/', views.noticia_unifesspa, name='noticia_unifesspa'),
    path('noticia/eja/', views.noticia_eja, name='noticia_eja'),
    path('noticia/planetario/', views.noticia_planetario, name='noticia_planetario'),

    path('site-pedagogico/', views.site_pedagogico, name='site_pedagogico'),
    path('verificar-cpf/', views.verificar_cpf_ajax, name='verificar_cpf_ajax'),
    path('admin-login/', admin_login_view, name='admin_login'),
    path('adm-site-pedagogico/', views.adm_site_pedagogico, name='adm_site_pedagogico'),
    path('upload-arquivo/', views.upload_arquivo, name='upload_arquivo'),
    path('cadastro-usuario/', cadastro_usuario, name='cadastro_usuario'),
    path('eja_cadastro/', eja_cadastro, name='eja_cadastro'),
    path('area-do-candidato/', area_do_candidato, name='area_do_candidato'),
    path('get-diagnose-data/', views.get_diagnose_data, name='get_diagnose_data'),

    path('matematica-aluno/dados/', get_diagnose_data_inic_alunos_matematica, name='get_diagnose_data_inic_alunos_matematica'),
    path('get-diagnose-data-inic-alunos-port/', views.get_diagnose_data_inic_alunos_port, name='get_diagnose_data_inic_alunos_port'),
    path('habilidades/portugues/', views.habilidades_portugues_view, name='habilidades_portugues_view'),
    path('habilidades/matematica/', views.habilidades_matematica_view, name='habilidades_matematica_view'),
    path('conselho/planetario/habilidades/portugues/', views.habilidades_portugues_view, name='habilidades_portugues'),

    path('conselho/planetario/habilidades/matematica/', habilidades_matematica_view, name='habilidades_matematica'),
    path('upload_arquivos/', views.upload_arquivos, name='upload_arquivos'),
    path('conselho/planetario/habilidades/pesquisa/', habilidades_pesquisa_view, name='habilidades_pesquisa'),


    path('lingua-portuguesa-alunos-iniciais/', views.lingua_portuguesa_alunos_iniciais, name='lingua_portuguesa_alunos_iniciais'),
    path('lingua-portuguesa-professores-iniciais/', views.lingua_portuguesa_professores_iniciais, name='lingua_portuguesa_professores_iniciais'),
    path('lingua-matematica-alunos-iniciais/', views.lingua_matematica_alunos_iniciais, name='lingua_matematica_alunos_iniciais'),
    path('lingua-matematica-professores-iniciais/', views.lingua_matematica_professores_iniciais, name='lingua_matematica_professores_iniciais'),
    path('lingua-portuguesa-alunos-finais/', views.lingua_portuguesa_alunos_finais, name='lingua_portuguesa_alunos_finais'),
    path('lingua-portuguesa-professores-finais/', views.lingua_portuguesa_professores_finais, name='lingua_portuguesa_professores_finais'),
    path('lingua-matematica-alunos-finais/', views.lingua_matematica_alunos_finais, name='lingua_matematica_alunos_finais'),
    path('lingua-matematica-professores-finais/', views.lingua_matematica_professores_finais, name='lingua_matematica_professores_finais'),

    path('dashboard/transporte/', dashboard_transporte, name='dashboard_transporte'),
    path('transporte/', dashboard_transporte, name='dashboard_transporte'),
    path('api/transporte-dados/', views.transporte_dados_api, name='transporte_dados_api'),
    path('transporte-escolar/', views.transporte_escolar, name='transporte_escolar'),

    path('planejamento/', views.planejamento, name='planejamento'),
    path('execucao/', views.execucao, name='execucao'),
    path('controle/', views.controle, name='controle'),
    path('comunicacao/', views.comunicacao, name='comunicacao'),

    path('quem-somos/', views.quem_somos, name='quem_somos'),
    path('missao-visao/', views.missao_visao, name='missao_visao'),
    path('equipe/', views.equipe, name='equipe'),
    path('projetos-especiais/', views.projetos_especiais, name='projetos_especiais'),
    path('contato-pedagogico/', views.contato_pedagogico, name='contato_pedagogico'),

    path('consulta_publica/', views.consulta_publica, name='consulta_publica'),
    path('painel/', views.painel_administrativo, name='painel_administrativo'),
    path('api/articles/', views.get_articles_data, name='get_articles_data'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('get-articles-data/', views.get_articles_data, name='get_articles_data'),
    path('site-pedagogico/', views.site_pedagogico_view, name='site_pedagogico'),

    path('vagas/', lambda request: render(request, 'banco_curriculos/vagas.html'), name='vagas'),
    path('login_curriculo/', lambda request: render(request, 'banco_curriculos/login.html'), name='login_curriculo'),
    path('curriculos/', views.curriculos, name='curriculos'),
    path('registrar/', views.registrar_view, name='registrar'),  # Nome da URL 'registrar'
    # Página Home específica para banco de currículos
    path('banco_curriculos/', views.banco_curriculos_home, name='banco_curriculos_home'),
    path('site-curriculos/', views.site_curriculos, name='site_curriculos'),

    path('upload-prof/', views.upload_planilha_prof, name='upload_planilha_prof'),
    path('habilidades-listar/', views.listar_habilidades_prof, name='listar_habilidades_prof'),
    path('habilidade-prof-iniciais/', views.habilidade_prof_view, name='habilidade_prof_view'),
    path('habilidade-prof-finais/', views.habilidade_prof_anos_finais_view, name='habilidade_prof_anos_finais_view'),
    path('portugues-finais/', views.portugues_final_view, name='diagnosis_prof_portugues_finais'),
    path('carregar-habilidades/<str:tipo>/', views.carregar_habilidades, name='carregar_habilidades'),

    path('tipo-demandas/', views.tipo_demandas, name='tipo_demandas'),  # Cadastro Tipo Demandas
    path('cadastro-demandas/', views.cadastro_demandas, name='cadastro_demandas'),  # Cadastro Demandas
    path('gestao-demandas/', views.gestao_demandas, name='gestao_demandas'),  # Gestão de Demandas
    path('relatorios-demandas/', views.relatorios_demandas, name='relatorios_demandas'),  # Relatórios de Demanda
    path('criar-demanda/', views.criar_demanda, name='criar_demanda'),
    path('editar-demanda/<int:id>/', views.editar_demanda, name='editar_demanda'),
    path('excluir-demanda/<int:id>/', views.excluir_demanda, name='excluir_demanda'),
    path('editar-demanda/<int:id>/', views.editar_demanda, name='editar_demanda'),
    path('listar-demandas/', views.listar_demandas, name='listar_demandas'),

    path('criar-tipo-demanda/', views.criar_tipo_demanda, name='criar_tipo_demanda'),
    path('relatorio-pdf/', views.gerar_relatorio_pdf, name='relatorio_pdf'),

    path('conselho/planetario/gestao-curriculo/', views.listar_curriculos, name='gestao_curriculos'),

    path('cadastrar/', views.cadastrar_curriculo, name='cadastrar_curriculo'),

    path('registrar/', registrar_curriculo, name='registrar_curriculo'),
    # path('curriculos/', listar_curriculos, name='listar_curriculos'),
    path('cadastrar/', cadastrar_curriculo, name='cadastrar_curriculo'),
    path('sucesso/', curriculo_sucesso, name='curriculo_sucesso'),
    path('novo/', CurriculoCreateView.as_view(), name='curriculo_create'),

    path('escolas/<int:id>/editar/', views.editar_escola, name='editar_escola'),
    path('adicionar-escola/', views.adicionar_escola, name='adicionar_escola'),
    
    path('curriculo-sucesso/', views.curriculo_sucesso, name='curriculo_sucesso'),
    path('curriculo/create/', CurriculoCreateView.as_view(), name='curriculo-create'),
    path('gestao-curriculos/', views.listar_curriculos, name='gestao_curriculos'),

    path('curriculos/', views.listar_curriculos, name='listar_curriculos'),
    path('curriculos/<int:id>/imprimir/', views.imprimir_curriculo, name='imprimir_curriculo'),

    path('listar-professores/', views.listar_professores, name='listar_professores'),  # Exemplo de listagem.
    path('professor/novo/', views.criar_professor, name='professor-create'),

    path('professores/cadastrar/', views.criar_professor, name='cadastrar_professor'),
    path('professores/', views.listar_professores, name='listar_professores'),
    path('professores/<int:id>/editar/', views.editar_professor, name='editar_professor'),


    path('cadastrar_professor/', views.cadastrar_professor, name='cadastrar_professor'),
    path('sucesso/', views.sucesso, name='sucesso'),  # Página de sucesso

    # path('listar_professores/', views.listar_professores, name='listar_professores'),
    # path('editar_professor/<int:professor_id>/', views.editar_professor, name='editar_professor'),
    path('excluir_professor/<int:professor_id>/', views.excluir_professor, name='excluir_professor'),
    path('relatorios_professores/', views.relatorios_professores, name='relatorios_professores'),

    path('diretores/', views.listar_diretores, name='listar_diretores'),
    path('diretores/cadastrar/', views.cadastrar_diretor, name='cadastrar_diretor'),
    path('diretor/<int:id>/', views.visualizar_diretor, name='visualizar_diretor'),
    path('diretor/editar/<int:id>/', views.editar_diretor, name='editar_diretor'),
    path('diretor/excluir/<int:id>/', views.excluir_diretor, name='excluir_diretor'),

    path('imprimir_curriculo/<int:diretor_id>/', views.imprimir_curriculo, name='imprimir_curriculo'),
    path('gerar_qrcode/<int:diretor_id>/', views.gerar_qrcode, name='gerar_qrcode'),


    path("registrar/", views.registrar_candidato, name="registrar_candidato"),
    # path("login/", views.login_candidato, name="login_candidato"),
    path("logout/", LogoutView.as_view(next_page="login_candidato"), name="logout"),
    path("area_administrativa/", views.area_administrativa, name="area_administrativa"),
    path("imprimir_curriculo/<int:user_id>/", views.imprimir_curriculo, name="imprimir_curriculo"),

    path('diretores/exportar_excel/', views.exportar_excel, name='exportar_excel'),
    path('diretores/exportar_pdf/', views.exportar_pdf, name='exportar_pdf'),
    path('diretores/exportar_csv/', views.exportar_csv, name='exportar_csv'),
    path('diretores/exportar_xls/', views.exportar_xls, name='exportar_xls'),

    path('transparencia/', views.transparencia_index, name='transparencia_index'),
    path('transparencia/folha-pagamento/', views.transparencia_folha_pagamento, name='transparencia_folha_pagamento'),
    path('transparencia/alimentacao/', views.transparencia_alimentacao, name='transparencia_alimentacao'),
    path('transparencia/bens-consumo/', views.transparencia_bens_consumo, name='transparencia_bens_consumo'),
    path('transparencia/outros-gastos/', views.outros_gastos, name='outros_gastos'),
    path('politica-de-privacidade/', views.privacy_policy, name='privacy_policy'),
    path('contato/', views.contact_us, name='contact_us'),
    path('ajuda/', views.help, name='help'),
    path('pesquisar/', views.pesquisar_curriculos, name='pesquisar_curriculos'),

    path('diretor/<int:diretor_id>/formacao/', views.cadastrar_formacao, name='cadastrar_formacao'),

    path('site-curriculos/', views.site_curriculos, name='site_curriculos'),

    path('registrar-curriculo/', views.registrar_novo_curriculo, name='registrar_novo_curriculo'),

    path('cadastrar-candidato/', views.cadastrar_candidato, name='cadastrar_candidato'),

    path("registrar-candidato/", views.cadastrar_candidato, name="cadastrar_candidato"),

    path("adicionar-curriculo/", views.adicionar_curriculo, name="adicionar_curriculo"),

     path("area-candidato/", views.area_candidato, name="area_candidato"),

     path('login-curriculo/', views.login_candidato, name='login_curriculo'),

    path('login-candidato/', views.login_candidato, name='login_candidato'),

    path('cadastrar-curriculo/', views.cadastrar_curriculo, name='cadastrar_curriculo'),

    path("logout/", views.logout_candidato, name="logout_candidato"),

    path('minhas-inscricoes/', views.minhas_inscricoes, name='minhas_inscricoes'),

    path('editar-perfil/', views.editar_perfil, name='editar_perfil'),

    path('verificar-cpf/', views.verificar_cpf, name='verificar_cpf'),
   
    path('imprimir-curriculo-cpf/<str:cpf>/', views.imprimir_curriculo_por_cpf, name='imprimir_curriculo_cpf'),

   #path('banco-curriculos/editar-perfil/', views.editar_perfil, name='editar_perfil'),

    path("banco-curriculos/logout/", views.logout_candidato, name="logout_candidato"),

    path('banco-curriculos/login/', login_candidato, name='login_candidato'),

    #path('visualizar-curriculo/<int:candidato_id>/', visualizar_curriculo, name='visualizar_curriculo'),

    path("visualizar-curriculo/", visualizar_curriculo, name="visualizar_curriculo"),

    path("banco-curriculos/login-candidato/", login_candidato, name="login_candidato"),

     #path("banco-curriculos/area-candidato/", area_candidato, name="area_candidato"),

     path("banco-curriculos/visualizar-curriculo/", visualizar_curriculo, name="visualizar_curriculo"),

     path('editar-curriculo/<int:candidato_id>/', editar_curriculo, name='editar_curriculo'),

     path("editar-perfil/", editar_perfil, name="editar_perfil"),

     path("recuperar-senha/", recuperar_senha, name="recuperar_senha"),

     path("resetar-senha/<uidb64>/<token>/", resetar_senha, name="resetar_senha"),

     path("enviar-link-recuperacao/", enviar_link_recuperacao, name="enviar_link_recuperacao"),

     path('banco-curriculos/enviar-link-recuperacao/', enviar_link_recuperacao, name='enviar_link_recuperacao'),

     path("resetar-senha/<int:candidato_id>/", resetar_senha, name="resetar_senha"),

    path("recuperar-senha/", enviar_link_recuperacao, name="enviar_link_recuperacao"),

    path("recuperar-senha/", enviar_email_recuperacao, name="recuperar_senha"),

    path('listar-diretores-antigos/', views.listar_diretores_antigos, name='listar_diretores_antigos'),
    
    path('listar-curriculos-antigos/', views.listar_curriculos_antigos, name='listar_curriculos_antigos'),
    path('visualizar-curriculo-antigo/<int:id>/', views.visualizar_curriculo_antigo, name='visualizar_curriculo_antigo'),
    path('editar-curriculo-antigo/<int:id>/', views.editar_curriculo_antigo, name='editar_curriculo_antigo'),
    path('excluir-curriculo-antigo/<int:id>/', views.excluir_curriculo_antigo, name='excluir_curriculo_antigo'),
    path('imprimir-curriculo-antigo/<str:cpf>/', views.imprimir_curriculo_antigo, name='imprimir_curriculo_antigo'),

    path('exportar-xls/', views.exportar_xls, name='exportar_xls'),
    path('exportar-pdf/', views.exportar_pdf, name='exportar_pdf'),

    path('educacao_infantil/', educacao_infantil, name='educacao_infantil'),

    path('educacao-infantil/', views.educacao_infantil, name='educacao_infantil'),
    path('educacao-infantil/cadastro-escola/', views.cadastro_escola, name='cadastro_escola'),
    path('educacao-infantil/cadastro-turma/', views.cadastro_turma, name='cadastro_turma'),
    path('educacao-infantil/cadastro-alunos/', views.cadastro_alunos, name='cadastro_alunos'),
    path('educacao-infantil/corrigir-avaliacoes/', views.corrigir_avaliacoes, name='corrigir_avaliacoes'),
    path("educacao-infantil/upload/", upload_cadastro_ei, name="upload_cadastro_ei"),

    path("cadastro-escola/", cadastro_escola, name="cadastro_escola"),
    path("cadastro-escola/excluir/<int:id_matricula>/", excluir_escola, name="excluir_escola"),  # Nova URL

    path("editar-escola/<str:id_matricula>/", editar_escola, name="editar_escola"),

    path("lancamento-notas/", views.selecionar_turma, name="selecionar_turma"),
    path("buscar_turmas/", views.buscar_turmas, name="buscar_turmas"),
    path("listar_alunos/", views.listar_alunos, name="listar_alunos"),
    path("salvar_notas/", views.salvar_notas, name="salvar_notas"),

    path("cadastro-turma/", cadastro_turma, name="cadastro_turma"),
    path("buscar_turmas/", get_turmas, name="buscar_turmas"),  # Endpoint para AJAX
    path('editar-turma/<int:id_matricula>/', views.editar_turma, name='editar_turma'),
    path('excluir-turma/<int:id_matricula>/', views.excluir_turma, name='excluir_turma'),  # Verifique esta linha

    path('visualizar-avaliacao/<int:id_matricula>/', visualizar_avaliacao, name='visualizar_avaliacao'),

    path('salvar-avaliacao/<int:id_matricula>/', salvar_avaliacao, name='salvar_avaliacao'),

    path('lancar-conceito/', views.lancar_conceito, name='lancar_conceito'),

    path('corrigir-avaliacoes/', views.corrigir_avaliacoes, name='corrigir_avaliacoes'),

    path('gestao-alunos/', views.gestao_alunos, name='gestao_alunos'),

    path("gestao-relatorios/", gestao_relatorios, name="gestao_relatorios"),

    path('gestao-relatorios/', views.gestao_relatorios, name='gestao_relatorios'),

    path('buscar_turmas/', views.buscar_turmas, name='buscar_turmas'),

    path('gestao-relatorios/', gestao_relatorios, name='gestao_relatorios'),

    path('gerar-pdf-relatorio/', gerar_pdf_relatorio, name='gerar_pdf_relatorio'),

    path('lancamento-conceitos/', lancamento_conceitos, name='lancamento_conceitos'),

    path('buscar_turmas/', buscar_turmas, name='buscar_turmas'),

    path('buscar_turmas/', get_turmas, name='buscar_turmas'),

    path('cadastro_escola/', cadastro_escola, name='cadastro_escola'),

    path('salvar_avaliacao/<int:id_matricula>/', salvar_avaliacao, name='salvar_avaliacao'),

    path('salvar_avaliacao/<int:id_matricula>/', views.salvar_avaliacao, name='salvar_avaliacao'),

    path('soe/principal/', views.soe_principal, name='soe_principal'),
    path('soe/gestao/', views.soe_gestao, name='soe_gestao'),
    path('soe/uploads/', views.soe_uploads, name='soe_uploads'),
    path('soe/relatorios/', views.soe_relatorios, name='soe_relatorios'),
    path('soe/servicos/', views.soe_servicos, name='soe_servicos'),
    path('upload-dados/', views.upload_dados, name='upload_dados'),
    path('dados-synaptic/', views.dados_synaptic, name='dados_synaptic'),
    path('upload-dados/', views.upload_files, name='upload_dados'),  # Altere para o nome correto da função
    path('banco-curriculos/ocorrencias-sige/', views.ocorrencias_sige, name='ocorrencias_sige'),
    path('ocorrencias-sige/', views.ocorrencias_sige, name='ocorrencias_sige'),
    path('ocorrencias-synaptic/', views.ocorrencias_synaptic, name='ocorrencias_synaptic'),
    path('ocorrencias-synaptic/', ocorrencias_synaptic, name='ocorrencias_synaptic'),
    path('ocorrencias-synaptic/pdf/', ocorrencias_synaptic_pdf, name='ocorrencias_synaptic_pdf'),
    path('ocorrencias-sige/pdf/', views.ocorrencias_sige_pdf, name='ocorrencias_sige_pdf'),
    path('ocorrencias-autokee/', ocorrencias_autokee, name='ocorrencias_autokee'),
    path('ocorrencias/orientadores/', ocorrencias_orientadores, name='ocorrencias_orientadores'),
    path('orientadores/ocorrencias/', views.orientadores_ocorrencias, name='orientadores_ocorrencias'),

    path('controle-usuarios/editar/<int:user_id>/', views.editar_usuario, name='editar_usuario'),
    path('controle-usuarios/excluir/<int:user_id>/', views.excluir_usuario, name='excluir_usuario'),
    path('professores/adicionar/', views.adicionar_professor, name='adicionar_professor'),
    path('coordenadores/adicionar/', views.adicionar_coordenador, name='adicionar_coordenador'),

    path('imprimir-curriculo-candidato/<int:candidato_id>/', views.imprimir_curriculo_por_candidato, name='imprimir_curriculo_candidato'),


    path('imprimir-curriculo-diretor/<int:diretor_id>/', views.imprimir_curriculo_por_diretor, name='imprimir_curriculo_diretor'),

    path('curriculos/<int:id>/imprimir/', views.imprimir_curriculo_por_diretor, name='imprimir_curriculo'),

    #path('curriculos/<str:cpf>/imprimir/', views.imprimir_curriculo_por_cpf, name='imprimir_curriculo'),

    path('banco-curriculos/imprimir-curriculo-diretor/<int:diretor_id>/', views.imprimir_curriculo_diretor, name='imprimir_curriculo_diretor'),

    path('login-prof/', views.login_prof, name='login_prof'),

    path('login-prof/', login_prof, name='login_prof'),

    path('logout-prof/', logout_prof, name='logout_prof'),

    path('modulo-pedagogico/', modulo_pedagogico, name='modulo_pedagogico'),

    path('registrar-professor/', views.registrar_professor, name='registrar_professor'),

    path('login-prof/', views.login_prof_view, name='login_prof'),

    path('logout-professor/', views.logout_prof, name='logout_prof'),

    path('api/unidades-turmas/', views.carregar_unidades_turmas, name='carregar_unidades_turmas'),

    path('editar-aluno/<int:id>/', views.editar_aluno, name='editar_aluno'),

    path('avaliar-aluno/<int:id>/', views.avaliar_aluno, name='avaliar_aluno'),

    path('carregar-turmas/', carregar_turmas_por_escola, name='carregar_turmas_por_escola'),

    path('carregar-turmas/', carregar_turmas_por_escola, name='carregar_turmas'),

    path('banco-curriculos/editar-curriculo/<int:diretor_id>/', editar_curriculo, name='editar_curriculo'),
    path('banco-curriculos/editar-curriculo/<int:candidato_id>/', editar_curriculo, name='editar_curriculo'),

    path("imprimir-curriculo-alternativo/<int:candidato_id>/", imprimir_curriculo_alternativo, name="imprimir_curriculo_alternativo"),
    path('banco-curriculos/imprimir-curriculo-alternativo/<int:diretor_id>/', imprimir_curriculo_alternativo, name='imprimir_curriculo_alternativo'),

    path('listar-diretores/', listar_diretores, name='listar_diretores'),


    # SEPECC
    path("get-escola-pdde/<int:pk>/", get_escola_pdde, name="get-escola-pdde"),
    path('banco-curriculos/adicionar-escola-pdde/', EscolaPddeCreateView.as_view(), name='adicionar_escola_pdde'),
    path('banco-curriculos/listar-escolas/', EscolaPddeListView.as_view(), name='lista_escolas_pdde'),  # Certifique-se de que essa rota existe!
    path('banco-curriculos/excluir-escola/<int:pk>/', EscolaPddeDeleteView.as_view(), name='excluir_escola_pdde'),
    path('banco-curriculos/detalhes-escola/<int:pk>/', EscolaPddeDetailView.as_view(), name='detalhes_escola_pdde'),

    path("banco-curriculos/escola-pdde/<int:pk>/", get_escola_pdde, name="get_escola_pdde"),
    path("banco-curriculos/escolas/", EscolaPddeListView.as_view(), name="listar_escolas"),
    path('get-escola-modal/<int:pk>/', get_escola_pdde_modal, name='get_escola_pdde_modal'),
    path("contabilidade/pdde/", EscolaPddeModalView.as_view(), name="escola_modal"),
    path("pddereceita-despesa/", pddereceita_despesa_view, name="pddereceita_despesa"),
    path("get-escola-pdde/<int:pk>/", get_escola_pdde, name="get_escola_pdde"),

    path("get-escola-pdde/<int:escola_id>/", get_escola_pdde, name="get_escola_pdde"),
    path("get-receita-despesa/<int:escola_id>/", get_receita_despesa, name="get_receita_despesa"),
    path("get-pagamentos/", get_pagamentos, name="get_pagamentos"),
    path("get-pagamentos/<int:escola_id>/", get_pagamentos, name="get_pagamentos"),
    path("pdde-list/", pdde_list, name="pdde_list"),

    # path("pdde-receita-despesa/", pddereceita_despesa, name="pddereceita_despesa"),
    path("pdde-lancar-receita/", pddelancar_receita, name="pddelancar_receita"),
    path("pdde-lancar-despesa/", pddelancar_despesa, name="pddelancar_despesa"),
    path("pdde-lancar-pagamento/", pddelancar_pagamento, name="pddelancar_pagamento"),
    path("editar-pagamento/<int:pagamento_id>/", editar_pagamento, name="editar_pagamento"),  # 🔹 Adicionada esta linha
    path("get-dados-financeiros/<int:escola_id>/", get_dados_financeiros, name="get_dados_financeiros"),

    path("pagamento-lancamento/", lancamento_pagamento, name="pagamento_lancamento"),
    path("get-pagamentos-pdde/<int:escola_id>/", get_pagamentos_pdde, name="get_pagamentos_pdde"),
    path("get-dados-pagamentos-pdde/<int:escola_id>/", get_dados_pagamentos_pdde, name="get_dados_pagamentos_pdde"),
    path('lancar-pagamento/', pddelancar_pagamento, name='lancar_pagamento'),
    path("get-escolas/", get_escolas, name="get_escolas"),
    path("get-escolas/", get_escolas, name="get-escolas"),
    path('banco-curriculos/pdde/gerar-pdf/', pdde_gerar_pdf, name='gerar_pdf'),
    path("get-dados-financeiros/<int:escola_id>/", get_dados_financeiros, name="get-dados-financeiros"),
    path('pdde/gerar-pdf/', pdde_gerar_pdf, name='pdde_gerar_pdf'),
    
    
     # 🔹 Conciliação Bancária
    path('conciliacao/extrato/', conciliacao_extrato, name='conciliacao_extrato'),
    path('conciliacao/lancamentos/', conciliacao_lancamento, name='conciliacao_lancamento'),
    path('conciliacao/saldo/', conciliacao_saldo, name='conciliacao_saldo'),
    path('conciliacao/conferencia/', conciliacao_conferencia, name='conciliacao_conferencia'),
    path('conciliacao/relatorios/', conciliacao_relatorios, name='conciliacao_relatorios'),

    # 🔹 Lançamentos Bancários
    path('conciliacao/lancamento/novo/', criar_lancamento, name="criar_lancamento"),
    path('conciliacao/lancamento/editar/<int:pk>/', editar_lancamento, name="editar_lancamento"),
    path('conciliacao/lancamento/excluir/<int:pk>/', excluir_lancamento, name="excluir_lancamento"),

    # 🔹 Lançamentos Bancários (Separados da Conciliação)
    path('lancamentos/', listar_lancamentos, name='listar_lancamentos'),
    path('lancamentos/novo/', criar_lancamento, name='criar_lancamento'),
    path('lancamentos/editar/<int:pk>/', editar_lancamento, name='editar_lancamento'),
    path('lancamentos/excluir/<int:pk>/', excluir_lancamento, name='excluir_lancamento'),


    path("listar-pdde/", listar_pdde, name="listar_pdde"),

    path("contas/nova/", criar_conta_bancaria, name="nova_conta"),
    path("contas/nova/", criar_conta_bancaria, name="nova_conta"),
    path("contas/listar/", listar_contas, name="listar_contas"),  # ✅ Adicionando a rota correta
    path("contas/editar/<int:conta_id>/", views.editar_conta, name="editar_conta"),
    path("contas/listar/", views.listar_contas, name="listar_contas"),
    path("contas/nova/", views.criar_conta_bancaria, name="nova_conta"),
    path("contas/excluir/<int:conta_id>/", excluir_conta, name="excluir_conta"),

    path("get-contas/<int:escola_id>/", get_contas_por_escola, name="get_contas_por_escola"),

    path("consulta-saldo/", consultar_saldo, name="consulta_saldo"),
    path("api/escolas/", api_escolas, name="api_escolas"),  # 🔹 API para carregar escolas
    path("api/contas/<int:escola_id>/", api_contas, name="api_contas"),  # 🔹 API para carregar contas da escola
    path("api/saldos/", api_saldos, name="api_saldos"),  # 🔹 API para buscar os saldos filtrados
    path("api/conferencia/", api_conferencia, name="api_conferencia"),

    path("api/extrato/", api_extrato, name="api_extrato"),  # 🔹 Rota para buscar extrato bancário

    path("programas/", listar_programas, name="listar_programas"),
    path("programas/novo/", criar_programa, name="criar_programa"),

    path("cadastrar-programa/", cadastrar_programa, name="cadastrar_programa"),

    path("listar-programas/", listar_programas, name="listar_programas"),

    path("listar-escolas/", listar_escolas, name="listar_escolas"),

    path("pdde-lancar-receita/", pddelancar_receita, name="lancar_receita"),  # ✅ URL correta 

    path('banco-curriculos/editar-escola/<int:escola_id>/', editar_escola_pdde, name='editar_escola'),

    path("get-receita-despesa/<int:escola_id>/", pddereceita_despesa, name="pddereceita_despesa"),

    path('editar-escola/<int:pk>/', editar_escola_pdde, name='editar_escola_pdde'),

    path('get-programas-vinculados/<int:escola_id>/', get_programas_vinculados, name='get_programas_vinculados'),

    path('banco-curriculos/pddereceita-despesa/<int:escola_id>/', pddereceita_despesa, name='pddereceita_despesa'),

    path("vincular-escola-programa/", vincular_escola_programa, name="vincular_escola_programa"),

    # path("get-programas-escola/<int:escola_id>/", listar_programas_por_escola, name="listar_programas_por_escola"),

    path("pdde/get-receita-despesa/<int:escola_id>/", views.get_dados_receita_despesa_pdde, name="get_dados_receita_despesa_pdde"),

    path("pdde/get-receita-despesa/<int:escola_id>/", get_dados_receita_despesa_pdde, name="get_dados_receita_despesa_pdde"),

    path("pdde/get-receita/<int:escola_id>/", get_dados_receita, name="get_dados_receita"),

    # path("get-programas-escola/<int:escola_id>/", get_programas_escola, name="get-programas-escola"),

    path("get-programas-escola/<int:escola_id>/", get_programas_por_escola, name="get_programas_por_escola"),

    path("get-receita/<int:escola_id>/<str:programa>/", get_receita, name="get_receita"),

    path('contas/editar/<int:conta_id>/', editar_conta, name='editar_conta'),

    path('conciliacao/emitir/', emitir_conciliacao, name='conciliacao_emitir'),

    path('conciliacao/gerar-pdf/', gerar_conciliacao_pdf, name='gerar_conciliacao_pdf'),


    path("", views.pesquisa_precos, name="pesquisa_precos"),
    path("cadastrar-item/", views.cadastrar_item, name="cadastrar_item"),
    path("cadastrar-proponente/", views.cadastrar_proponente, name="cadastrar_proponente"),
    path("listar-proponentes/", views.listar_proponentes, name="listar_proponentes"),  # Adicione esta linha
    path("cadastrar-proposta/", views.cadastrar_propostas, name="cadastrar_propostas"),  # Verifique o nome aqui
    path("cadastrar-proposta/", views.cadastrar_propostas, name="cadastrar_proposta"),  # Certifique-se de que o nome é correto
    path("apuracao-resultado/", views.apuracao_resultado, name="apuracao_resultado"),
    path("get-subcategorias/<int:categoria_id>/", views.get_subcategorias, name="get_subcategorias"),
    path("listar-itens/", views.listar_itens, name="listar_item"),
    path("gerar-pdf-orcamento/", views.gerar_pdf_orcamento, name="gerar_pdf_orcamento"),  # Adicione esta linha
    path("gerar-excel-orcamento/", views.gerar_excel_orcamento, name="gerar_excel_orcamento"),  # Adicione esta linha
    path("cadastrar-subcategoria/", views.cadastrar_subcategoria, name="cadastrar_subcategoria"),
    path("cadastrar-categoria/", views.cadastrar_categoria, name="cadastrar_categoria"),  # ✅ Nova URL para cadastrar categoria
    path("apuracao/", apuracao_resultados, name="apuracao_resultados"),
    path("apuracao-resultados/", apuracao_resultados, name="apuracao_resultados"),  # 🔹 Confirme que esta URL está correta
    path("api/detalhes_proponente/<int:proponente_id>/", detalhes_proponente, name="detalhes_proponente"),


    path("documentos/", listar_documentos, name="listar_documentos"),
    path("documentos/cadastrar/", cadastrar_documento, name="cadastrar_documento"),
    path("bens/cadastrar/", cadastrar_bem, name="cadastrar_bem"),
    path("bens/listar/", views.listar_bens, name="listar_bem"),
    path("bens/", listar_bens, name="listar_bens"),
    path('representantes/', views.listar_representantes, name='listar_representantes'),
    path('representantes/cadastrar/', views.cadastrar_representante, name='cadastrar_representante'),
    path("representantes/cadastrar/", cadastrar_representante, name="cadastrar_representante"),
    path("relatorio/prestacao_contas/", gerar_prestacao_contas_pdf, name="gerar_prestacao_contas_pdf"),

    path('get-escola-dados/<int:escola_id>/', get_escola_dados, name="get_escola_dados"),

    path("documentos/listar/", views.listar_documento, name="listar_documento"),
    path('documentos/cadastrar/', cadastrar_documento, name="cadastrar_documento"),

    path('termo-doacao/cadastrar/', views.cadastrar_termo_doacao, name='cadastrar_termo_doacao'),
    path('termo-doacao/<int:termo_id>/', views.visualizar_termo_doacao, name='visualizar_termo_doacao'),

    path("bens-doacao/cadastrar/", views.cadastrar_bem_doado, name="cadastrar_bem_doado"),
    path("bens-doacao/listar/", views.listar_bens_doados, name="listar_bens_doados"),
    path("bens-doacao/termo/", views.gerar_pdf_termo_doacao, name="gerar_termo_doacao"),

    path('termo-doacao/pdf/', views.gerar_pdf_termo_doacao, name='gerar_pdf_termo_doacao'),

    path('get-escola-dados/<int:escola_id>/', views.get_escola_dados, name='get_escola_dados'),
    path("termo-doacao/cadastrar/", views.cadastrar_termo_doacao, name="cadastrar_termo_doacao"),
    path('get-escola-dados/<int:escola_id>/', views.get_dados_escola, name='get_dados_escola'),
    # urls.py
    path("termo-doacao/pdf/<int:termo_id>/", views.gerar_pdf_termo_doacao, name="gerar_pdf_termo_doacao"),

    path('bem-doado/pdf/<int:bem_id>/', views.gerar_pdf_bem, name='gerar_pdf_bem'),

    path("representantes/", views.listar_representantes, name="listar_representante"),  # <- nome deve casar com o template


    path('enviar-plano/', enviar_plano_gestao, name='enviar_plano'),

    path('planos-de-gestao/', listar_pge_planos, name='listar_pge_planos'),

    path('get-dados-unidade/<str:unidade_nome>/', views.obter_dados_unidade, name='get_dados_unidade'),

    path('admin/pge/', plano_gestao_escolar_admin, name='plano_gestao_escolar'),

    # Página de administração dos planos (com tabela e filtros)
    path('planos-gestao/', views.plano_gestao_escolar_admin, name='plano_gestao_escolar'),

    # Página alternativa ou simplificada, se desejar manter
    path('planos-gestao/listar/', views.listar_pge_planos, name='listar_planos'),

    # Atualização de status (usado pelo fetch ou modal)
    path('planos-gestao/<int:plano_id>/atualizar/', views.atualizar_status_plano, name='atualizar_status_plano'),
    path('planos-gestao/novo/', views.enviar_plano_gestao, name='enviar_plano'),  # Este é o correto

    path('planos-gestao/', views.listar_pge_planos, name='listar_planos'),

    path('planos-gestao/enviar/', views.enviar_plano_gestao, name='enviar_plano'),


    path('certidoes/', views.emissao_certidoes, name='emissao_certidoes'),
    path('upload-certidao/', views.upload_arquivo_certidao, name='upload_arquivo_certidao'),

    path('pdde/gerar-cotacao/', views.gerar_cotacao, name='gerar_cotacao'),

    path('gerar-cotacao/', gerar_cotacao, name='gerar_cotacao'),



    
    path('livro-diario/', views.livro_diario, name='livro_diario'),
    path('livro-diario/adicionar/', views.adicionar_lancamento_diario, name='adicionar_lancamento_diario'),
    path('livro-diario/excluir/<int:id>/', views.excluir_lancamento_diario, name='excluir_lancamento_diario'),
    path('livro-diario/export/pdf/', views.exportar_livro_diario_pdf, name='exportar_livro_diario_pdf'),
    path('livro-diario/export/csv/', views.exportar_livro_diario_csv, name='exportar_livro_diario_csv'),
    path('livro-diario/export/excel/', views.exportar_livro_diario_excel, name='exportar_livro_diario_excel'),

    
    path('livro-caixa/info-completa/<int:escola_id>/', views.get_info_completa_escola, name='info_completa_escola'),

    path('livro-caixa/info-basica/<int:escola_id>/', views.get_info_receita_despesa, name='info_basica'),
    path('livro-caixa/info-detalhada/<int:escola_id>/', views.get_receita_info, name='info_detalhada'),



    path('contas/consolidado/', views.get_consolidado_contas, name='consolidado_contas'),

    path('contas/consolidado-receita/', views.get_consolidado_receita, name='consolidado_receita'),

    path('contas/sintese-receita/', views.get_sintese_receita, name='sintese_receita'),

    path('pdde/sintese/', views.sintese_pdde_view, name='sintese_pdde'),

    path('pdde/cadastrar-info/', views.cadastrar_info_pdde, name='cadastrar_info_pdde'),


    path('contas/sintese-pdf/', views.gerar_pdf_sintese, name='sintese_pdf'),


    path('manuais/', views.lista_manuais, name='manuais'),
    path('manuais/download/<str:arquivo>/', views.download_manual, name='download_manual'),

    path('planos-gestao/<int:plano_id>/indeferimento/pdf/', views.gerar_pdf_indeferimento, name='gerar_pdf_indeferimento'),

    path('planos-gestao/salvar-motivo/', views.salvar_motivo_indeferimento, name='salvar_motivo_indeferimento'),

    path('planos-gestao/enviar-email/', views.enviar_email_indeferimento, name='enviar_email_indeferimento'),


    path('relatorio/gerar-mapeamento/', views.gerar_pdf_mapeamento, name='gerar_pdf_mapeamento'),
    path('relatorio/gerar-detalhado/', views.gerar_pdf_detalhado, name='gerar_pdf_detalhado'),

    path('relatorio/saida-rede/', relatorio_saida_rede, name='relatorio_saida_rede'),

    path('relatorio/saida-rede/', views.relatorio_saida_rede, name='relatorio_saida_rede'),

    path('relatorio/gerar-saida-rede/', gerar_pdf_saida_rede, name='gerar_pdf_saida_rede'),

    path('relatorio/exportar-pptx/', exportar_pptx_saida_rede, name='exportar_pptx_saida_rede'),

    path('relatorio/geral/', gerar_pdf_relatorio_geral, name='gerar_pdf_relatorio_geral'),

    path('gerar-pdf-habilidades-especificas/', views.gerar_pdf_habilidades_especificas, name='gerar_pdf_habilidades_especificas'),

    path('gerar-graficos-pdf/', views.gerar_graficos_pdf, name='gerar_graficos_pdf'),

    path('gerar-graficos-q11-q13/', views.gerar_graficos_q11_q13, name='gerar_graficos_q11_q13'),

    path('relatorio/matematica-saida/', relatorio_saida_matematica_view, name='relatorio_saida_matematica'),

    path('relatorio/saida-matematica/', relatorio_saida_matematica_view, name='relatorio_saida_matematica'),

    path("relatorio/matematica-saida/", relatorio_saida_matematica_view, name="relatorio_saida_matematica"),


    

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)