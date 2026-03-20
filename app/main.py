#   - `GET /categoria/<id>` → dettaglio categoria con lista prodotti
#   - `GET /crea_categoria` → form per nuova categoria
#   - `POST /crea_categoria` → salva categoria nel DB
#   - `GET /crea_prodotto` → form per nuovo prodotto (select categoria)
#   - `POST /crea_prodotto` → salva prodotto nel DB


from flask import Blueprint, flash, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from app.repositories import product_repository, categoria_repository



bp = Blueprint("main", __name__)

@bp.route("/")
def index():


    # 1. Prendiamo i canali dal database
    categorie: list[dict] = categoria_repository.get_all_categories()

    # 2. Passiamo la variabile 'channels' al template
    return render_template("index.html", categorie=categorie)


@bp.route("/cateegoria/<int:id>")
def category_detail(id):
    category = product_repository.get_channel_by_id(id)
    if category is None:
        abort(404, "Canale non trovato.")

    # 2. Prendiamo i prodotti della categoria
    categories = product_repository.get_products_by_category(id)

    # 3. Passiamo al template
    return render_template("categoria_detail.html", category=category, categories=categories)

