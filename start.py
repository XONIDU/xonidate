from random import choice
from fpdf import FPDF

list_p = []
list_d = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
list_c = []
list_l = []

def names(persons):
    for i in range(1, persons + 1):
        person = input(f"Persona {i}: ")
        list_p.append(person)

def less():
    print("\nDias que no se puede: \n")
    for j in range(len(list_d)):
        print(list_d[j] + f" {j}")
    day = input("\nPresiona -enter- para aceptar: ")
    if day == "":
        return
    elif day.isdigit() and 0 <= int(day) < len(list_d):
        list_d.pop(int(day))
        less()
    else:
        print("Opcion invalida\n")
        less()

def food():
    comida = input("Ingrese un alimento (enter vacío para terminar): ")
    if comida == "":
        return
    else:
        list_c.append(comida)
        food()

def place():
    lugar = input("Ingrese un lugar (enter vacío para terminar): ")
    if lugar == "":
        return
    else:
        list_l.append(lugar)
        place()

def day_random():
    if not list_d:
        return None, None, None
    dia = choice(list_d)
    comida = choice(list_c) if list_c else "No definida"
    lugar = choice(list_l) if list_l else "No definido"
    return dia, comida, lugar

def generate_pdf(dia, comida, lugar):
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
    for person in list_p:
        pdf.cell(0, 10, f"- {person}", 0, 1)
    pdf.output("cita.pdf")
    print("\nPDF generado como 'cita.pdf' ✅")

names(2)
less()
food()
place()
dia, comida, lugar = day_random()
if dia:
    print(f"\nDía: {dia}\nComida: {comida}\nLugar: {lugar}\nAsistentes: {list_p}")
    generate_pdf(dia, comida, lugar)
else:
    print("No hay días disponibles para generar la cita.")

