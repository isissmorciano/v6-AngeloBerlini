DROP TABLE IF EXISTS prodotti;
DROP TABLE IF EXISTS categorie;

CREATE TABLE categorie (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nome TEXT NOT NULL
);

CREATE TABLE prodotti (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  categoria_id INTEGER NOT NULL,
  nome TEXT NOT NULL,
  prezzo REAL NOT NULL,
  FOREIGN KEY (categoria_id) REFERENCES categorie (id)
);

-- Dati di esempio
INSERT INTO categorie (nome) VALUES ('Elettronica');
INSERT INTO categorie (nome) VALUES ('Libri');
INSERT INTO categorie (nome) VALUES ('Abbigliamento');

INSERT INTO prodotti (categoria_id, nome, prezzo) VALUES (1, 'Laptop', 999.99);
INSERT INTO prodotti (categoria_id, nome, prezzo) VALUES (1, 'Mouse', 29.99);
INSERT INTO prodotti (categoria_id, nome, prezzo) VALUES (2, 'Python 101', 39.99);
INSERT INTO prodotti (categoria_id, nome, prezzo) VALUES (2, 'Flask Guida', 34.99);
INSERT INTO prodotti (categoria_id, nome, prezzo) VALUES (3, 'Maglietta', 19.99);