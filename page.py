from flask import Flask, request, redirect, url_for, send_file, flash, get_flashed_messages, render_template_string
from fpdf import FPDF
from random import choice
import qrcode
import socket
import io
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "clave_secreta_xonidu"

# Inicialización de las listas globales
list_p = []
list_d = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
list_c = []
list_l = []

# HTML integrado directamente en el código
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generador de Citas - XONIDU</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            color: #333;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        
        .header h1 {
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 10px;
            letter-spacing: 1px;
        }
        
        .header p {
            font-size: 1.1rem;
            opacity: 0.9;
            margin-bottom: 20px;
        }
        
        .qr-section {
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            border-bottom: 1px solid #eaeaea;
        }
        
        .qr-info {
            display: inline-block;
            background: white;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            margin-bottom: 15px;
        }
        
        .qr-info p {
            margin: 5px 0;
            font-size: 0.9rem;
            color: #666;
        }
        
        .content {
            padding: 30px;
        }
        
        .section {
            margin-bottom: 30px;
            background: #f8f9fa;
            padding: 20px;
            border-radius: 15px;
            border-left: 4px solid #667eea;
        }
        
        .section h2 {
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.3rem;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .section h2 i {
            font-size: 1.2rem;
        }
        
        .form-grid {
            display: grid;
            grid-template-columns: 1fr auto;
            gap: 10px;
            align-items: center;
        }
        
        input[type="text"], select {
            padding: 12px 15px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 1rem;
            font-family: 'Poppins', sans-serif;
            transition: all 0.3s ease;
        }
        
        input[type="text"]:focus, select:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        button {
            padding: 12px 25px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            font-family: 'Poppins', sans-serif;
            letter-spacing: 0.5px;
        }
        
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.2);
        }
        
        .lists {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        
        .list-box {
            background: white;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
        }
        
        .list-box h3 {
            color: #764ba2;
            margin-bottom: 10px;
            font-size: 1.1rem;
            border-bottom: 2px solid #f0f0f0;
            padding-bottom: 5px;
        }
        
        .list-item {
            padding: 8px 0;
            border-bottom: 1px solid #f5f5f5;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .list-item:last-child {
            border-bottom: none;
        }
        
        .generate-btn {
            display: block;
            width: 100%;
            padding: 15px;
            font-size: 1.1rem;
            margin-top: 20px;
            background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%);
        }
        
        .flash-messages {
            margin: 20px 0;
        }
        
        .flash {
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 10px;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 10px;
            animation: slideIn 0.3s ease;
        }
        
        .flash-success {
            background: #d4edda;
            color: #155724;
            border-left: 4px solid #28a745;
        }
        
        .flash-warning {
            background: #fff3cd;
            color: #856404;
            border-left: 4px solid #ffc107;
        }
        
        .footer {
            text-align: center;
            padding: 20px;
            color: #666;
            font-size: 0.9rem;
            border-top: 1px solid #eaeaea;
            background: #f8f9fa;
        }
        
        @keyframes slideIn {
            from {
                transform: translateX(-20px);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        
        .badge {
            background: #667eea;
            color: white;
            padding: 3px 10px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 500;
        }
        
        @media (max-width: 768px) {
            .container {
                margin: 10px;
            }
            
            .header h1 {
                font-size: 2rem;
            }
            
            .content {
                padding: 20px;
            }
            
            .form-grid {
                grid-template-columns: 1fr;
            }
            
            .lists {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎉 Generador de Citas</h1>
            <p>Organiza tus encuentros sociales de forma fácil y divertida</p>
        </div>
        
        <div class="qr-section">
            <div class="qr-info">
                <p>📱 Escanea para acceder desde tu teléfono</p>
                <p>🔗 URL: {{ server_url }}</p>
            </div>
        </div>
        
        <div class="content">
            <div class="flash-messages">
                {% for message in get_flashed_messages() %}
                    <div class="flash flash-success">
                        {{ message }}
                    </div>
                {% endfor %}
            </div>
            
            <div class="section">
                <h2>👥 Asistentes</h2>
                <form method="POST" class="form-grid">
                    <input type="hidden" name="action" value="add_person">
                    <input type="text" name="person" placeholder="Ingresa el nombre del asistente" required>
                    <button type="submit">➕ Añadir Asistente</button>
                </form>
                <div class="list-box">
                    <h3>Asistentes Registrados <span class="badge">{{ list_p|length }}</span></h3>
                    {% for person in list_p %}
                        <div class="list-item">
                            <span>👤 {{ person }}</span>
                        </div>
                    {% endfor %}
                </div>
            </div>
            
            <div class="section">
                <h2>📅 Días Disponibles</h2>
                <form method="POST" class="form-grid">
                    <input type="hidden" name="action" value="remove_day">
                    <select name="day">
                        {% for day in list_d %}
                            <option value="{{ day }}">{{ day }}</option>
                        {% endfor %}
                    </select>
                    <button type="submit">🗑️ Eliminar Día</button>
                </form>
                <div class="list-box">
                    <h3>Días Disponibles <span class="badge">{{ list_d|length }}</span></h3>
                    {% for day in list_d %}
                        <div class="list-item">
                            <span>📅 {{ day }}</span>
                        </div>
                    {% endfor %}
                </div>
            </div>
            
            <div class="section">
                <h2>🍕 Comidas</h2>
                <form method="POST" class="form-grid">
                    <input type="hidden" name="action" value="add_food">
                    <input type="text" name="food" placeholder="Ejemplo: Pizza, Sushi, Tacos..." required>
                    <button type="submit">➕ Añadir Comida</button>
                </form>
                <div class="list-box">
                    <h3>Comidas Disponibles <span class="badge">{{ list_c|length }}</span></h3>
                    {% for food in list_c %}
                        <div class="list-item">
                            <span>🍴 {{ food }}</span>
                        </div>
                    {% endfor %}
                </div>
            </div>
            
            <div class="section">
                <h2>🏙️ Lugares</h2>
                <form method="POST" class="form-grid">
                    <input type="hidden" name="action" value="add_place">
                    <input type="text" name="place" placeholder="Ejemplo: Parque, Restaurante, Cine..." required>
                    <button type="submit">➕ Añadir Lugar</button>
                </form>
                <div class="list-box">
                    <h3>Lugares Disponibles <span class="badge">{{ list_l|length }}</span></h3>
                    {% for place in list_l %}
                        <div class="list-item">
                            <span>📍 {{ place }}</span>
                        </div>
                    {% endfor %}
                </div>
            </div>
            
            <form method="POST">
                <input type="hidden" name="action" value="generate">
                <button type="submit" class="generate-btn">
                    🎲 Generar Cita y Descargar PDF
                </button>
            </form>
        </div>
        
        <div class="footer">
            <p>Generador de Citas XONIDU © 2024 | Crea recuerdos increíbles</p>
        </div>
    </div>
</body>
</html>
"""

def get_server_ip():
    """Obtiene la dirección IP del servidor"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        try:
            s.connect(('10.254.254.254', 1))
            ip = s.getsockname()[0]
        except Exception:
            ip = '127.0.0.1'
        finally:
            s.close()
        return ip
    except Exception:
        return '127.0.0.1'

def generate_qr_code(url):
    """Genera un código QR para la URL"""
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        # Crear imagen del QR
        img = qr.make_image(fill_color="#667eea", back_color="white")
        
        # Guardar en bytes
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        return img_bytes
    except Exception:
        return None

def generate_terminal_qr(url):
    """Genera un código QR en ASCII para la terminal"""
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=2,
            border=1,
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        qr_text = qr.get_matrix()
        ascii_qr = ""
        for row in qr_text:
            for pixel in row:
                if pixel:
                    ascii_qr += "██"
                else:
                    ascii_qr += "  "
            ascii_qr += "\n"
        
        return ascii_qr
    except Exception:
        return ""

class ElegantPDF(FPDF):
    def __init__(self):
        super().__init__()
        # Usamos las fuentes estándar de FPDF que ya vienen instaladas
    
    def header(self):
        # Título principal
        self.set_font('Arial', 'B', 24)
        self.set_text_color(102, 126, 234)
        self.cell(0, 20, 'CITA GENERADA - XONIDU', 0, 1, 'C')
        self.ln(5)
        
        # Línea decorativa
        self.set_draw_color(102, 126, 234)
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(10)
    
    def footer(self):
        # Posición a 1.5 cm del final
        self.set_y(-15)
        # Fuente
        self.set_font('Arial', 'I', 8)
        # Número de página
        self.cell(0, 10, 'Pagina ' + str(self.page_no()), 0, 0, 'C')
    
    def add_gradient_background(self):
        # Añadir un fondo degradado sutil
        self.set_fill_color(240, 245, 255)
        self.rect(0, 0, 210, 297, 'F')
    
    def chapter_title(self, label):
        # Título de sección
        self.set_font('Arial', 'B', 16)
        self.set_text_color(102, 126, 234)
        self.set_fill_color(240, 245, 255)
        self.cell(0, 10, label, 0, 1, 'L', True)
        self.ln(4)
    
    def chapter_body(self, content):
        # Texto de la sección
        self.set_font('Arial', '', 12)
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 8, content)
        self.ln()
    
    def add_info_card(self, title, content):
        # Tarjeta de información
        self.set_fill_color(255, 255, 255)
        self.set_draw_color(220, 220, 220)
        self.set_line_width(0.3)
        
        # Guardar posición Y
        y = self.get_y()
        
        # Dibujar rectángulo
        self.rect(10, y, 190, 20, 'DF')
        
        # Título
        self.set_font('Arial', 'B', 12)
        self.set_text_color(102, 126, 234)
        self.set_xy(15, y + 5)
        self.cell(40, 10, title, 0, 0, 'L')
        
        # Contenido
        self.set_font('Arial', '', 12)
        self.set_text_color(30, 30, 30)
        self.set_xy(60, y + 5)
        self.cell(0, 10, content, 0, 1, 'L')
        
        # Mover posición Y
        self.set_y(y + 25)
    
    def add_attendants_list(self, attendants):
        # Lista de asistentes
        self.chapter_title("ASISTENTES")
        self.set_font('Arial', '', 12)
        self.set_text_color(50, 50, 50)
        
        for i, person in enumerate(attendants, 1):
            # Usar caracteres ASCII para viñetas
            self.cell(10, 8, f"{i}.", 0, 0, 'L')
            self.cell(0, 8, person, 0, 1, 'L')
        
        self.ln(10)

@app.route("/", methods=["GET", "POST"])
def index():
    global list_p, list_d, list_c, list_l
    
    if request.method == "POST":
        action = request.form.get("action")
        
        if action == "add_person":
            person = request.form.get("person", "").strip()
            if person and person not in list_p:
                list_p.append(person)
                flash(f"✅ Asistente '{person}' agregado exitosamente")
        
        elif action == "remove_day":
            day = request.form.get("day")
            if day in list_d:
                list_d.remove(day)
                flash(f"❌ Día '{day}' eliminado de las opciones")
        
        elif action == "add_food":
            food = request.form.get("food", "").strip()
            if food and food not in list_c:
                list_c.append(food)
                flash(f"🍴 Comida '{food}' agregada exitosamente")
        
        elif action == "add_place":
            place = request.form.get("place", "").strip()
            if place and place not in list_l:
                list_l.append(place)
                flash(f"🏙️ Lugar '{place}' agregado exitosamente")
        
        elif action == "generate":
            if not list_d:
                flash("⚠️ No hay días disponibles para generar la cita")
                return redirect(url_for("index"))
            
            if not list_p:
                flash("⚠️ Agrega al menos un asistente antes de generar")
                return redirect(url_for("index"))
            
            dia = choice(list_d)
            comida = choice(list_c) if list_c else "Por definir"
            lugar = choice(list_l) if list_l else "Por definir"
            
            filename = generate_pdf(dia, comida, lugar, list_p)
            flash("🎉 ¡Cita generada exitosamente! Descarga tu PDF")
            return send_file(filename, 
                           as_attachment=True, 
                           download_name=f"cita_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                           mimetype='application/pdf')
        
        return redirect(url_for("index"))
    
    # Obtener URL del servidor para el QR
    server_ip = get_server_ip()
    port = request.environ.get('SERVER_PORT', 5000)
    server_url = f"http://{server_ip}:{port}"
    
    # Renderizar la página con los datos actuales
    return render_template_string(HTML_TEMPLATE, 
                                 list_p=list_p,
                                 list_d=list_d,
                                 list_c=list_c,
                                 list_l=list_l,
                                 server_url=server_url)

def generate_pdf(dia, comida, lugar, asistentes):
    """Genera un PDF elegante con la información de la cita"""
    filename = "cita_generada.pdf"
    
    pdf = ElegantPDF()
    pdf.add_page()
    pdf.add_gradient_background()
    
    # Título principal
    pdf.set_font('Arial', 'B', 24)
    pdf.set_text_color(102, 126, 234)
    pdf.cell(0, 20, "TU CITA HA SIDO GENERADA", 0, 1, 'C')
    pdf.ln(5)
    
    # Fecha y hora de generación
    pdf.set_font('Arial', 'I', 10)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 10, f"Generado el: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", 0, 1, 'C')
    pdf.ln(15)
    
    # Información de la cita en tarjetas (sin emojis)
    pdf.add_info_card("DIA:", dia)
    pdf.add_info_card("LUGAR:", lugar)
    pdf.add_info_card("COMIDA:", comida)
    
    # Lista de asistentes
    pdf.add_attendants_list(asistentes)
    
    # Separador decorativo
    pdf.set_draw_color(102, 126, 234)
    pdf.set_line_width(0.5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(10)
    
    # Mensaje final (sin emojis)
    pdf.set_font('Arial', 'I', 12)
    pdf.set_text_color(102, 126, 234)
    pdf.multi_cell(0, 10, "¡Disfruta de este encuentro especial! Que sea memorable y lleno de buenos momentos.", 0, 'C')
    
    # Pie de página informativo
    pdf.ln(15)
    pdf.set_font('Arial', '', 9)
    pdf.set_text_color(100, 100, 100)
    pdf.multi_cell(0, 6, "Generado automaticamente por XONIDU - Generador de Citas\n"
                        "Organiza tus encuentros sociales de forma facil y divertida", 0, 'C')
    
    # Generar el PDF
    pdf.output(filename)
    return filename

def display_terminal_info():
    """Muestra información en la terminal al iniciar"""
    server_ip = get_server_ip()
    port = 5000  # Puerto por defecto de Flask
    server_url = f"http://{server_ip}:{port}"
    
    print("\n" + "="*60)
    print("🎉 GENERADOR DE CITAS XONIDU")
    print("="*60)
    print("Organiza tus encuentros sociales de forma fácil y divertida")
    print("="*60)
    print(f"\n🌐 URL Local:  http://127.0.0.1:{port}/")
    print(f"🌐 URL Red:    {server_url}/")
    print("\n📱 Código QR para acceso rápido desde tu teléfono:")
    print("="*60)
    
    # Generar y mostrar QR en terminal
    qr_ascii = generate_terminal_qr(server_url)
    if qr_ascii:
        print(qr_ascii)
        print("Escanea este código QR con la cámara de tu teléfono")
    else:
        print("(Ejecuta 'pip install qrcode' para ver el código QR)")
    
    print("="*60)
    print("\n💡 Características:")
    print("  • ✅ Añade asistentes por nombre")
    print("  • 📅 Elimina días no disponibles")
    print("  • 🍕 Sugiere comidas")
    print("  • 🏙️ Propone lugares")
    print("  • 🎯 Genera citas aleatorias")
    print("  • 📄 Crea PDFs elegantes")
    print("="*60)
    print("\nPresiona Ctrl+C para detener el servidor\n")

# Correr la aplicación
if __name__ == "__main__":
    display_terminal_info()
    app.run(host='0.0.0.0', port=5000, debug=True)
