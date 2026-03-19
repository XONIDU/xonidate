# 🚀 XONIDATE · Generador Automático de Citas

<div align="center">
  <h3>⚡ Organiza encuentros sociales de forma fácil y divertida</h3>
  
  [✨ Características](#-características) • 
  [📦 Instalación](#-instalación) • 
  [🎮 Uso](#-uso) • 
  [🐧 Linux](#-notas-para-linux) • 
  [📞 Contacto](#-contacto)
</div>

---

## ⚠️ Aviso importante

> **Este código es exclusivamente para fines educativos.**  
> No nos hacemos responsables del mal uso que se pueda dar a esta herramienta.

---

## ✨ Características

| Función               | Descripción                                           |
|-----------------------|-------------------------------------------------------|
| **👥 Asistentes**      | Añade o elimina participantes fácilmente.            |
| **📅 Días**            | Gestiona los días disponibles para la cita.          |
| **🍴 Comidas**         | Propone opciones gastronómicas.                       |
| **📍 Lugares**         | Define posibles ubicaciones.                          |
| **🎲 Generación**      | Combina aleatoriamente los elementos y crea una cita. |
| **📄 PDF elegante**    | Descarga un documento profesional con los resultados. |
| **🌐 Multi‑plataforma**| Funciona en Windows, macOS y Linux.                   |
| **🖥️ Interfaz terminal**| Diseño inspirado en consola con colores verde, azul, rojo y blanco. |

---

## 📦 Instalación

### Requisitos previos
- Python 3.8 o superior
- `pip` (gestor de paquetes)

### Pasos rápidos

1. **Clona el repositorio**
   ```bash
   git clone https://github.com/XONIDU/xonidate.git
   cd xonidate
   ```

2. **(Recomendado) Crea un entorno virtual**
   ```bash
   python -m venv venv
   # Activar:
   #   Linux/macOS: source venv/bin/activate
   #   Windows:     venv\Scripts\activate
   ```

3. **Ejecuta el lanzador** (se encarga de instalar dependencias y arrancar la app)
   ```bash
   python start.py
   ```
   > El script `start.py` detectará tu sistema operativo, instalará automáticamente `flask`, `fpdf`, `qrcode` y `pillow` (usando `--break-system-packages` en distribuciones Linux que lo requieran) y luego lanzará `xonidate.py`.

4. **Accede a la aplicación**
   - Local: http://127.0.0.1:5000
   - Desde tu red: http://[IP-del-equipo]:5000

### Instalación manual (alternativa)
Si prefieres hacerlo manualmente:
```bash
pip install flask fpdf qrcode pillow
python xonidate.py
```

---

## 🎮 Uso

1. **Añade elementos** en cada sección (asistentes, comidas, lugares…).  
2. **Elimina** cualquier elemento haciendo clic en la **✕** roja junto a él, o usando los menús desplegables.  
3. **Limpia todo** con el botón `[ LIMPIAR TODO ]`.  
4. Cuando estés listo, pulsa **`> GENERAR CITA Y DESCARGAR PDF`**.  
5. ¡Disfruta de tu cita única!

---

## 🐧 Notas para Linux

En distribuciones como **Debian 12, Ubuntu 23.04+, Fedora, Arch o Manjaro**, puede aparecer el error:

```
error: externally-managed-environment
```

El lanzador `start.py` lo maneja automáticamente:  
- Si tu distro lo requiere, usará `--break-system-packages` durante la instalación de dependencias.  
- Si prefieres hacerlo a mano, ejecuta:

```bash
pip install flask fpdf qrcode pillow --break-system-packages
```

**Siempre es preferible usar un entorno virtual** para evitar conflictos con los paquetes del sistema.

---

## 📁 Estructura del proyecto

```
xonidate/
├── start.py              # Lanzador universal (instala dependencias y ejecuta la app)
├── xonidate.py           # Aplicación principal Flask
├── requirements.txt      # Lista de dependencias (opcional)
├── README.md             # Este archivo
└── templates/
    └── index.html        # Interfaz de usuario con estilo terminal
```

---

## 📞 Contacto

| Medio     | Enlace                              |
|-----------|-------------------------------------|
| 📸 Instagram | [@xonidu](https://instagram.com/xonidu) |
| 📘 Facebook  | [xonidu](https://facebook.com/xonidu)   |
| 📧 Email     | [xonidu@gmail.com](mailto:xonidu@gmail.com) |

**Creador**: Darian Alberto Camacho Salas  
**#SomosXONIDU**

---

<div align="center">
  ⭐ **Si te gusta el proyecto, no olvides dejar una estrella en GitHub** ⭐  
  <br>  
  **XONIDATE © 2026 · Hecho con 💚 desde la terminal**
</div>
```
