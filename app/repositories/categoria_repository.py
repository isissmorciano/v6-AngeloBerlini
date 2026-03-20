#File app/repositories/categoria_repository.py:


from app.db import get_db


def create_category(nome: str):
    """Crea una nuova categoria."""
    db = get_db()
    # La tabella nello schema si chiama 'categorie'
    cursor = db.execute(
        "INSERT INTO categorie (nome) VALUES (?)", (nome,)
    )
    db.commit()
    return cursor.lastrowid

def get_all_categories():
    """
    Recupera tutte le categorie.
    """
    db = get_db()
    query = """
        SELECT * FROM categorie ORDER BY nome
    """
    categories = db.execute(query).fetchall()
    return [dict(category) for category in categories]



def get_category_by_id(category_id):
    db = get_db()
    query = """
        SELECT *
        FROM categorie
        WHERE categorie.id = ?
    """
    category = db.execute(query,(category_id) ).fetchone()
    if category:
        return dict(category)
    return None


