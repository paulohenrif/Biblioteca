from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from biblioteca.models import Livro, Usuario, Emprestimo
from django.http import HttpResponse

class CustomLoginView(LoginView):
    def get_success_url(self):
        user = self.request.user
        if user.is_staff:
            return "/"
        else:
            return "/"


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('Home')
        else:
            return render(request, 'login.html', {'error': 'Usuário ou senha inválidos'})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def Home(request):
    is_admin = request.user.is_staff
    return render(request, "home.html")

@login_required
def cadastrar_usuario(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        email = request.POST.get("email")
        curso = request.POST.get("curso")
        if nome:
            Usuario.objects.create(nome=nome, curso=curso, email=email)
        return redirect("consultar_usuarios")

    return render(request, "paginas_cadastros/cadastrar_usuario.html")

@login_required
def cadastrar_livro(request):
    if request.method == "POST":
        titulo = request.POST.get("titulo")
        autor = request.POST.get("autor")
        exemplares = int(request.POST.get("exemplares", 0))
        Livro.objects.create(
            titulo=titulo, autor=autor, exemplares=exemplares, status="disponível"
        )
        return redirect("consultar_acervo")
    return render(request, "paginas_cadastros/cadastrar_livro.html")

@login_required
def consultar_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(
        request, "paginas_consultas/consultar_usuarios.html", {"usuarios": usuarios}
    )

@login_required
def consultar_acervo(request):
    livros = Livro.objects.all()
    return render(
        request, "paginas_consultas/consultar_acervo.html", {"livros": livros}
    )
@login_required
def solicitar_emprestimo(request):
    if request.method == "POST":
        livro_id = request.POST.get("livro_id")
        usuario_id = request.POST.get("usuario_id")
        livro = Livro.objects.get(id=livro_id)
        usuario = Usuario.objects.get(id=usuario_id)

        if livro.exemplares > 0:
            Emprestimo.objects.create(
                livro=livro, usuario=usuario
            )
            livro.exemplares -= 1
            livro.save()

            return HttpResponse(
                """
                                    <script>
                                        alert('Empréstimo realizado com sucesso!');
                                    </script>
                                    """
            )
        else:
            return HttpResponse(
                """
                                    <script>
                                        alert('Não há exemplares disponíveis para empréstimo.');
                                    </script>
                                    """
            )

    livros = Livro.objects.all()
    usuarios = Usuario.objects.all()

    return render(
        request,
        "paginas_solicitacoes/solicitar_emprestimo.html",
        {"livros": livros, "usuarios": usuarios},
    )

@login_required
def solicitar_devolucao(request):
    if request.method == "POST":
        livro_id = request.POST.get("livro_id")
        usuario_id = request.POST.get("usuario_id")
        livro = Livro.objects.get(id=livro_id)
        usuario = Usuario.objects.get(id=usuario_id)

        emprestimo = Emprestimo.objects.filter(livro=livro, usuario=usuario).first()

        if emprestimo:
            emprestimo.delete()
            livro.exemplares += 1
            livro.save()

            return redirect("consultar_acervo")
        else:
            return redirect("consultar_acervo")

    livros = Livro.objects.all()
    usuarios = Usuario.objects.all()

    return render(
        request,
        "paginas_solicitacoes/solicitar_devolucao.html",
        {"livros": livros, "usuarios": usuarios},
    )

@login_required
def remover_usuario(request):
    if request.method == "POST":
        usuario_id = request.POST.get("usuario_id")
        nome = Usuario.objects.filter(id=usuario_id)

        if nome:
            nome.delete()

            return redirect("consultar_usuarios")
        else:
            return redirect("remover_usuario")

    usuarios = Usuario.objects.all()

    return render(
        request,
        "remover_usuario.html",
        {"usuarios": usuarios},
    )


@login_required
def emprestimos_view(request):
    if request.user.is_superuser:
        emprestimos = Emprestimo.objects.all()
    else:
        emprestimos = Emprestimo.objects.filter(usuario=request.user)
    return render(request, 'emprestimos.html', {'emprestimos': emprestimos})

@login_required
def estender_prazo(request, emprestimo_id):
    emprestimo = Emprestimo.objects.get(id=emprestimo_id)
    if emprestimo.usuario == request.user and not emprestimo.prazo_estendido:
        emprestimo.estender_prazo()
    return redirect('emprestimos')