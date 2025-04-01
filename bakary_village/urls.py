from django.urls import path
from . import views


urlpatterns = [
    # Home
    path("", views.home, name="home"),
    # Accounts
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("account/", views.my_account, name="my_account"),
    path("password/reset/", views.forgot_password, name="forgot_password"),
    # Products
    path("products/", views.products_list, name="products"),
    path("products/add/", views.product_create, name="product_create"),
    path("products/edit/<int:id>/", views.product_edit, name="product_edit"),
    path("products/delete/<int:id>/", views.product_delete, name="product_delete"),
    path("products/download/", views.download_products, name="download_products"),
    # Clients
    path("clients/add/", views.client_create, name="client_create"),
    path("clients/edit/<int:id>/", views.client_edit, name="client_edit"),
    path("clients/delete/<int:id>/", views.client_delete, name="client_delete"),
    # Cart
    path("cart/", views.shopping_cart, name="cart"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("cart/checkout/", views.checkout, name="checkout"),
    # Purchases
    path("purchase/", views.make_purchase, name="make_purchase"),
    path("my-purchases/", views.my_purchases, name="my_purchases"),
    path(
        "my-purchases/retrieved/<int:id>/",
        views.mark_as_retrieved,
        name="mark_as_retrieved",
    ),
    path(
        "my-purchases/will-retrieve/<int:id>/",
        views.will_retrieve,
        name="will_retrieve",
    ),
    # Debts
    path("debts/query/", views.debt_query, name="debt_query"),
    path("debts/update/", views.debt_update, name="debt_update"),
    # Support
    path("support/", views.support, name="support"),
]
