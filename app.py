from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

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

@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")

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

if __name__ == "__main__":
    app.run(debug=True)