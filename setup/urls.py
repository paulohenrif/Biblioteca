from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from biblioteca import views
from biblioteca.views import CustomLoginView

urlpatterns = [
    # Página inicial acessível diretamente
    path('', views.Home, name='Home'),

    # Autenticação
    path('accounts/login/',CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),

    # Funcionalidades protegidas
    path('emprestimos/', views.solicitar_emprestimo, name='solicitar_emprestimo'),
    path('estender/<int:emprestimo_id>/', views.estender_prazo, name='estender_prazo'),
    path('admin/', admin.site.urls),
    path('cadastrar_livro/', views.cadastrar_livro, name='cadastrar_livro'),
    path('cadastrar_usuario/', views.cadastrar_usuario, name='cadastrar_usuario'),
    path('consultar_acervo/', views.consultar_acervo, name='consultar_acervo'),
    path('consultar_usuarios/', views.consultar_usuarios, name='consultar_usuarios'),
    path('remover_usuario/', views.remover_usuario, name='remover_usuario'),
    path('solicitar_devolucao/', views.solicitar_devolucao, name='solicitar_devolucao'),
]