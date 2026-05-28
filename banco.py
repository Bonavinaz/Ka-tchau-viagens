import sqlite3

conn = sqlite3.connect("banco.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS carros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        marca TEXT NOT NULL,
        ano TEXT NOT NULL,
        preco_dia REAL,
        disponivel INTEGER DEFAULT 1,
        imagem TEXT,
        descricao TEXT,
        categoria TEXT
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        usuario TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL,
        tipo TEXT DEFAULT 'cliente'
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS alugueis (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        carro_id INTEGER,
        usuario_id INTEGER,
        data_inicio TEXT DEFAULT (datetime('now')),
        data_fim TEXT DEFAULT NULL
    )
""")

carros = [
    ("Fiat Argo", "2025", 150.00, 1, "AE-Fiat-Argo-Drive-10-8-scaled-e1758229233410.jpeg", "Hatchback compacto, econômico e moderno. Ideal para uso urbano.", "Luxo,Superesportivos de Luxo"),
    ("Chevrolet Tracker", "2021", 220.00, 1, "c7-chevrolet-tracker-2-jpg.jpg", "SUV compacto com estilo, tecnologia e conforto para o dia a dia.", "SUV,Caminhonetes"),
    ("Ford Focus ST-Line X", "2024", 200.00, 1, "maxresdefault.jpg", "Hatch médio com visual esportivo e ótimo desempenho nas estradas.", "Populares,Esportivos"),
]

usuarios = [
    ("Admin", "admin", "admin@gmail.com", "123", "admin")
]

cursor.executemany("""
    INSERT INTO carros (marca, ano, preco_dia, disponivel, imagem, descricao, categoria)
    VALUES (?, ?, ?, ?, ?, ?, ?)
""", carros)

cursor.executemany("""
    INSERT INTO usuarios (nome, usuario, email, senha, tipo)
    VALUES (?, ?, ?, ?, ?)
""", usuarios)

conn.commit()
conn.close()

print("Banco criado com sucesso!")