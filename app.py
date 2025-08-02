from flask import Flask, render_template, request, redirect, url_for
from db_config import get_connection

app = Flask(__name__)

# Mostrar todos los alumnos
@app.route('/')
def index():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM alumno")
    alumnos = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', alumnos=alumnos)

# Crear un nuevo alumno
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        edad = request.form['edad']

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO alumno (nombre, apellido, edad) VALUES (%s, %s, %s)", 
                    (nombre, apellido, edad))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))
    return render_template('create.html')

# Actualizar un alumno
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    conn = get_connection()
    cur = conn.cursor()
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        edad = request.form['edad']
        cur.execute("UPDATE alumno SET nombre=%s, apellido=%s, edad=%s WHERE id=%s",
                    (nombre, apellido, edad, id))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))
    else:
        cur.execute("SELECT * FROM alumno WHERE id = %s", (id,))
        alumno = cur.fetchone()
        cur.close()
        conn.close()
        return render_template('update.html', alumno=alumno)

# Eliminar un alumno
@app.route('/delete/<int:id>')
def delete(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM alumno WHERE id = %s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
