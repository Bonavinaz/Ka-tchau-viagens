from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "chave_local_para_dev")

def get_db():
    conn = sqlite3.connect("banco.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    conn = get_db()
    carros = conn.execute("SELECT * FROM carros").fetchall()
    conn.close()
    return render_template("index.html", carros=carros)

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    erro = None
    if request.method == "POST":
        nome = request.form["nome"]
        usuario = request.form["usuario"]
        email = request.form["email"]
        senha = request.form["senha"]
        confirma_senha = request.form["confirma_senha"]

        if senha != confirma_senha:
            erro = "Senhas não coincidem!"

        else:
            conn = get_db()
            try:
                conn.execute(
                    "INSERT INTO usuarios (nome, usuario, email, senha) VALUES (?, ?, ?, ?)",
                    (nome, usuario, email, senha)
                )
                conn.commit()
                return redirect("/cadastro?sucesso=1")
            except:
                erro = "Email ou usuário já cadastrado!"
            finally:
                conn.close()

    return render_template("cadastro.html", erro=erro)


@app.route("/login", methods=["POST"])
def login():
    login_input = request.form["login"]
    senha = request.form["senha"]

    conn = get_db()
    usuario = conn.execute(
        "SELECT * FROM usuarios WHERE (usuario = ? OR email = ?) AND senha = ?",
        (login_input, login_input, senha)
    ).fetchone()
    conn.close()

    if usuario:
        session["usuario_id"] = usuario["id"]
        session["usuario_nome"] = usuario["nome"]
        session["usuario_tipo"] = usuario["tipo"]
        return redirect("/")
    else:
        origem = request.referrer or "/"
        return redirect(origem + "?login_erro=1")

@app.route("/catalogo")
def catalogo():
    conn = get_db()
    q = request.args.get("q", "")
    categoria = request.args.get("categoria", "")
    
    if q and categoria:
        carros = conn.execute(
            "SELECT * FROM carros WHERE marca LIKE ? AND categoria LIKE ?", (f"%{q}%", f"%{categoria}%")
        ).fetchall()
    elif q:
        carros = conn.execute(
            "SELECT * FROM carros WHERE marca LIKE ?", (f"%{q}%",)
        ).fetchall()
    elif categoria:
        carros = conn.execute(
            "SELECT * FROM carros WHERE categoria LIKE ?", (f"%{categoria}%",)
        ).fetchall()
    else:
        carros = conn.execute("SELECT * FROM carros").fetchall()
    
    conn.close()
    return render_template("catalogo.html", carros=carros)
    
@app.route("/dashboard")
def dashboard():
    if not session.get("usuario_id"):
        return redirect("/?erro=login")
    
    if session.get("usuario_tipo") != "admin":
        return redirect("/")
    
    conn = get_db()

    # total de veículos
    total = conn.execute("SELECT COUNT(*) FROM carros").fetchone()[0]
    
    # carros disponíveis
    disponiveis = conn.execute("SELECT COUNT(*) FROM carros WHERE disponivel = 1").fetchone()[0]
    
    # carros alugados
    alugados = conn.execute("SELECT COUNT(*) FROM carros WHERE disponivel = 0").fetchone()[0]

    # receita por carro
    receita_total = conn.execute("""
        SELECT COALESCE(SUM(preco_dia), 0) as total
        FROM carros
        WHERE disponivel = 0
    """).fetchone()[0]

    # lista de alugueis com cliente e status
    alugueis = conn.execute("""
        SELECT carros.marca, carros.ano, carros.preco_dia,
            carros.disponivel, usuarios.nome
        FROM carros
        LEFT JOIN alugueis ON carros.id = alugueis.carro_id AND alugueis.data_fim IS NULL
        LEFT JOIN usuarios ON usuarios.id = alugueis.usuario_id
        GROUP BY carros.id
    """).fetchall()
    
    conn.close()
    return render_template("dashboard.html",
        total=total,
        disponiveis=disponiveis,
        alugados=alugados,
        receita_total=receita_total,
        alugueis=alugueis
    )

@app.route("/alugar/<int:carro_id>")
def alugar(carro_id):
    conn = get_db()

    if not session.get("usuario_id"):
        return redirect("/?erro=login")
    
    # verifica se já tem um carro alugado
    aluguel_ativo = conn.execute("""
        SELECT * FROM alugueis WHERE usuario_id = ? AND data_fim IS NULL
    """, (session["usuario_id"],)).fetchone()
    
    if aluguel_ativo:
        conn.close()
        return redirect("/catalogo?erro=ja_alugado")
    
    # verifica se o carro está disponível
    carro = conn.execute("SELECT * FROM carros WHERE id = ?", (carro_id,)).fetchone()
    
    if not carro or carro["disponivel"] == 0:
        conn.close()
        return redirect("/catalogo?erro=indisponivel")
    
    # aluga o carro
    conn.execute("INSERT INTO alugueis (carro_id, usuario_id) VALUES (?, ?)", 
                 (carro_id, session["usuario_id"]))
    conn.execute("UPDATE carros SET disponivel = 0 WHERE id = ?", (carro_id,))
    conn.commit()
    conn.close()
    
    return redirect("/catalogo?sucesso=alugado")

@app.route("/perfil")
def perfil():
    if not session.get("usuario_id"):
        return redirect("/?erro=login")
    
    conn = get_db()
    
    usuario = conn.execute(
        "SELECT * FROM usuarios WHERE id = ?", (session["usuario_id"],)
    ).fetchone()
    
    carro_atual = conn.execute("""
        SELECT carros.id, carros.marca FROM alugueis
        JOIN carros ON carros.id = alugueis.carro_id
        WHERE alugueis.usuario_id = ? AND alugueis.data_fim IS NULL
    """, (session["usuario_id"],)).fetchone()
    
    historico = conn.execute("""
        SELECT carros.marca, carros.ano, alugueis.data_inicio, alugueis.data_fim
        FROM alugueis
        JOIN carros ON carros.id = alugueis.carro_id
        WHERE alugueis.usuario_id = ?
        ORDER BY alugueis.id DESC
    """, (session["usuario_id"],)).fetchall()
        
    conn.close()
    return render_template("perfil.html",
        usuario=usuario,
        carro_atual=carro_atual,
        historico=historico
    )

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/devolver/<int:carro_id>")
def devolver(carro_id):
    if not session.get("usuario_id"):
        return redirect("/?erro=login")
    
    conn = get_db()
    conn.execute("""
        UPDATE alugueis SET data_fim = datetime('now') 
        WHERE carro_id = ? AND usuario_id = ?
    """, (carro_id, session["usuario_id"]))
    conn.execute("UPDATE carros SET disponivel = 1 WHERE id = ?", (carro_id,))
    conn.commit()
    conn.close()
    
    return redirect("/perfil")

if __name__ == "__main__":
    app.run(debug=True)