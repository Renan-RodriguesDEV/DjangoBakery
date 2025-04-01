# Sistema de Gerenciamento de Padaria 🥖

Sistema web desenvolvido em Python usando Django para gerenciamento de uma padaria, com funcionalidades para clientes e funcionários/proprietários.

## 🛠️ Tecnologias Utilizadas

- Python 3.8+
- Django 5.1
- MySQL/MariaDB
- HTML/CSS/JavaScript
- Bootstrap
- FontAwesome

## 📋 Funcionalidades

### Área do Cliente

- Login/Cadastro de clientes
- Catálogo de produtos
- Carrinho de compras
- Histórico de compras
- Consulta de pendências/dívidas
- Reset de senha
- Suporte ao usuário

### Área do Proprietário/Funcionário

- Gerenciamento de produtos
- Gerenciamento de clientes
- Controle de estoque
- Gestão de dívidas
- Download de relatórios

## 🗄️ Estrutura do Banco de Dados

- Produtos
- Clientes
- ClienteProduto (Vendas)
- Carrinho
- Dívidas
- Usuários (Funcionários)

## 💻 Como Executar

1. Clone o repositório
2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Configure o banco de dados no arquivo settings.py
4. Execute as migrações:

```bash
python manage.py migrate
```

5. Inicie o servidor:

```bash
python manage.py runserver
```

## 🔧 Configuração do Banco de Dados

Edite o arquivo `bakery/settings.py` para configurar a conexão com o banco de dados:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "django_bakery",
        "USER": "seu_usuario",
        "PASSWORD": "sua_senha",
        "HOST": "localhost",
        "PORT": "3306",
        "OPTIONS": {
            "charset": "utf8mb4",
        },
    }
}
```

## 🎨 Customização

O projeto utiliza Bootstrap e FontAwesome para estilização, tornando fácil a personalização dos temas e componentes visuais.

## 📱 Preview da Interface

- Interface responsiva com Bootstrap
- Ícones intuitivos com FontAwesome
- Layout moderno e amigável
- Navegação simplificada

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma issue ou enviar um pull request.

## 📄 Licença

Este projeto está sob a licença MIT.

---

Developer: Renan Rodrigues [(@little_renan.py)](https://instagram.com/__little_renan__.py)