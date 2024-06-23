from django.db import models

# Create your models here.
class Produto(models.Model):
    produto = models.CharField(max_length=20)
    descricao = models.CharField(max_length= 200)
   

    def __str__(self):
        return f"{self.produto} "