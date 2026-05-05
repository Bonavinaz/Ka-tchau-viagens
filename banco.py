import sqlite3

conn = sqlite3.connect("banco.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS carros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        marca TEXT NOT NULL,
        preco_dia REAL,
        disponivel INTEGER DEFAULT 1,
        imagem TEXT,
        descricao TEXT
    )
""")

carros = [
    ("Fiat Argo 2025", 150.00, 1, "AE-Fiat-Argo-Drive-10-8-scaled-e1758229233410.jpeg", "Hatchback compacto, econômico e moderno. Ideal para uso urbano."),
    ("Chevrolet Tracker 2021", 220.00, 1, "c7-chevrolet-tracker-2-jpg.jpg", "SUV compacto com estilo, tecnologia e conforto para o dia a dia."),
    ("Ford Focus ST-Line X 2024", 200.00, 1, "maxresdefault.jpg", "Hatch médio com visual esportivo e ótimo desempenho nas estradas."),
    ("Fiat Argodwd 2025", 150.00, 1, "AE-Fiadawdt-Argo-Drive-10-8-scaled-e1758229233410.jpeg", "Hatchbackdawd compacto, econômico e moderno. Ideal para uso urbano."),
]

cursor.executemany("""
    INSERT INTO carros (marca, preco_dia, disponivel, imagem, descricao)
    VALUES (?, ?, ?, ?, ?)  
""", carros)

conn.commit()
conn.close()

print("Banco criado com sucesso!")