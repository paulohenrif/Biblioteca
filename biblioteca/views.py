from django.shortcuts import render, redirect
from biblioteca.models import Livro, Emprestimo, Pessoa, Usuario
from pyexpat.errors import messages

def Home(request):
    return render(request, 'home.html')

def cadastrar_usuario(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        if nome:
            Pessoa.objects.create(nome=nome, email=email)
        return redirect('consultar_usuarios')
    
    return render(request, 'paginas_cadastros/cadastrar_usuario.html')

def cadastrar_livro(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        autor = request.POST.get('autor')
        exemplares = request.POST.get('exemplares')
        Livro.objects.create(titulo=titulo, autor=autor, exemplares=exemplares, status='disponível')
        return redirect('consultar_acervo')
    return render(request, 'paginas_cadastros/cadastrar_livro.html')

def consultar_usuarios(request):
    pessoas = Pessoa.objects.all()
    return render(request, 'paginas_consultas/consultar_usuarios.html', {'pessoas': pessoas})
    
def consultar_acervo(request):
    livros = Livro.objects.all()
    return render(request, 'paginas_consultas/consultar_acervo.html', {'livros': livros})

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

        return redirect('consultar_acervo')

    livros = Livro.objects.all()
    pessoas = Pessoa.objects.all()

    return render(request, 'paginas_solicitacoes/solicitar_emprestimo.html', {'livros': livros, 'usuarios': pessoas})

def solicitar_devolucao(request, livro_id):
    livro = Livro.objects.get(id=livro_id)
    return render(request, 'paginas_solicitacoes/solicitar_devolucao.html', {'livro': livro})
