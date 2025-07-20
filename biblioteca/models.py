from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User

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
        self.status = "disponível" if self.exemplares > 0 else "emprestado"
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
            self.matricula = (ultimo_id.matricula + 1) if ultimo_id else 1
        super(Usuario, self).save(*args, **kwargs)


class Emprestimo(models.Model):
    data_emprestimo = models.DateTimeField(auto_now_add=True)
    prazo_final = models.DateTimeField(default=timezone.now() + timedelta(days=30))  # prazo padrão
    estendido = models.BooleanField(default=False)  # indica se o prazo já foi estendido

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Se não tiver prazo_final definido, define 1 mês a partir da data de empréstimo
        if not self.prazo_final:
            self.prazo_final = timezone.now() + timedelta(days=30)
        super().save(*args, **kwargs)

    def tempo_restante(self):
        """Retorna o tempo restante em dias para o usuário ver."""
        delta = self.prazo_final - timezone.now()
        return delta.days if delta.days > 0 else 0

    def pode_estender(self):
        """Permite estender o empréstimo apenas uma vez."""
        return not self.estendido

    def estender_prazo(self):
        """Estende o prazo por mais 30 dias, se possível."""
        if self.pode_estender():
            self.prazo_final += timedelta(days=30)
            self.estendido = True
            self.save()

    def __str__(self):
        return f"{self.usuario.nome} - {self.livro.titulo} (Devolve até {self.prazo_final.date()})"