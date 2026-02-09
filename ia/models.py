from django.db import models

# Create your models here.
from usuarios.models import Cliente

class Pergunta(models.Model):
    pergunta = models.TextField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def __str__(self):
        return self.pergunta
