#File app/repositories/product_repository.py:
#
from app.db import get_db

def get_all_products():
    """
    Recupera tutti i prodotti.
    """
    db = get_db()
    query = """
        SELECT prodotti.id, prodotti.nome, prodotti.prezzo
        FROM prodotti
        JOIN categorie ON prodotti.categoria_id = categorie.id
    """
    prodotti = db.execute(query).fetchall()
    return [dict(prodotto) for prodotto in prodotti]

def get_products_by_category(category_id):
    db = get_db()
    query = """
        SELECT *
        FROM categorie
        JOIN categorie ON prodotti.categoria_id = categorie.id
    """
    products = db.execute(query, (category_id,)).fetchall()
    return [dict(product) for product in products]


def get_product_by_id(product_id):
    """Recupera un singolo prodotto per ID."""
    db = get_db()
    query = """
        SELECT *
        FROM prodotti
        WHERE id = ?
    """
    product = db.execute(query, (product_id,)).fetchone()
    if product:
        return dict(product)
    return None

def create_product(catergory_id,nome,prezzo):
    """Crea un nuovo prodotto."""
    db = get_db()
    cursor = db.execute(
        "INSERT INTO prodotti (catergory_id,nome,prezzo) VALUES (?, ?, ?)",
        (catergory_id,nome,prezzo),
    )
    db.commit()
    return cursor.lastrowid