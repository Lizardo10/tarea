const apiUrl = 'http://localhost:5000/api/alumnos';

document.addEventListener('DOMContentLoaded', cargarAlumnos);
document.getElementById('formulario').addEventListener('submit', guardarAlumno);

function cargarAlumnos() {
  fetch(apiUrl)
    .then(res => res.json())
    .then(data => {
      const lista = document.getElementById('lista');
      lista.innerHTML = '';
      data.forEach(alumno => {
        const li = document.createElement('li');
        li.textContent = `${alumno.nombre} ${alumno.apellido} - Edad: ${alumno.edad}`;

        const editarBtn = document.createElement('button');
        editarBtn.textContent = 'Editar';
        editarBtn.onclick = () => cargarFormulario(alumno);

        const eliminarBtn = document.createElement('button');
        eliminarBtn.textContent = 'Eliminar';
        eliminarBtn.onclick = () => eliminarAlumno(alumno.id);

        li.appendChild(editarBtn);
        li.appendChild(eliminarBtn);
        lista.appendChild(li);
      });
    });
}

function guardarAlumno(e) {
  e.preventDefault();
  const id = document.getElementById('id').value;
  const nombre = document.getElementById('nombre').value;
  const apellido = document.getElementById('apellido').value;
  const edad = document.getElementById('edad').value;

  const alumno = { nombre, apellido, edad };

  if (id) {
    fetch(`${apiUrl}/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(alumno)
    }).then(() => {
      document.getElementById('formulario').reset();
      cargarAlumnos();
    });
  } else {
    fetch(apiUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(alumno)
    }).then(() => {
      document.getElementById('formulario').reset();
      cargarAlumnos();
    });
  }
}

function cargarFormulario(alumno) {
  document.getElementById('id').value = alumno.id;
  document.getElementById('nombre').value = alumno.nombre;
  document.getElementById('apellido').value = alumno.apellido;
  document.getElementById('edad').value = alumno.edad;
}

function eliminarAlumno(id) {
  fetch(`${apiUrl}/${id}`, {
    method: 'DELETE'
  }).then(cargarAlumnos);
}