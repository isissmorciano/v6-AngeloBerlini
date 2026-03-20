# 🧱 TEMPLATE FLASK + SQLite — COMPLETO

> Sostituisci **`elemento`/`elementi`** con il nome della tua entità principale  
> Sostituisci **`sottoelemento`/`sottoelementi`** con la seconda entità  
> Sostituisci **`campo1, campo2, campo3`** con i tuoi campi reali

---

## 📁 STRUTTURA CARTELLE

```
progetto/
├── run.py
├── setup_db.py
└── app/
    ├── __init__.py
    ├── db.py
    ├── schema.sql
    ├── repositories/
    │   ├── elementi_repo.py
    │   └── sottoelementi_repo.py
    ├── main.py
    └── templates/
        ├── base.html
        ├── index.html
        ├── create_elemento.html
        ├── create_sottoelemento.html
        ├── edit_elemento.html
        └── sottoelementi_elemento.html
```

---

## 🔧 run.py

```python
from app import create_app
from random import randint

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=randint(2000, 9000))
```

---

## 🔧 setup_db.py

```python
import sqlite3
import os

if not os.path.exists('instance'):
    os.makedirs('instance')

db_path = os.path.join('instance', 'mio_db.sqlite')
connection = sqlite3.connect(db_path)

with open('app/schema.sql') as f:
    connection.executescript(f.read())

print("Database creato in:", db_path)
connection.close()
```

---

## 🔧 app/__init__.py

```python
import os
from flask import Flask

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'mio_db.sqlite'),
    )

    os.makedirs(app.instance_path, exist_ok=True)

    from app import db
    db.init_app(app)

    from app import main
    app.register_blueprint(main.bp)

    return app
```

---

## 🔧 app/db.py

```python
import sqlite3
from flask import current_app, g

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db)
```

---

## 🗄️ app/schema.sql

```sql
DROP TABLE IF EXISTS sottoelementi;
DROP TABLE IF EXISTS elementi;

CREATE TABLE elementi (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    campo1    TEXT    NOT NULL,
    campo2    INTEGER NOT NULL,
    campo3    TEXT    NOT NULL
);

CREATE TABLE sottoelementi (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    elemento_id  INTEGER NOT NULL,
    campo_a      TEXT    NOT NULL,
    campo_b      INTEGER NOT NULL,
    FOREIGN KEY (elemento_id) REFERENCES elementi(id)
);

-- Dati di esempio
INSERT INTO elementi (campo1, campo2, campo3) VALUES ('Esempio1', 10, 'CategoriaA');
INSERT INTO elementi (campo1, campo2, campo3) VALUES ('Esempio2', 20, 'CategoriaB');
INSERT INTO elementi (campo1, campo2, campo3) VALUES ('Altro',    5,  'CategoriaA');

INSERT INTO sottoelementi (elemento_id, campo_a, campo_b) VALUES (1, 'Alice', 100);
INSERT INTO sottoelementi (elemento_id, campo_a, campo_b) VALUES (1, 'Bob',   200);
INSERT INTO sottoelementi (elemento_id, campo_a, campo_b) VALUES (2, 'Carlo', 150);
```

---

## 🗄️ app/repositories/elementi_repo.py

```python
from app.db import get_db

# ── LEGGI TUTTI ───────────────────────────────────────────────────────────────
def get_elementi():
    db = get_db()
    risultati = db.execute('SELECT * FROM elementi ORDER BY id').fetchall()
    return [dict(r) for r in risultati]

# ── LEGGI UNO PER ID ──────────────────────────────────────────────────────────
def get_elemento_id(id):
    db = get_db()
    risultato = db.execute('SELECT * FROM elementi WHERE id = ?', (id,)).fetchone()
    if risultato:
        return dict(risultato)
    return None

# ── CREA ──────────────────────────────────────────────────────────────────────
def create_elemento(campo1, campo2, campo3):
    db = get_db()
    query = 'INSERT INTO elementi (campo1, campo2, campo3) VALUES (?, ?, ?)'
    cursor = db.execute(query, (campo1, campo2, campo3))
    db.commit()
    return cursor.lastrowid

# ── MODIFICA ──────────────────────────────────────────────────────────────────
def update_elemento(id, campo1, campo2, campo3):
    db = get_db()
    query = 'UPDATE elementi SET campo1=?, campo2=?, campo3=? WHERE id=?'
    db.execute(query, (campo1, campo2, campo3, id))
    db.commit()

# ── ELIMINA ───────────────────────────────────────────────────────────────────
def delete_elemento(id):
    db = get_db()
    db.execute('DELETE FROM elementi WHERE id = ?', (id,))
    db.commit()

# ── CERCA CON LIKE (ricerca testuale su campo1) ───────────────────────────────
def cerca_elementi(testo):
    db = get_db()
    # %testo% → contiene  |  testo% → inizia con  |  %testo → finisce con
    query = 'SELECT * FROM elementi WHERE campo1 LIKE ? ORDER BY campo1'
    risultati = db.execute(query, (f'%{testo}%',)).fetchall()
    return [dict(r) for r in risultati]

# ── FILTRA PER VALORE ESATTO DI UN CAMPO ──────────────────────────────────────
def get_elementi_per_categoria(categoria):
    db = get_db()
    query = 'SELECT * FROM elementi WHERE campo3 = ? ORDER BY campo1'
    risultati = db.execute(query, (categoria,)).fetchall()
    return [dict(r) for r in risultati]

# ── FILTRA CON CONFRONTO NUMERICO (>, <, >=, <=) ─────────────────────────────
def get_elementi_maggiori_di(valore):
    db = get_db()
    query = 'SELECT * FROM elementi WHERE campo2 > ? ORDER BY campo2 DESC'
    risultati = db.execute(query, (valore,)).fetchall()
    return [dict(r) for r in risultati]

# ── ORDINA PER COLONNA (ASC o DESC) ──────────────────────────────────────────
def get_elementi_ordinati(colonna='campo1', direzione='ASC'):
    db = get_db()
    # ATTENZIONE: colonna non va passata come ? ma va messa nella stringa
    # Validare prima per sicurezza!
    colonne_valide = ['id', 'campo1', 'campo2', 'campo3']
    if colonna not in colonne_valide:
        colonna = 'id'
    query = f'SELECT * FROM elementi ORDER BY {colonna} {direzione}'
    risultati = db.execute(query).fetchall()
    return [dict(r) for r in risultati]

# ── CONTA QUANTI ELEMENTI CI SONO ─────────────────────────────────────────────
def conta_elementi():
    db = get_db()
    risultato = db.execute('SELECT COUNT(*) as totale FROM elementi').fetchone()
    return risultato['totale']

# ── FUNZIONI AGGREGATE (MAX, MIN, AVG, SUM) ───────────────────────────────────
def statistiche_campo2():
    db = get_db()
    risultato = db.execute('''
        SELECT 
            MAX(campo2) as massimo,
            MIN(campo2) as minimo,
            AVG(campo2) as media,
            SUM(campo2) as totale
        FROM elementi
    ''').fetchone()
    return dict(risultato)

# ── FILTRA CON PIÙ CONDIZIONI (AND / OR) ─────────────────────────────────────
def get_elementi_filtrati(campo3, valore_minimo):
    db = get_db()
    query = '''
        SELECT * FROM elementi
        WHERE campo3 = ? AND campo2 >= ?
        ORDER BY campo2 DESC
    '''
    risultati = db.execute(query, (campo3, valore_minimo)).fetchall()
    return [dict(r) for r in risultati]

# ── JOIN: prende elementi con i loro sottoelementi ───────────────────────────
def get_elementi_con_sottoelementi():
    db = get_db()
    query = '''
        SELECT 
            elementi.id,
            elementi.campo1,
            elementi.campo3,
            sottoelementi.campo_a,
            sottoelementi.campo_b
        FROM elementi
        JOIN sottoelementi ON elementi.id = sottoelementi.elemento_id
        ORDER BY elementi.id
    '''
    risultati = db.execute(query).fetchall()
    return [dict(r) for r in risultati]

# ── LEFT JOIN: tutti gli elementi, anche senza sottoelementi ─────────────────
def get_tutti_elementi_con_sotto():
    db = get_db()
    query = '''
        SELECT 
            elementi.id,
            elementi.campo1,
            sottoelementi.campo_a
        FROM elementi
        LEFT JOIN sottoelementi ON elementi.id = sottoelementi.elemento_id
        ORDER BY elementi.id
    '''
    risultati = db.execute(query).fetchall()
    return [dict(r) for r in risultati]

# ── GROUP BY: conta i sottoelementi per ogni elemento ────────────────────────
def conta_sotto_per_elemento():
    db = get_db()
    query = '''
        SELECT 
            elementi.id,
            elementi.campo1,
            COUNT(sottoelementi.id) as numero_sotto
        FROM elementi
        LEFT JOIN sottoelementi ON elementi.id = sottoelementi.elemento_id
        GROUP BY elementi.id
        ORDER BY numero_sotto DESC
    '''
    risultati = db.execute(query).fetchall()
    return [dict(r) for r in risultati]
```

---

## 🗄️ app/repositories/sottoelementi_repo.py

```python
from app.db import get_db

# ── LEGGI TUTTI DI UN ELEMENTO ────────────────────────────────────────────────
def get_sottoelementi_id(elemento_id):
    db = get_db()
    risultati = db.execute(
        'SELECT * FROM sottoelementi WHERE elemento_id = ?', (elemento_id,)
    ).fetchall()
    return [dict(r) for r in risultati]

# ── CREA ──────────────────────────────────────────────────────────────────────
def create_sottoelemento(elemento_id, campo_a, campo_b):
    db = get_db()
    query = 'INSERT INTO sottoelementi (elemento_id, campo_a, campo_b) VALUES (?, ?, ?)'
    cursor = db.execute(query, (elemento_id, campo_a, campo_b))
    db.commit()
    return cursor.lastrowid

# ── ELIMINA ───────────────────────────────────────────────────────────────────
def delete_sottoelemento(id):
    db = get_db()
    db.execute('DELETE FROM sottoelementi WHERE id = ?', (id,))
    db.commit()

# ── CERCA CON LIKE ────────────────────────────────────────────────────────────
def cerca_sottoelementi(testo):
    db = get_db()
    risultati = db.execute(
        'SELECT * FROM sottoelementi WHERE campo_a LIKE ?', (f'%{testo}%',)
    ).fetchall()
    return [dict(r) for r in risultati]

# ── ORDINA PER campo_b DECRESCENTE ───────────────────────────────────────────
def get_sottoelementi_ordinati(elemento_id):
    db = get_db()
    risultati = db.execute(
        'SELECT * FROM sottoelementi WHERE elemento_id = ? ORDER BY campo_b DESC',
        (elemento_id,)
    ).fetchall()
    return [dict(r) for r in risultati]

# ── IL MASSIMO DI campo_b PER UN ELEMENTO ────────────────────────────────────
def get_massimo_campo_b(elemento_id):
    db = get_db()
    risultato = db.execute(
        'SELECT MAX(campo_b) as massimo FROM sottoelementi WHERE elemento_id = ?',
        (elemento_id,)
    ).fetchone()
    return risultato['massimo']
```

---

## 🔧 app/main.py

```python
from flask import Blueprint, flash, redirect, render_template, request, url_for
from app.repositories import elementi_repo, sottoelementi_repo

bp = Blueprint('main', __name__)

# ── HOME: lista tutti gli elementi ───────────────────────────────────────────
@bp.route('/')
def index():
    lista = elementi_repo.get_elementi()
    return render_template('index.html', lista_elementi=lista)

# ── RICERCA CON LIKE ─────────────────────────────────────────────────────────
# L'utente digita nella barra di ricerca → URL: /?q=testo
@bp.route('/cerca')
def cerca():
    testo = request.args.get('q', '')   # prende il parametro GET dalla URL
    risultati = elementi_repo.cerca_elementi(testo)
    return render_template('index.html', lista_elementi=risultati, ricerca=testo)

# ── CREA ELEMENTO ─────────────────────────────────────────────────────────────
@bp.route('/crea_elemento', methods=('GET', 'POST'))
def create_elemento():
    if request.method == 'POST':
        campo1 = request.form['campo1']
        campo2 = request.form['campo2']
        campo3 = request.form['campo3']
        error = None

        if not campo1:
            error = 'campo1 è obbligatorio.'
        if not campo3:
            error = 'campo3 è obbligatorio.'

        if error:
            flash(error)
        else:
            elementi_repo.create_elemento(campo1, campo2, campo3)
            return redirect(url_for('main.index'))

    return render_template('create_elemento.html')

# ── MODIFICA ELEMENTO ─────────────────────────────────────────────────────────
@bp.route('/modifica_elemento/<int:id>', methods=('GET', 'POST'))
def edit_elemento(id):
    elemento = elementi_repo.get_elemento_id(id)

    if request.method == 'POST':
        campo1 = request.form['campo1']
        campo2 = request.form['campo2']
        campo3 = request.form['campo3']
        error = None

        if not campo1:
            error = 'campo1 è obbligatorio.'

        if error:
            flash(error)
        else:
            elementi_repo.update_elemento(id, campo1, campo2, campo3)
            return redirect(url_for('main.index'))

    return render_template('edit_elemento.html', elemento=elemento)

# ── ELIMINA ELEMENTO ──────────────────────────────────────────────────────────
@bp.route('/elimina_elemento/<int:id>')
def delete_elemento(id):
    elementi_repo.delete_elemento(id)
    return redirect(url_for('main.index'))

# ── LISTA SOTTOELEMENTI ───────────────────────────────────────────────────────
@bp.route('/sottoelementi/<int:id>')
def sottoelementi_elemento(id):
    elemento = elementi_repo.get_elemento_id(id)
    sottoelementi = sottoelementi_repo.get_sottoelementi_id(id)
    return render_template('sottoelementi_elemento.html',
                           elemento=elemento,
                           sottoelementi=sottoelementi)

# ── CREA SOTTOELEMENTO ────────────────────────────────────────────────────────
@bp.route('/nuovo_sottoelemento/<int:id>', methods=('GET', 'POST'))
def create_sottoelemento(id):
    if request.method == 'POST':
        campo_a = request.form['campo_a']
        campo_b = request.form['campo_b']
        error = None

        if not campo_a:
            error = 'campo_a è obbligatorio.'

        if error:
            flash(error)
        else:
            sottoelementi_repo.create_sottoelemento(id, campo_a, campo_b)
            return redirect(url_for('main.sottoelementi_elemento', id=id))

    return render_template('create_sottoelemento.html')

# ── ELIMINA SOTTOELEMENTO ─────────────────────────────────────────────────────
@bp.route('/elimina_sottoelemento/<int:id>/<int:id_elemento>')
def delete_sottoelemento(id, id_elemento):
    sottoelementi_repo.delete_sottoelemento(id)
    return redirect(url_for('main.sottoelementi_elemento', id=id_elemento))
```

---

## 🌐 templates/base.html

```html
<!doctype html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <title>La Mia App</title>
    <style>
        body { background-color: #f0f4ff; font-family: sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        nav { background-color: #3355aa; padding: 10px; border-radius: 8px; }
        nav a { color: white; text-decoration: none; margin-right: 15px; }
        .elimina { background: red; color: white; border: none; cursor: pointer; padding: 5px 10px; border-radius: 5px; }
        .modifica { background: orange; color: white; border: none; cursor: pointer; padding: 5px 10px; border-radius: 5px; }
        .flash { color: red; border: 1px solid red; padding: 10px; margin: 10px 0; }
        hr { border: 0; border-top: 1px solid #ccc; }
    </style>
</head>
<body>
    {% for message in get_flashed_messages() %}
        <div class="flash">{{ message }}</div>
    {% endfor %}

    <nav>
        <a href="{{ url_for('main.index') }}">🏠 Home</a>
        <a href="{{ url_for('main.create_elemento') }}">➕ Crea Elemento</a>
    </nav>

    <main>{% block content %}{% endblock %}</main>

    <hr>
    <footer><small>&copy; 2025 - La Mia App</small></footer>
</body>
</html>
```

---

## 🌐 templates/index.html

```html
{% extends 'base.html' %}

{% block content %}
<h1>Lista Elementi</h1>

<!-- Barra di ricerca (LIKE) -->
<form method="get" action="{{ url_for('main.cerca') }}">
    <input type="text" name="q" placeholder="Cerca..." value="{{ ricerca if ricerca else '' }}">
    <button type="submit">🔍 Cerca</button>
</form>

{% for elemento in lista_elementi %}
<article>
    <h2>
        <a href="{{ url_for('main.sottoelementi_elemento', id=elemento['id']) }}">
            {{ elemento['campo1'] }}
        </a>
    </h2>
    <p>campo2: {{ elemento['campo2'] }}</p>
    <p>campo3: {{ elemento['campo3'] }}</p>

    <a href="{{ url_for('main.edit_elemento', id=elemento['id']) }}">
        <button class="modifica">✏️ Modifica</button>
    </a>
    <a href="{{ url_for('main.delete_elemento', id=elemento['id']) }}">
        <button class="elimina">🗑 Elimina</button>
    </a>
</article>
<hr>
{% else %}
    <p>Nessun elemento trovato.</p>
{% endfor %}
{% endblock %}
```

---

## 🌐 templates/create_elemento.html

```html
{% extends 'base.html' %}

{% block content %}
<h1>Crea Nuovo Elemento</h1>
<form method="post">
    <label for="campo1">campo1</label>
    <input type="text" name="campo1" id="campo1" required><br><br>

    <label for="campo2">campo2</label>
    <input type="number" name="campo2" id="campo2" required><br><br>

    <label for="campo3">campo3</label>
    <input type="text" name="campo3" id="campo3" required><br><br>

    <input type="submit" value="Crea">
</form>
{% endblock %}
```

---

## 🌐 templates/edit_elemento.html  ← NUOVO (per la modifica)

```html
{% extends 'base.html' %}

{% block content %}
<h1>Modifica Elemento</h1>
<form method="post">
    <label for="campo1">campo1</label>
    <!-- value="..." precompila il campo con i dati attuali -->
    <input type="text" name="campo1" id="campo1" value="{{ elemento['campo1'] }}" required><br><br>

    <label for="campo2">campo2</label>
    <input type="number" name="campo2" id="campo2" value="{{ elemento['campo2'] }}" required><br><br>

    <label for="campo3">campo3</label>
    <input type="text" name="campo3" id="campo3" value="{{ elemento['campo3'] }}" required><br><br>

    <input type="submit" value="Salva Modifiche">
</form>
{% endblock %}
```

---

## 🌐 templates/sottoelementi_elemento.html

```html
{% extends 'base.html' %}

{% block content %}
<h1>{{ elemento['campo1'] }}</h1>

{% for sotto in sottoelementi %}
<article>
    <p>campo_a: {{ sotto['campo_a'] }}</p>
    <p>campo_b: {{ sotto['campo_b'] }}</p>
    <a href="{{ url_for('main.delete_sottoelemento', id=sotto['id'], id_elemento=elemento['id']) }}">
        <button class="elimina">🗑 Elimina</button>
    </a>
</article>
<hr>
{% else %}
    <p>Nessun sottoelemento presente.</p>
{% endfor %}

<a href="{{ url_for('main.create_sottoelemento', id=elemento['id']) }}">
    <button>➕ Aggiungi</button>
</a>
{% endblock %}
```

---

## 🌐 templates/create_sottoelemento.html

```html
{% extends 'base.html' %}

{% block content %}
<h1>Aggiungi Sottoelemento</h1>
<form method="post">
    <label for="campo_a">campo_a</label>
    <input type="text" name="campo_a" id="campo_a" required><br><br>

    <label for="campo_b">campo_b</label>
    <input type="number" name="campo_b" id="campo_b" required><br><br>

    <input type="submit" value="Aggiungi">
</form>
{% endblock %}
```

---

## 📚 TUTTE LE QUERY SQL UTILI — Cheatsheet

```python
db = get_db()

# ── SELECT BASE ───────────────────────────────────────────────────────────────
db.execute('SELECT * FROM elementi').fetchall()                  # tutti
db.execute('SELECT * FROM elementi').fetchone()                  # solo il primo
db.execute('SELECT campo1, campo2 FROM elementi').fetchall()     # solo alcune colonne

# ── WHERE ─────────────────────────────────────────────────────────────────────
db.execute('SELECT * FROM elementi WHERE id = ?', (id,))
db.execute('SELECT * FROM elementi WHERE campo3 = ?', (valore,))
db.execute('SELECT * FROM elementi WHERE campo2 > ?', (10,))
db.execute('SELECT * FROM elementi WHERE campo2 BETWEEN ? AND ?', (5, 20))

# ── LIKE ──────────────────────────────────────────────────────────────────────
db.execute('SELECT * FROM elementi WHERE campo1 LIKE ?', ('%testo%',))  # contiene
db.execute('SELECT * FROM elementi WHERE campo1 LIKE ?', ('testo%',))   # inizia con
db.execute('SELECT * FROM elementi WHERE campo1 LIKE ?', ('%testo',))   # finisce con

# ── AND / OR ──────────────────────────────────────────────────────────────────
db.execute('SELECT * FROM elementi WHERE campo3 = ? AND campo2 > ?', (cat, val))
db.execute('SELECT * FROM elementi WHERE campo3 = ? OR campo3 = ?', (cat1, cat2))

# ── ORDER BY ──────────────────────────────────────────────────────────────────
db.execute('SELECT * FROM elementi ORDER BY campo1 ASC')    # A→Z
db.execute('SELECT * FROM elementi ORDER BY campo2 DESC')   # dal più grande

# ── LIMIT ─────────────────────────────────────────────────────────────────────
db.execute('SELECT * FROM elementi ORDER BY id DESC LIMIT 5')  # ultimi 5 inseriti

# ── COUNT / MAX / MIN / AVG / SUM ────────────────────────────────────────────
db.execute('SELECT COUNT(*) as totale FROM elementi').fetchone()['totale']
db.execute('SELECT MAX(campo2) as m FROM elementi').fetchone()['m']
db.execute('SELECT MIN(campo2) as m FROM elementi').fetchone()['m']
db.execute('SELECT AVG(campo2) as m FROM elementi').fetchone()['m']
db.execute('SELECT SUM(campo2) as m FROM elementi').fetchone()['m']

# ── GROUP BY ──────────────────────────────────────────────────────────────────
db.execute('''
    SELECT campo3, COUNT(*) as totale
    FROM elementi
    GROUP BY campo3
''').fetchall()

# ── JOIN ──────────────────────────────────────────────────────────────────────
db.execute('''
    SELECT elementi.campo1, sottoelementi.campo_a
    FROM elementi
    JOIN sottoelementi ON elementi.id = sottoelementi.elemento_id
''').fetchall()

# ── LEFT JOIN (include anche chi non ha figli) ────────────────────────────────
db.execute('''
    SELECT elementi.campo1, sottoelementi.campo_a
    FROM elementi
    LEFT JOIN sottoelementi ON elementi.id = sottoelementi.elemento_id
''').fetchall()

# ── INSERT ────────────────────────────────────────────────────────────────────
cursor = db.execute('INSERT INTO elementi (campo1, campo2) VALUES (?, ?)', (v1, v2))
db.commit()
cursor.lastrowid   # restituisce l'id dell'elemento appena creato

# ── UPDATE ────────────────────────────────────────────────────────────────────
db.execute('UPDATE elementi SET campo1=?, campo2=? WHERE id=?', (v1, v2, id))
db.commit()

# ── DELETE ────────────────────────────────────────────────────────────────────
db.execute('DELETE FROM elementi WHERE id = ?', (id,))
db.commit()
```

---

## 📌 COSE DA RICORDARE IN VERIFICA

| Concetto | Cosa fare |
|---|---|
| Leggere parametro dal form (POST) | `request.form['nome_campo']` |
| Leggere parametro dalla URL (GET) | `request.args.get('nome', '')` |
| Passare variabile al template | `render_template('pagina.html', variabile=valore)` |
| Usarla nel template | `{{ variabile }}` o `{{ dizionario['chiave'] }}` |
| Ciclo in Jinja2 | `{% for x in lista %}...{% endfor %}` |
| Condizione in Jinja2 | `{% if condizione %}...{% endif %}` |
| Nessun risultato nel for | `{% for x in lista %}...{% else %}<p>Vuoto</p>{% endfor %}` |
| Redirect dopo POST | `return redirect(url_for('main.nome_funzione'))` |
| Messaggio di errore | `flash('testo errore')` → `get_flashed_messages()` nel template |
| Precompilare un form | `value="{{ elemento['campo1'] }}"` nell'input |
| LIKE: contiene | `WHERE campo LIKE ?` con `('%testo%',)` |
| LIKE: inizia con | `WHERE campo LIKE ?` con `('testo%',)` |
| Query con JOIN | `FROM a JOIN b ON a.id = b.a_id` |
| Sempre fare commit dopo INSERT/UPDATE/DELETE | `db.commit()` |

---

## 🚀 AVVIO RAPIDO

```bash
python setup_db.py   # crea il database
python run.py        # avvia il server
```