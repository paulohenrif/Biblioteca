from django.contrib import admin
from django.urls import path, include
from biblioteca import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.Home, name="Home"),
    path("cadastrar_livro/", views.cadastrar_livro, name="cadastrar_livro"),
    path("cadastrar_usuario/", views.cadastrar_usuario, name="cadastrar_usuario"),
    path("consultar_acervo/", views.consultar_acervo, name="consultar_acervo"),
    path("consultar_usuarios/", views.consultar_usuarios, name="consultar_usuarios"),
    path(
        "solicitar_emprestimo/", views.solicitar_emprestimo, name="solicitar_emprestimo"
    ),
    path("solicitar_devolucao/", views.solicitar_devolucao, name="solicitar_devolucao"),
]
