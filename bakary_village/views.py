from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
import csv
import datetime
from decimal import Decimal

from .models import Produto, Cliente, ClienteProduto, Divida, Carrinho, User
from .auth.hasher import hasher

# user_adm = User(nome="root", email="renanrodrigues7110@gmail.com", senha="admin")
# user_adm.save()


# Home
def home(request):
    return render(request, "home/index.html")


# Accounts
def login_view(request:HttpRequest):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        is_admin = request.POST.get("typeuser", False)
        remember = request.POST.get("remember", False)

        try:
            print(username)
            print(password)
            print(is_admin)
            print(remember)
            if is_admin:
                print("administrator")
                cliente = User.objects.get(email=username)
            else:
                cliente = Cliente.objects.get(email=username)
            if hasher.check_password(password, cliente.senha):
                print("Autenticado com sucesso")
                # Aqui você precisaria implementar um sistema de autenticação customizado
                # ou adaptar para usar o sistema de autenticação do Django
                request.session["user_id"] = cliente.id
                request.session["user_name"] = cliente.nome
                request.session["is_staff"] = False if not is_admin else True

                if not remember:
                    request.session.set_expiry(0)

                return redirect("home")
        except Cliente.DoesNotExist as e:
            print("---", e)
            pass

        messages.error(request, "Email ou senha inválidos.")

    return render(request, "accounts/login.html")


def logout_view(request):
    if "user_id" in request.session:
        del request.session["user_id"]
        del request.session["user_name"]
        if "is_staff" in request.session:
            del request.session["is_staff"]

    return redirect("login")


@login_required
def my_account(request):
    user_id = request.session.get("user_id")
    cliente = get_object_or_404(Cliente, id=user_id)

    user_data = {
        "nome": cliente.nome,
        "email": cliente.email,
        "cpf_formatado": cliente.cpf,
        "telefone_formatado": cliente.telefone,
    }

    return render(request, "accounts/my_account.html", {"user_data": user_data})


def forgot_password(request):
    token_sent = False

    if request.method == "POST":
        email = request.POST.get("email")

        try:
            cliente = Cliente.objects.get(email=email)
            # Aqui você implementaria a lógica de geração e envio de token
            # Por enquanto, apenas marcamos como enviado
            token_sent = True
            messages.success(request, "Token enviado com sucesso! Verifique seu email.")
        except Cliente.DoesNotExist:
            messages.error(request, "Email não encontrado em nossa base de dados.")

    return render(request, "accounts/forgot_password.html", {"token_sent": token_sent})


# Products
@login_required
def products_list(request):
    search = request.GET.get("search", "")
    categoria = request.GET.get("categoria", "")

    produtos = Produto.objects.all()

    if search:
        produtos = produtos.filter(nome__icontains=search)

    if categoria:
        produtos = produtos.filter(categoria=categoria)

    return render(request, "catalog/products.html", {"produtos": produtos})


@login_required
def product_create(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        preco = request.POST.get("preco")
        quantidade = request.POST.get("qtde")
        categoria = request.POST.get("categoria")

        Produto.objects.create(
            nome=nome, preco=preco, estoque=quantidade, categoria=categoria
        )

        messages.success(request, "Produto cadastrado com sucesso!")
        return redirect("product_create")

    return render(request, "management/products/create.html")


@login_required
def product_edit(request, id=0):
    if request.method == "POST":
        produto_id = request.POST.get("produto")
        nome = request.POST.get("nome")
        preco = request.POST.get("preco")
        quantidade = request.POST.get("qtde")
        categoria = request.POST.get("categoria")

        produto = get_object_or_404(Produto, id=produto_id)
        produto.nome = nome
        produto.preco = preco
        produto.estoque = quantidade
        produto.categoria = categoria
        produto.save()

        messages.success(request, "Produto alterado com sucesso!")
        return redirect("product_edit", id=0)

    produtos = Produto.objects.all()
    return render(request, "management/products/edit.html", {"produtos": produtos})


@login_required
def product_delete(request, id=0):
    if request.method == "POST":
        produto_id = request.POST.get("produto")
        confirm_delete = request.POST.get("confirmDelete")

        if confirm_delete:
            produto = get_object_or_404(Produto, id=produto_id)
            produto.delete()
            messages.success(request, "Produto excluído com sucesso!")
            return redirect("product_delete")
        else:
            messages.error(request, "Você precisa confirmar a exclusão.")

    produtos = Produto.objects.all()
    return render(request, "management/products/delete.html", {"produtos": produtos})


@login_required
def download_products(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="produtos.csv"'

    writer = csv.writer(response)
    writer.writerow(["ID", "Nome", "Preço", "Categoria", "Estoque"])

    produtos = Produto.objects.all()
    for produto in produtos:
        writer.writerow(
            [
                produto.id,
                produto.nome,
                produto.preco,
                produto.categoria,
                produto.estoque,
            ]
        )

    return response


# Clients
@login_required
def client_create(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        cpf = request.POST.get("cpf")
        email = request.POST.get("email")
        telefone = request.POST.get("telefone")

        # Usando CPF como senha inicial
        Cliente.objects.create(
            nome=nome,
            cpf=cpf,
            email=email,
            telefone=telefone,
            senha=cpf,  # O método __init__ do modelo cuidará da criptografia
        )

        messages.success(request, "Cliente cadastrado com sucesso!")
        return redirect("client_create")

    return render(request, "management/clients/create.html")


@login_required
def client_edit(request, id=0):
    if request.method == "POST":
        cliente_id = request.POST.get("cliente")
        nome = request.POST.get("nome")
        cpf = request.POST.get("cpf")
        email = request.POST.get("email")
        telefone = request.POST.get("telefone")

        cliente = get_object_or_404(Cliente, id=cliente_id)
        cliente.nome = nome
        cliente.cpf = cpf
        cliente.email = email
        cliente.telefone = telefone
        cliente.save()

        messages.success(request, "Cliente alterado com sucesso!")
        return redirect("client_edit", id=0)

    clientes = Cliente.objects.all()
    return render(request, "management/clients/edit.html", {"clientes": clientes})


@login_required
def client_delete(request, id=0):
    if request.method == "POST":
        cliente_id = request.POST.get("cliente")

        cliente = get_object_or_404(Cliente, id=cliente_id)
        cliente.delete()

        messages.success(request, "Cliente excluído com sucesso!")
        return redirect("client_delete")

    clientes = Cliente.objects.all()
    return render(request, "management/clients/delete.html", {"clientes": clientes})


# Cart
@login_required
def shopping_cart(request):
    user_id = request.session.get("user_id")
    cart_items = Carrinho.objects.filter(cliente_id=user_id)

    total = Decimal("0.00")
    for item in cart_items:
        item.subtotal = item.produto.preco * item.quantidade
        total += item.subtotal

    return render(
        request,
        "cart/shopping_cart.html",
        {"cart_items": cart_items, "cart_total": total},
    )


@login_required
def add_to_cart(request, product_id):
    if request.method == "POST":
        user_id = request.session.get("user_id")
        quantidade = Decimal(request.POST.get("quantidade", 1))

        produto = get_object_or_404(Produto, id=product_id)

        # Verifica se já existe no carrinho
        try:
            carrinho_item = Carrinho.objects.get(
                cliente_id=user_id, produto_id=product_id
            )
            carrinho_item.quantidade += quantidade
            carrinho_item.save()
        except Carrinho.DoesNotExist:
            Carrinho.objects.create(
                cliente_id=user_id, produto_id=product_id, quantidade=quantidade
            )

        messages.success(request, "Produto adicionado ao carrinho!")

        # Redireciona de volta para a página de origem
        referer = request.META.get("HTTP_REFERER")
        if referer:
            return redirect(referer)
        return redirect("products")


@login_required
def remove_from_cart(request, item_id):
    if request.method == "POST":
        carrinho_item = get_object_or_404(Carrinho, id=item_id)
        carrinho_item.delete()

        messages.success(request, "Item removido do carrinho!")

        # Redireciona de volta para a página de origem
        referer = request.META.get("HTTP_REFERER")
        if referer:
            return redirect(referer)
        return redirect("cart")


@login_required
def checkout(request):
    user_id = request.session.get("user_id")
    cart_items = Carrinho.objects.filter(cliente_id=user_id)

    total = Decimal("0.00")
    for item in cart_items:
        item.subtotal = item.produto.preco * item.quantidade
        total += item.subtotal

    return render(
        request, "cart/checkout.html", {"cart_items": cart_items, "cart_total": total}
    )


# Purchases
@login_required
def make_purchase(request):
    user_id = request.session.get("user_id")

    # Itens do carrinho
    cart_items = Carrinho.objects.filter(cliente_id=user_id)

    total = Decimal("0.00")
    for item in cart_items:
        item.subtotal = item.produto.preco * item.quantidade
        total += item.subtotal

    # Produtos disponíveis
    produtos = Produto.objects.all()

    return render(
        request,
        "purchases/make_purchase.html",
        {"produtos": produtos, "cart_items": cart_items, "cart_total": total},
    )


@login_required
def my_purchases(request):
    user_id = request.session.get("user_id")
    compras = ClienteProduto.objects.filter(cliente_id=user_id)

    return render(request, "purchases/my_purchase.html", {"compras": compras})


@login_required
def mark_as_retrieved(request, id):
    if request.method == "POST":
        compra = get_object_or_404(ClienteProduto, id=id)
        # Aqui você implementaria a lógica para marcar como retirado
        # Por exemplo, deletar o registro ou atualizar um status

        messages.success(request, "Produto marcado como retirado com sucesso!")
        return redirect("my_purchases")


@login_required
def will_retrieve(request, id):
    if request.method == "POST":
        compra = get_object_or_404(ClienteProduto, id=id)
        # Aqui você implementaria a lógica para marcar como "vai retirar"

        messages.success(request, "Status atualizado com sucesso!")
        return redirect("my_purchases")


# Debts
@login_required
def debt_query(request):
    user_id = request.session.get("user_id")
    is_staff = request.session.get("is_staff", False)

    if is_staff:
        # Para funcionários/admin, pode filtrar por cliente
        cliente_id = request.GET.get("cliente", "")
        data_inicio = request.GET.get("data_inicio", "")
        data_fim = request.GET.get("data_fim", "")

        dividas = ClienteProduto.objects.all()

        if cliente_id:
            dividas = dividas.filter(cliente_id=cliente_id)

        if data_inicio:
            dividas = dividas.filter(data__gte=data_inicio)

        if data_fim:
            dividas = dividas.filter(data__lte=data_fim)

        clientes = Cliente.objects.all()
    else:
        # Para clientes normais, mostra apenas suas próprias dívidas
        dividas = ClienteProduto.objects.filter(cliente_id=user_id)
        clientes = []

    # Calcular total
    total_pendente = sum(divida.total for divida in dividas)

    return render(
        request,
        "management/debts/query.html",
        {"dividas": dividas, "clientes": clientes, "total_pendente": total_pendente},
    )


@login_required
def debt_update(request):
    # Esta view seria apenas para admin/funcionários
    if not request.session.get("is_staff", False):
        messages.error(request, "Acesso negado.")
        return redirect("home")

    cliente_id = request.GET.get("cliente", "")
    data_inicio = request.GET.get("data_inicio", "")
    data_fim = request.GET.get("data_fim", "")

    dividas = ClienteProduto.objects.all()

    if cliente_id:
        dividas = dividas.filter(cliente_id=cliente_id)

    if data_inicio:
        dividas = dividas.filter(data__gte=data_inicio)

    if data_fim:
        dividas = dividas.filter(data__lte=data_fim)

    clientes = Cliente.objects.all()
    total_pendente = sum(divida.total for divida in dividas)

    return render(
        request,
        "management/debts/update.html",
        {"dividas": dividas, "clientes": clientes, "total_pendente": total_pendente},
    )


# Support
@login_required
def support(request):
    if request.method == "POST":
        assunto = request.POST.get("assunto")
        mensagem = request.POST.get("mensagem")

        # Aqui você implementaria o envio da mensagem de suporte
        # Por exemplo, envio de email ou salvamento em um modelo de mensagens

        messages.success(
            request, "Mensagem enviada com sucesso! Em breve entraremos em contato."
        )
        return redirect("support")

    return render(request, "support/contact.html")
