from django.shortcuts import render, redirect
from biblioteca.models import Livro, Emprestimo

def adicionar_livro(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        autor = request.POST.get('autor')
        exemplares = request.POST.get('exemplares')
        Livro.objects.create(titulo=titulo, autor=autor, exemplares=exemplares, status='disponível')
        return redirect('lista_livros')
    return render(request, 'adicionar_livro.html')

def registrar_emprestimo(request, livro_id):
    livro = Livro.objects.get(id=livro_id)
    if livro.status == 'disponível':
        livro.status = 'emprestado'
        Emprestimo.objects.create(livro=livro)      
        livro.save()
    return redirect('lista_livros')

def lista_livros(request):
    livros = Livro.objects.all()
    return render(request, 'lista_livros.html', {'livros': livros})
