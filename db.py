import sqlite3

DB_NAME = 'alumnos.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alumno (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            edad INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def get_all_alumnos():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM alumno')
    rows = cursor.fetchall()
    conn.close()
    return [dict(id=r[0], nombre=r[1], apellido=r[2], edad=r[3]) for r in rows]

def get_alumno(id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM alumno WHERE id=?', (id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(id=row[0], nombre=row[1], apellido=row[2], edad=row[3])
    return None

def insert_alumno(nombre, apellido, edad):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO alumno (nombre, apellido, edad) VALUES (?, ?, ?)', (nombre, apellido, edad))
    conn.commit()
    conn.close()

def update_alumno(id, nombre, apellido, edad):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('UPDATE alumno SET nombre=?, apellido=?, edad=? WHERE id=?', (nombre, apellido, edad, id))
    conn.commit()
    conn.close()

def delete_alumno(id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM alumno WHERE id=?', (id,))
    conn.commit()
    conn.close()