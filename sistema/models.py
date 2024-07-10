from django.db import models
from django.urls import reverse
from produtos.models import Produto
from django.db.models import Sum
from decimal import Decimal
from datetime import date


class Municipio(models.Model):
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome


class Ata(models.Model):
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, related_name='atas')
    numero_ata = models.CharField(max_length=200, null= True)
    data = models.DateField()
    valor_total_ata = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    valor_total_pedidos = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    valor_restante = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    link_drive = models.CharField(max_length=200)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        itens = Item.objects.filter(ata=self)
        pedidos = Pedido.objects.filter(ata=self)
        valor_total_ata_agg = itens.aggregate(total=Sum('valor_total'))['total']
        valor_total_pedidos_agg = pedidos.aggregate(total_2=Sum('valor_total_pedido'))['total_2']
        self.valor_total_ata = Decimal(valor_total_ata_agg) if valor_total_ata_agg is not None else Decimal('0.00')
        self.valor_total_pedidos = Decimal(valor_total_pedidos_agg) if valor_total_pedidos_agg is not None else Decimal('0.00')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.municipio} - {self.numero_ata}"


class Item(models.Model):
    ata = models.ForeignKey(Ata, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    unidade_opcoes = (
        ('un', 'un'),
        ('kg', 'kg'),
        ('gramas', 'gramas'),
    )
    unidade = models.CharField(max_length=20, choices=unidade_opcoes, null=True)
    valor_unitario = models.DecimalField(max_digits=20, decimal_places=3)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    quantidade_restante = models.IntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.valor_total = self.quantidade * self.valor_unitario
        if self.quantidade_restante is None:
            self.quantidade_restante = self.quantidade
        super().save(*args, **kwargs)
        self.ata.save()

    def __str__(self):
        return f"{self.produto} - {self.unidade}"


class Pedido(models.Model):
    ata = models.ForeignKey(Ata, on_delete=models.CASCADE)
    nota_fiscal = models.IntegerField()
    produto =  models.ForeignKey(Item, on_delete=models.CASCADE)
    quantidade_pedida = models.IntegerField()
    valor_total_pedido = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status_choices = {
        ('n', 'Não iniciado'),
        ('e', 'Em entrega'),
        ('f', 'Finalizado'),
    }
    prazo = models.DateField()
    status = models.CharField(max_length=1, choices=status_choices, blank=True, null=True)

    def save(self, *args, **kwargs):
        item = Item.objects.get(ata=self.ata, produto=self.produto)
        self.valor_total_pedido = self.quantidade_pedida * item.valor_unitario
        if self.pk is None:
            item.quantidade_restante = (item.quantidade_restante or item.quantidade) - self.quantidade_pedida
        else:
            old_pedido = Pedido.objects.get(pk=self.pk)
            item.quantidade_restante += old_pedido.quantidade_pedida - self.quantidade_pedida
        super().save(*args, **kwargs)
        item.save()

    def prazo_vencido(self):
        return self.prazo > date.today()

    prazo_vencido.boolean = True
    prazo_vencido.short_description = 'Prazo'

    def __str__(self):
        return f"Pedido {self.id} - {self.ata.municipio}"


class Resumo(models.Model):
    ata = models.ForeignKey(Ata, on_delete=models.CASCADE)
    resumo = models.TextField()

    def generate_resumo(self):
        itens = Item.objects.filter(ata=self.ata)
        resumo_text = ""
        for item in itens:
            resumo_text += f"Produto: {item.produto} \nQuantidade: {item.quantidade} \nValor Total: {item.valor_total} \nQuantidade Restante: {item.quantidade_restante}\n------------\n"
        self.resumo = resumo_text

    def save(self, *args, **kwargs):
        self.generate_resumo()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Resumo - {self.ata.municipio}"


class Geral(models.Model):
    valor_total_atas_ganhas = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    valor_total_pedidos = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    valor_total_restante = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        atas = Ata.objects.all()
        self.valor_total_atas_ganhas = atas.aggregate(total=Sum('valor_total_ata'))['total'] or 0.00
        self.valor_total_pedidos = atas.aggregate(total2=Sum('valor_total_pedidos'))['total2'] or 0.00
        self.valor_total_restante = self.valor_total_atas_ganhas - self.valor_total_pedidos
        super().save(*args, **kwargs)

    def __str__(self):
        return "Total ganho/pedido/restante"

    class Meta:
        verbose_name_plural = 'Geral'
