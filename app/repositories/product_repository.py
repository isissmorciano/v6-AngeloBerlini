from app.db import get_db


def get_all_products():
    """Recupera tutti i prodotti con il nome della categoria."""
    db = get_db()
    query = """
        SELECT prodotti.id, prodotti.nome, prodotti.prezzo, prodotti.categoria_id, categorie.nome AS categoria_nome
        FROM prodotti
        JOIN categorie ON prodotti.categoria_id = categorie.id
    """
    prodotti = db.execute(query).fetchall()
    return [dict(p) for p in prodotti]


def get_products_by_category(category_id):
    """Recupera i prodotti di una specifica categoria."""
    db = get_db()
    query = """
        SELECT prodotti.id, prodotti.nome, prodotti.prezzo, categorie.nome AS categoria_nome
        FROM prodotti
        JOIN categorie ON prodotti.categoria_id = categorie.id
        WHERE prodotti.categoria_id = ?
        ORDER BY prodotti.nome ASC
    """
    products = db.execute(query, (category_id,)).fetchall()
    return [dict(product) for product in products]


def get_product_by_id(product_id):
    """Recupera un singolo prodotto per ID."""
    db = get_db()
    query = "SELECT * FROM prodotti WHERE id = ?"
    product = db.execute(query, (product_id,)).fetchone()
    if product:
        return dict(product)
    return None


def create_product(categoria_id, nome, prezzo):
    """Crea un nuovo prodotto."""
    db = get_db()
    cursor = db.execute(
        "INSERT INTO prodotti (categoria_id, nome, prezzo) VALUES (?, ?, ?)",
        (categoria_id, nome, prezzo),
    )
    db.commit()
    return cursor.lastrowid


def find_products_by_name(search_term):
    db = get_db()
    query = """
        SELECT prodotti.id, prodotti.nome, prodotti.prezzo, categorie.nome AS categoria_nome
        FROM prodotti
        JOIN categorie ON prodotti.categoria_id = categorie.id
        WHERE prodotti.nome LIKE ?
        ORDER BY categorie.nome ASC
    """
    prodotti = db.execute(query, (f'%{search_term}%',)).fetchall()
    return [dict(prodotto) for prodotto in prodotti]