from django.db import models

class Livro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=100)
    exemplares = models.IntegerField()
    status = models.CharField(max_length=20, choices=[('disponível', 'Disponível'), ('emprestado', 'Emprestado')])

    def __str__(self):
        return self.titulo
    
class Pessoa(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    matricula = models.CharField(max_length=50)

    def __str__(self):
        return self.nome
    
class Administrador(models.Model):
    funcao = models.CharField(max_length=50)
    salario = models.IntegerField()
    cod_pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE)

    def __str__(self):
        return self.funcao
    
class Usuario(models.Model):
    curso = models.CharField(max_length=50)
    cod_pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE)

    def __str__(self):
        return self.curso

class Emprestimo(models.Model):
    data = models.DateField(auto_now=False, auto_now_add=False)
    hora = models.TimeField(auto_now=False, auto_now_add=False)
    cod_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    cod_livro = models.ForeignKey(Livro, on_delete=models.CASCADE)

    def __str__(self):
        return f'Data do empréstimo do livro: {self.cod_livro.titulo}'