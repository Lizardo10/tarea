import os
import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

DB_PATH = os.getenv("DB_PATH", "alumnos.db")

app = Flask(__name__)
CORS(app)

# Conexión a la BD
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Crear tabla si no existe
with get_db_connection() as conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS alumnos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            edad INTEGER NOT NULL,
            curso TEXT NOT NULL
        )
    """)
    conn.commit()

# Obtener todos o buscar
@app.route("/alumnos", methods=["GET"])
def get_alumnos():
    search = request.args.get("search", "")
    conn = get_db_connection()
    if search:
        alumnos = conn.execute("SELECT * FROM alumnos WHERE nombre LIKE ?", (f"%{search}%",)).fetchall()
    else:
        alumnos = conn.execute("SELECT * FROM alumnos").fetchall()
    conn.close()
    return jsonify([dict(row) for row in alumnos])

# Crear alumno
@app.route("/alumnos", methods=["POST"])
def create_alumno():
    data = request.get_json()
    conn = get_db_connection()
    conn.execute("INSERT INTO alumnos (nombre, edad, curso) VALUES (?, ?, ?)",
                 (data["nombre"], data["edad"], data["curso"]))
    conn.commit()
    conn.close()
    return jsonify({"message": "Alumno creado"}), 201

# Actualizar alumno
@app.route("/alumnos/<int:id>", methods=["PUT"])
def update_alumno(id):
    data = request.get_json()
    conn = get_db_connection()
    conn.execute("UPDATE alumnos SET nombre=?, edad=?, curso=? WHERE id=?",
                 (data["nombre"], data["edad"], data["curso"], id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Alumno actualizado"})

# Eliminar alumno
@app.route("/alumnos/<int:id>", methods=["DELETE"])
def delete_alumno(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM alumnos WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Alumno eliminado"})

if __name__ == "__main__":
    app.run(debug=True)
