from django.db import models


class Livro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=100)
    exemplares = models.IntegerField()
    status = models.CharField(
        max_length=20,
        choices=[("disponível", "Disponível"), ("emprestado", "Emprestado")],
        default="disponível",
    )

    def save(self, *args, **kwargs):
        if self.exemplares == 0:
            self.status = "emprestado"
        else:
            self.status = "disponível"
        super().save(*args, **kwargs)

    def __str__(self):
        if self.status == "emprestado":
            return f"{self.titulo} ({self.status})"
        else:
            return f"{self.titulo} - {self.exemplares} exemplares ({self.status})"


class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, unique=True)
    curso = models.CharField(max_length=100)
    matricula = models.IntegerField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.matricula:
            ultimo_id = Usuario.objects.all().order_by("-matricula").first()
            if ultimo_id:
                self.matricula = ultimo_id.matricula + 1
            else:
                self.matricula = 1
        super(Usuario, self).save(*args, **kwargs)


class Emprestimo(models.Model):
    data_emprestimo = models.DateTimeField(auto_now_add=True)
    data_devolucao = models.DateTimeField(null=True, blank=True)

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)

    def __str__(self):
        return f"Data do empréstimo do livro: {self.livro.titulo}"
