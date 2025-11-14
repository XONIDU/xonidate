from flask import Flask, request, redirect, url_for, send_file, flash, get_flashed_messages
from fpdf import FPDF
from random import choice

app = Flask(__name__)
app.secret_key = "clave_secreta_xonidu"

# Inicialización de las listas globales
list_p = []
list_d = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
list_c = []
list_l = []

# HTML integrado directamente en el código
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        action = request.form.get("action")
        if action == "add_person":
            person = request.form.get("person")
            if person:
                list_p.append(person)
                flash(f"Asistente '{person}' agregado ✅.")
        elif action == "remove_day":
            day = request.form.get("day")
            if day in list_d:
                list_d.remove(day)
                flash(f"Día '{day}' eliminado ❌.")
        elif action == "add_food":
            food = request.form.get("food")
            if food:
                list_c.append(food)
                flash(f"Comida '{food}' agregada 🍴.")
        elif action == "add_place":
            place = request.form.get("place")
            if place:
                list_l.append(place)
                flash(f"Lugar '{place}' agregado 🏙️.")
        elif action == "generate":
            if not list_d:
                flash("No hay días disponibles para generar la cita ❗")
            else:
                dia = choice(list_d)
                comida = choice(list_c) if list_c else "No definida"
                lugar = choice(list_l) if list_l else "No definido"
                filename = generate_pdf(dia, comida, lugar, list_p)
                return send_file(filename, as_attachment=True)
        return redirect(url_for("index"))  # Evitar reenvío de formularios en actualizaciones

    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Generador de Citas - XONIDU</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
                text-align: center;
                background: #f4f4f9;
            }}
            .container {{
                display: inline-block;
                width: 90%;
                max-width: 500px;
                text-align: left;
                padding: 15px;
                background: white;
                border: 1px solid #ccc;
                border-radius: 10px;
                box-shadow: 0px 3px 6px rgba(0, 0, 0, 0.1);
            }}
            form {{
                margin: 1em 0;
            }}
            input[type="text"], select, button {{
                margin: 5px 0;
                padding: 10px;
                width: 100%;
                border-radius: 5px;
                border: 1px solid #ddd;
            }}
            button {{
                background: #007BFF;
                color: white;
                border: none;
                cursor: pointer;
            }}
            button:hover {{
                background: #0056b3;
            }}
            .flash {{
                color: green;
                margin: 5px 0;
            }}
        </style>
    </head>
    <body>
        <h1>Generador de Citas - XONIDU</h1>
        <div class="container">
            <h2>Asistentes:</h2>
            <form method="POST">
                <input type="hidden" name="action" value="add_person">
                <input type="text" name="person" placeholder="Ingresa un nombre" required>
                <button type="submit">Añadir Asistente</button>
            </form>

            <h2>Días no disponibles:</h2>
            <form method="POST">
                <input type="hidden" name="action" value="remove_day">
                <select name="day">
                    {"".join([f"<option value='{day}'>{day}</option>" for day in list_d])}
                </select>
                <button type="submit">Eliminar Día</button>
            </form>

            <h2>Comidas:</h2>
            <form method="POST">
                <input type="hidden" name="action" value="add_food">
                <input type="text" name="food" placeholder="Ejemplo: Pizza" required>
                <button type="submit">Añadir Comida</button>
            </form>

            <h2>Lugares:</h2>
            <form method="POST">
                <input type="hidden" name="action" value="add_place">
                <input type="text" name="place" placeholder="Ejemplo: Parque" required>
                <button type="submit">Añadir Lugar</button>
            </form>

            <h2>Generar Cita:</h2>
            <form method="POST">
                <input type="hidden" name="action" value="generate">
                <button type="submit">Generar y Descargar PDF</button>
            </form>

            <!-- Mostrar mensajes flash -->
            <div class="flash">
                {"<br>".join(get_flashed_messages())}
            </div>
        </div>
    </body>
    </html>
    """

# Función para generar el PDF
def generate_pdf(dia, comida, lugar, asistentes):
    filename = "cita.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Resumen de la Cita", 0, 1, "C")
    pdf.ln(10)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Día: {dia}", 0, 1)
    pdf.cell(0, 10, f"Lugar: {lugar}", 0, 1)
    pdf.cell(0, 10, f"Comida: {comida}", 0, 1)
    pdf.ln(5)
    pdf.cell(0, 10, "Asistentes:", 0, 1)
    for person in asistentes:
        pdf.cell(0, 10, f"- {person}", 0, 1)
    pdf.output(filename)
    return filename

# Correr la aplicación
if __name__ == "__main__":
    app.run(debug=True)
