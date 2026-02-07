from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Cliente(models.Model):
    TIPO_CHOICES = [
        ('PF', 'Pessoa Física'),
        ('PJ', 'Pessoa Jurídica'),
    ]
    nome = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    tipo = models.CharField(max_length=2, choices=TIPO_CHOICES, default='PF')
    status = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome