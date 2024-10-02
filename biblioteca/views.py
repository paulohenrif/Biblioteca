from django.shortcuts import render, redirect
from biblioteca.models import Livro, Usuario, Emprestimo
from django.http import HttpResponse

def Home(request):
    return render(request, 'home.html')

def cadastrar_usuario(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        if nome:
            Usuario.objects.create(nome=nome, email=email)
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
    usuarios = Usuario.objects.all()
    return render(request, 'paginas_consultas/consultar_usuarios.html', {'usuarios': usuarios})
    
def consultar_acervo(request):
    livros = Livro.objects.all()
    return render(request, 'paginas_consultas/consultar_acervo.html', {'livros': livros})

def solicitar_emprestimo(request):
    if request.method == 'POST':
        livro_id = request.POST.get('livro_id')
        usuario_id = request.POST.get('usuario_id')
        livro = Livro.objects.get(id=livro_id)
        usuario = Usuario.objects.get(id=usuario_id)

        if livro.exemplares > 0:
            Emprestimo.objects.create(livro=livro, usuario=usuario)
            livro.exemplares -= 1
            livro.save()

            return HttpResponse("""
                                    <script>
                                        alert('Empréstimo realizado com sucesso!');
                                    </script>
                                    """)
        else:
            return HttpResponse("""
                                    <script>
                                        alert('Não há exemplares disponíveis para empréstimo.');
                                    </script>
                                    """)

    livros = Livro.objects.all()
    usuarios = Usuario.objects.all()

    return render(request, 'paginas_solicitacoes/solicitar_emprestimo.html', {'livros': livros, 'usuarios': usuarios})

def solicitar_devolucao(request):
    if request.method == 'POST':
        livro_id = request.POST.get('livro_id')
        usuario_id = request.POST.get('usuario_id')
        livro = Livro.objects.get(id=livro_id)
        usuario = Usuario.objects.get(id=usuario_id)

        emprestimo = Emprestimo.objects.filter(livro=livro, usuario=usuario).first()

        if emprestimo:
            emprestimo.delete()
            livro.exemplares += 1
            livro.save()

            return redirect('consultar_acervo')
        else:
            return redirect('consultar_acervo')

    livros = Livro.objects.all()
    usuarios = Usuario.objects.all()

    return render(request, 'paginas_solicitacoes/solicitar_devolucao.html', {'livros': livros, 'usuarios': usuarios})
