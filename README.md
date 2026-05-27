# 🎉 XONIDATE

Generador automático de citas por web con estilo terminal  
Optimizado para organizar encuentros sociales de forma fácil y divertida  
Desarrollado por Darian Alberto Camacho Salas – XONIDU

## 📋 Características

- ✅ Interfaz tipo terminal (colores verde, azul, rojo, blanco)
- ✅ Añade/elimina asistentes, días, comidas y lugares
- ✅ Eliminación individual con ✕ o por menús desplegables
- ✅ Botón "Limpiar Todo" para reiniciar
- ✅ Generación aleatoria de citas (un día, una comida, un lugar)
- ✅ Descarga de PDF elegante (sin guardar en servidor)
- ✅ QR de acceso para usar desde el móvil
- ✅ Multiplataforma (Windows, macOS, Linux)
- ✅ Sin bases de datos – todo en memoria

## 📦 Instalación

### Opción 1 – Clonado manual

```bash
git clone https://github.com/XONIDU/xonidate.git
cd xonidate
pip install -r requirements.txt   # o pip install flask fpdf qrcode pillow
python start.py
```

### Opción 2 – Comando `xoninstall` (recomendado para futuras herramientas XONI)

Agrega la siguiente función a tu `~/.bashrc` con un solo comando:

```bash
echo 'xoninstall() { if [ -z "$1" ]; then echo "Uso: xoninstall <repo>"; echo "Ej: xoninstall xoniran"; else git clone "https://github.com/XONIDU/$1.git"; fi; }' >> ~/.bashrc && source ~/.bashrc && echo "✅ Listo. Usa: xoninstall xonidate"
```

Luego simplemente escribe:

```bash
xoninstall xonidate
cd xonidate
pip install -r requisitos.txt
python start.py
```

> **Nota:** Esta función te servirá para instalar cualquier otra herramienta futura de XONIDU (por ejemplo `xoninstall xonidate`).

## 🔧 Configuración

No requiere configuración manual. El lanzador `start.py` se encarga de:
- Detectar tu sistema operativo.
- Verificar e instalar `pip` si falta (en Linux).
- Instalar las dependencias (`flask`, `fpdf`, `qrcode`, `pillow`) usando `--break-system-packages` cuando es necesario.
- Ejecutar la aplicación principal.

### Archivos generados

- El PDF se descarga directamente en tu navegador, no se guarda en el servidor.
- No se crean archivos de configuración locales (todo funciona en memoria).

## 🚀 Uso

```bash
python start.py   # o ./start.py en Linux/macOS si tiene permisos
```

Dentro de la interfaz web (abre automáticamente en http://127.0.0.1:5000):

1. **Añade asistentes**, comidas y lugares usando los campos de texto.
2. **Elimina** elementos con la ✕ roja o mediante los menús desplegables.
3. **Limpia todo** con el botón correspondiente.
4. Pulsa **`> GENERAR CITA Y DESCARGAR PDF`**.
5. Se descargará un PDF con los detalles de la cita (día, lugar, comida, lista de asistentes).

**Controles**:  
- `Ctrl + C` en la terminal para detener el servidor web.

### Ejemplo de pantalla

```
============================================================
   XONIDATE - GENERADOR DE CITAS CON ESTILO TERMINAL
============================================================
   Añade asistentes, comidas y lugares.  
   Elimina lo que no quieras.  
   ¡Genera tu cita y descarga el PDF!
============================================================

> ASISTENTES
   - Ana
   - Carlos
   - María

> DÍAS DISPONIBLES: Lunes, Martes, Miércoles...
> COMIDAS: Pizza, Sushi
> LUGARES: Parque, Cine

[ GENERAR CITA Y DESCARGAR PDF ]
```

## 📁 Estructura del paquete

| Archivo              | Ubicación                          |
|----------------------|------------------------------------|
| `xonidate.py`        | Programa principal (Flask)         |
| `start.py`           | Lanzador universal                 |
| `templates/index.html` | Interfaz de usuario (estilo terminal) |
| `requirements.txt`   | Dependencias (opcional)            |
| `README.md`          | Este archivo                       |

## 🧪 Pruebas

Ejecuta directamente el lanzador:

```bash
python start.py
```

Si todo funciona, verás un mensaje como:

```
✅ Servidor iniciado en http://127.0.0.1:5000
```

Abre esa URL en tu navegador.

## 🐛 Problemas comunes y soluciones

| Problema | Solución |
|----------|----------|
| `ModuleNotFoundError: No module named 'flask'` | Ejecuta `pip install flask fpdf qrcode pillow` (o usa `start.py` que lo instala automáticamente). |
| `error: externally-managed-environment` (Linux) | Usa `pip install --break-system-packages ...` o mejor ejecuta `python start.py` que lo maneja solo. |
| El puerto 5000 ya está ocupado | Cambia el puerto en `xonidate.py` (última línea) o mata el proceso: `sudo kill -9 $(sudo lsof -t -i:5000)`. |
| No se ve el código QR en la terminal | Instala `qrcode` (`pip install qrcode`). No es esencial para el funcionamiento. |
| El PDF no se descarga | Revisa que tu navegador permita descargas automáticas. El PDF se genera en memoria. |

## 📄 Licencia

© 2026 Darian Alberto Camacho Salas (XONIDU)  
Todos los derechos reservados. No se permite la copia, distribución o modificación sin autorización explícita.

## ✉️ Contacto

- **Creador**: Darian Alberto Camacho Salas  
- **Email**: [xonidu@gmail.com](mailto:xonidu@gmail.com)  
- **GitHub**: [@XONIDU](https://github.com/XONIDU)

---

