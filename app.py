from flask import Flask, render_template
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

if __name__ == "__main__":
    app.run(debug=True)