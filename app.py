from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

from db import init_db, get_all_alumnos, get_alumno, insert_alumno, update_alumno, delete_alumno

init_db()

@app.route('/api/alumnos', methods=['GET'])
def obtener_alumnos():
    return jsonify(get_all_alumnos())

@app.route('/api/alumnos/<int:id>', methods=['GET'])
def obtener_alumno(id):
    alumno = get_alumno(id)
    if alumno:
        return jsonify(alumno)
    return jsonify({'error': 'No encontrado'}), 404

@app.route('/api/alumnos', methods=['POST'])
def crear_alumno():
    data = request.json
    insert_alumno(data['nombre'], data['apellido'], data['edad'])
    return jsonify({'mensaje': 'Alumno creado'}), 201

@app.route('/api/alumnos/<int:id>', methods=['PUT'])
def actualizar_alumno(id):
    data = request.json
    update_alumno(id, data['nombre'], data['apellido'], data['edad'])
    return jsonify({'mensaje': 'Alumno actualizado'})

@app.route('/api/alumnos/<int:id>', methods=['DELETE'])
def eliminar_alumno(id):
    delete_alumno(id)
    return jsonify({'mensaje': 'Alumno eliminado'})

if __name__ == '__main__':
    app.run(debug=True)