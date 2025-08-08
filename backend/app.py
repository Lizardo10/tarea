from flask import Flask, request, jsonify
from flask_cors import CORS
from db import get_connection

app = Flask(__name__)
CORS(app)

# 📌 Obtener todos los alumnos
@app.route("/alumnos", methods=["GET"])
def obtener_alumnos():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nombre, edad, curso FROM alumnos ORDER BY id ASC;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    alumnos = [{"id": r[0], "nombre": r[1], "edad": r[2], "curso": r[3]} for r in rows]
    return jsonify(alumnos)

# 📌 Buscar alumno por nombre
@app.route("/alumnos/buscar", methods=["GET"])
def buscar_alumno():
    nombre = request.args.get("nombre", "")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nombre, edad, curso FROM alumnos WHERE nombre ILIKE %s;", (f"%{nombre}%",))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    alumnos = [{"id": r[0], "nombre": r[1], "edad": r[2], "curso": r[3]} for r in rows]
    return jsonify(alumnos)

# 📌 Crear alumno
@app.route("/alumnos", methods=["POST"])
def crear_alumno():
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO alumnos (nombre, edad, curso) VALUES (%s, %s, %s) RETURNING id;",
        (data["nombre"], data["edad"], data["curso"])
    )
    nuevo_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Alumno creado", "id": nuevo_id})

# 📌 Actualizar alumno
@app.route("/alumnos/<int:id>", methods=["PUT"])
def actualizar_alumno(id):
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE alumnos SET nombre=%s, edad=%s, curso=%s WHERE id=%s;",
        (data["nombre"], data["edad"], data["curso"], id)
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Alumno actualizado"})

# 📌 Eliminar alumno
@app.route("/alumnos/<int:id>", methods=["DELETE"])
def eliminar_alumno(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM alumnos WHERE id=%s;", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Alumno eliminado"})

if __name__ == "__main__":
    app.run(debug=True)
