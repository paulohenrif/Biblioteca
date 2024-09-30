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
    email = models.EmailField(max_length=254, unique=True)
    matricula = models.IntegerField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.matricula:
            ultimo_id = Pessoa.objects.all().order_by('-matricula').first()
            if ultimo_id:
                self.matricula = ultimo_id.matricula + 1
            else:
                self.matricula = 1
        super(Pessoa, self).save(*args, **kwargs)
    
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
    data_emprestimo = models.DateTimeField()
    data_devolucao = models.DateTimeField(null=True, blank=True)
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)

    def __str__(self):
        return f'Data do empréstimo do livro: {self.cod_livro.titulo}'