from django.contrib import admin
from django.urls import path, include
from biblioteca import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Home, name='Home'), 
    path('cadastrar_livro/', views.cadastrar_livro, name='cadastrar_livro'), 
    path('lista_livros/', views.lista_livros, name='lista_livros'),
    path('lista_pessoas/', views.lista_pessoas, name='lista_pessoas'),
    path('cadastrar_usuario/', views.cadastrar_usuario, name='cadastrar_usuario'),
    path('solicitar_emprestimo/', views.solicitar_emprestimo, name='solicitar_emprestimo'),
    path('devolucao/', views.devolucao, name='devolucao'),
]