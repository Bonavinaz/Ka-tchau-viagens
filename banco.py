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
    ("Fiat Argo", "2025", 150.00, 1, "AE-Fiat-Argo-Drive-10-8-scaled-e1758229233410.jpeg", "Hatchback compacto, econômico e moderno. Ideal para uso urbano.", "Hatch,Populares"),
    ("Chevrolet Tracker", "2021", 220.00, 1, "c7-chevrolet-tracker-2-jpg.jpg", "SUV compacto com estilo, tecnologia e conforto para o dia a dia.", "SUV"),
    ("Ford Focus ST-Line X", "2024", 200.00, 1, "maxresdefault.jpg", "Hatch médio com visual esportivo e ótimo desempenho nas estradas.", "Hatch,Populares"),
    ("Jeep Avenger", "2024", 250.00, 1, "avenger.webp", "SUV moderno, robusto e ideal para viagens com estilo e segurança.", "SUV"),
    ("Audi A6", "2025", 600.00, 1, "audi-a6.jpg", "Sedã executivo de luxo, confortável e sofisticado para ocasiões especiais.", "Sedã"),
    ("Toyota Yaris Sedan", "2025", 170.00, 1, "yaris.jpg", "Sedã econômico, confortável e excelente para o uso diário.", "Sedã,Populares"),
    ("Ford Mustang Shelby GT500", "2013", 850.00, 1, "ford-mustang-2013.jpeg", "Muscle car americano com motor V8 superalimentado de 662 cv e sonoro escapamento esportivo.", "Esportivos"),
    ("Lamborghini Revuelto", "2023", 4500.00, 1, "revuelto.png", "Híbrido V12 da Lamborghini com 1001 cv, sucessor do Aventador com design futurista e desempenho brutal.", "Esportivos"),
    ("Ram 2500 Power Wagon", "2017", 620.00, 1, "power wagon.png", "Caminhonete off-road de alta capacidade com tração 4x4 e suspensão reforçada para os terrenos mais difíceis.", "Caminhonetes"),
    ("Ford F 150", "2021", 480.00, 1, "f 150.png", "A picape mais vendida do mundo, versátil e potente, com carroceria de alumínio e tecnologia de ponta.", "Caminhonetes"),
    ("Lykan Hypersport", "2013", 6500.00, 1, "lykan.png", "Superesportivo árabe com 780 cv, faróis cravejados com pedras preciosas e um dos carros mais raros do mundo.", "Superesportivos de Luxo"),
    ("Ferrari LaFerrari Stradale", "2014", 7200.00, 1, "stradale.png", "Híbrido de 963 cv da Ferrari, topo absoluto da linha com tecnologia direta da Fórmula 1.", "Superesportivos de Luxo"),
    ("Bentley Continental Supersports", "2017", 2800.00, 1, "bentley.png", "Gran turismo britânico com interior luxuoso em couro e W12 de 700 cv para longas viagens com requinte.", "luxo,Sedã"),
    ("Cadillac CTS-V Sedan", "2016", 980.00, 1, "cadilac.png", "Sedã americano de alto desempenho com V8 superalimentado de 640 cv e postura esportiva agressiva.", "luxo,Sedã"),
    ("Nissan Skyline R34 V-Spec", "1999", 1200.00, 1, "r34.png", "Lenda japonesa do tuning com tração integral ATTESA e motor RB26 biturbo, ícone dos anos 90.", "Esportivos"),
]

usuarios = [
    ("Admin", "admin", "admin@gmail.com", "123", "admin"),
    ("Rodrigo Fulano", "cliente", "teste@gmail.com", "123", "cliente"),
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