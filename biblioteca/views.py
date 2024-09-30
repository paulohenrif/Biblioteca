from django.shortcuts import render, redirect
from biblioteca.models import Livro, Emprestimo, Pessoa
from pyexpat.errors import messages

def Home(request):
    return render(request, 'home.html')

def cadastrar_usuario(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        if nome:
            Pessoa.objects.create(nome=nome, email=email)
        return redirect('lista_pessoas')
    
    return render(request, 'cadastrar_usuario.html')

def cadastrar_livro(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        autor = request.POST.get('autor')
        exemplares = request.POST.get('exemplares')
        Livro.objects.create(titulo=titulo, autor=autor, exemplares=exemplares, status='disponível')
        return redirect('lista_livros')
    return render(request, 'cadastrar_livro.html')

def lista_livros(request):
    livros = Livro.objects.all()
    return render(request, 'lista_livros.html', {'livros': livros})

def solicitar_emprestimo(request):
    if request.method == 'POST':
        livro_id = request.POST.get('livro_id')
        pessoa_id = request.POST.get('pessoa_id')
        livro = Livro.objects.get(id=livro_id)
        pessoa = Pessoa.objects.get(id=pessoa_id)

        if livro.exemplares > 0:
            Emprestimo.objects.create(livro=livro, usuario=pessoa)
            livro.exemplares -= 1
            livro.save()
            messages.success(request, 'Empréstimo realizado com sucesso!')
        else:
            messages.error(request, 'Não há exemplares disponíveis para empréstimo.')

        return redirect('lista_livros')

    livros = Livro.objects.all()
    pessoas = Pessoa.objects.all()

    return render(request, 'solicitar_emprestimo.html', {'livros': livros, 'usuarios': pessoas})

def devolucao(request, livro_id):
    livro = Livro.objects.get(id=livro_id)
    return render(request, 'devolucao.html', {'livro': livro})

def lista_pessoas(request):
    pessoas = Pessoa.objects.all()
    return render(request, 'lista_pessoas.html', {'pessoas': pessoas})