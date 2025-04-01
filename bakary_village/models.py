from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
from .auth.hasher import hasher


class Produto(models.Model):
    nome = models.CharField(max_length=500)
    preco = models.DecimalField(max_digits=15, decimal_places=2)

    CATEGORIA_CHOICES = [
        ("Bebidas", "Bebidas"),
        ("Doces", "Doces"),
        ("Salgados", "Salgados"),
        ("Padaria", "Padaria"),
        ("Mercearia", "Mercearia"),
    ]
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)
    estoque = models.IntegerField()

    class Meta:
        db_table = "produtos"

    def __str__(self):
        return f"Produto(id={self.id}, nome='{self.nome}', preco={self.preco}, categoria='{self.categoria}', estoque={self.estoque})"


class Cliente(models.Model):
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=255, unique=True, null=True, blank=True)
    senha = models.CharField(max_length=255)
    telefone = models.CharField(max_length=15, null=True, blank=True)
    email = models.CharField(max_length=255, unique=True, null=True, blank=True)
    token = models.CharField(max_length=255, null=True, blank=True)
    activate = models.BooleanField(default=True)

    class Meta:
        db_table = "clientes"

    def __str__(self):
        return f"Cliente(id={self.id}, nome='{self.nome}', cpf='{self.cpf}', telefone='{self.telefone}', email='{self.email}')"

    def __init__(self, *args, **kwargs):
        if "senha" in kwargs and kwargs["senha"]:
            kwargs["senha"] = hasher.hash_password(kwargs["senha"])
        super().__init__(*args, **kwargs)


class User(models.Model):
    nome = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    senha = models.CharField(max_length=255)

    class Meta:
        db_table = "users"

    def __init__(self, *args, **kwargs):
        if "senha" in kwargs and kwargs["senha"]:
            kwargs["senha"] = hasher.hash_password(kwargs["senha"])
        super().__init__(*args, **kwargs)

    def __str__(self):
        return f"User(id={self.id}, nome='{self.nome}', email='{self.email}')"


class ClienteProduto(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    preco = models.DecimalField(max_digits=15, decimal_places=2)
    quantidade = models.IntegerField()
    total = models.DecimalField(max_digits=15, decimal_places=2)
    data = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "cliente_produto"


class Divida(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    pago = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    activate = models.BooleanField(default=True)
    data_modificacao = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "dividas"

    def __str__(self):
        return f"Divida(id={self.id}, cliente_id={self.cliente.id}, valor={self.valor}, pago={self.pago})"


class Carrinho(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.DecimalField(max_digits=15, decimal_places=2)
    data = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "carrinho"

    def __str__(self):
        return f"Carrinho(id={self.id}, cliente_id={self.cliente.id}, produto_id={self.produto.id}, quantidade={self.quantidade})"
