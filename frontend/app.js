const API_URL = "http://127.0.0.1:5000/alumnos";

async function obtenerAlumnos() {
    let search = document.getElementById("buscar").value;
    let res = await fetch(`${API_URL}?search=${search}`);
    let alumnos = await res.json();

    let tbody = document.getElementById("tabla-alumnos");
    tbody.innerHTML = "";

    alumnos.forEach(a => {
        tbody.innerHTML += `
            <tr>
                <td>${a.id}</td>
                <td><input type="text" value="${a.nombre}" id="nombre-${a.id}"></td>
                <td><input type="number" value="${a.edad}" id="edad-${a.id}"></td>
                <td><input type="text" value="${a.curso}" id="curso-${a.id}"></td>
                <td>
                    <button onclick="actualizarAlumno(${a.id})">💾</button>
                    <button onclick="eliminarAlumno(${a.id})">🗑️</button>
                </td>
            </tr>
        `;
    });
}

async function crearAlumno() {
    let nombre = document.getElementById("nombre").value;
    let edad = document.getElementById("edad").value;
    let curso = document.getElementById("curso").value;

    await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nombre, edad, curso })
    });
    obtenerAlumnos();
}

async function actualizarAlumno(id) {
    let nombre = document.getElementById(`nombre-${id}`).value;
    let edad = document.getElementById(`edad-${id}`).value;
    let curso = document.getElementById(`curso-${id}`).value;

    await fetch(`${API_URL}/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nombre, edad, curso })
    });
    obtenerAlumnos();
}

async function eliminarAlumno(id) {
    await fetch(`${API_URL}/${id}`, { method: "DELETE" });
    obtenerAlumnos();
}

document.addEventListener("DOMContentLoaded", obtenerAlumnos);
