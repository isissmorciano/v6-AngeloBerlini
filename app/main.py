

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

@bp.route("/create_category", methods=("GET", "POST"))
def create_category():
    if request.method == "POST":
        nome = request.form["nome"]
        error = None

        if not nome:
            error = "Il nome è obbligatorio."

        if error is not None:
            flash(error)
        else:
            # Creiamo la categoria
            categoria_repository.create_category(nome)
            return redirect(url_for("main.index"))
    
    categoria = categoria_repository.get_all_categories()
    return render_template("crea_categoria.html",categoria = categoria)
    
        
@bp.route("/crea_prodotto", methods=("GET", "POST"))
def crea_prodotto():
    if request.method == "POST":
        categoria_id = request.form.get("categorie_id", type=int)
        nome = request.form["nome"]
        prezzo = request.form["prezzo"]
        error = None

        if not nome:
            error = "Il nome è obbligatorio."
        
        
        if prezzo is None or prezzo <= 0:
            error = "Il prezzo deve essere un numero positivo."
        
        

        if error is not None:
            flash(error)
        else:
            # Creiamo il video
            product_repository.create_product(categoria_id, nome, prezzo)
            return redirect(url_for("main.categoria_detail", id=categoria_id))
    
    prodotto = product_repository.get_all_products()
    return render_template("crea_prodotto.html",prodotto=prodotto)
        

@bp.route("/ricerca_prodotto",methods=("GET", "POST"))
def ricerca_prodotto():
    if request.method == "POST":
        search_term = request.form["ricerca"]
        error = None

        if not search_term:
            error = "inserire il termine di ricerca"

        if error is not None:
            flash(error)
        else:
            # Creiamo il video
            product_repository.find_products_by_name(search_term)
            return redirect(url_for("main.categoria_detail", search_term = search_term))
        
    

