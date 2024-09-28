from django.contrib import admin
from django.urls import path, include
from biblioteca.views import adicionar_livro, lista_livros, registrar_emprestimo

urlpatterns = [
    path('admin/', admin.site.urls),
    path('adicionar_livro/', adicionar_livro, name='adicionar_livro'),
    path('', lista_livros, name='lista_livros'),
    path('emprestimo/<int:livro_id>/', registrar_emprestimo, name='registrar_emprestimo'),
]