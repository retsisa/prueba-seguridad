"""
Laboratorio 8 - Auditoria de Sistemas
Mini aplicacion de practica INTENCIONALMENTE vulnerable a SQL Injection.

USO EXCLUSIVO: practica academica personal con sqlmap.
No subir datos reales. No usar contra terceros. No dejar publico mas
tiempo del necesario para el laboratorio.
"""

import os
import sqlite3
from flask import Flask, request, render_template

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), "prueba.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)
    # Datos de ejemplo (ficticios) para que sqlmap tenga algo que extraer
    cur.execute("SELECT COUNT(*) FROM usuarios")
    if cur.fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO usuarios (usuario, password) VALUES (?, ?)",
            [
                ("admin", "Adm1n_Lab8_2026"),
                ("carlos", "practica123"),
                ("auditor", "Clave_Segura!"),
            ],
        )
    conn.commit()
    conn.close()


@app.route("/", methods=["GET"])
def home():
    return render_template("login.html", error=None)


@app.route("/login", methods=["GET"])
def login():
    """
    Endpoint VULNERABLE A PROPOSITO.
    El parametro 'usuario' se concatena directamente en la consulta SQL,
    sin sanitizar ni usar parametros preparados. Esto permite inyeccion SQL
    clasica por el parametro GET 'usuario', por ejemplo:

        /login?usuario=admin' OR '1'='1&password=cualquiercosa

    o para usar con sqlmap directamente:

        sqlmap -u "https://TU-APP.onrender.com/login?usuario=admin&password=x" --dbs
        sqlmap -u "https://TU-APP.onrender.com/login?usuario=admin&password=x" -D prueba -T usuarios --dump
    """
    usuario = request.args.get("usuario", "")
    password = request.args.get("password", "")

    conn = get_db()
    cur = conn.cursor()

    # --- LINEA VULNERABLE A PROPOSITO (NO HACER ESTO EN PRODUCCION) ---
    query = "SELECT * FROM usuarios WHERE usuario = '%s' AND password = '%s'" % (usuario, password)
    try:
        cur.execute(query)
        row = cur.fetchone()
    except sqlite3.OperationalError:
        row = None
    conn.close()

    if row:
        return render_template("bienvenida.html", usuario=row["usuario"])
    return render_template("login.html", error="Usuario o contraseña incorrectos.")


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
else:
    # Cuando Render/gunicorn importa el modulo, igual inicializamos la BD
    init_db()
