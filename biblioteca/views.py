from django.shortcuts import render

def adicionar_livro(request):
    return render(request, 'adicionar_livro.html')