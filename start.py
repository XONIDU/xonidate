#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
XONIDATE 2026 - Lanzador Universal del Generador de Citas
Este script ejecuta xonidate.py y verifica/instala dependencias
Desarrollado por: Darian Alberto Camacho Salas
#Somos XONIDU
"""

import subprocess
import sys
import os
import platform
import shutil
import importlib.util
import time

# Colores para terminal
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    
    @staticmethod
    def supports_color():
        """Verifica si la terminal soporta colores"""
        if platform.system() == 'Windows':
            try:
                import ctypes
                kernel32 = ctypes.windll.kernel32
                return kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            except:
                return False
        return True

# Desactivar colores si no hay soporte
if not Colors.supports_color():
    for attr in dir(Colors):
        if not attr.startswith('_') and attr != 'supports_color':
            setattr(Colors, attr, '')

def get_system():
    """Detecta el sistema operativo"""
    return platform.system().lower()

def get_linux_distro():
    """Detecta la distribución de Linux"""
    if get_system() != 'linux':
        return None
    
    try:
        if os.path.exists('/etc/os-release'):
            with open('/etc/os-release', 'r') as f:
                content = f.read().lower()
                if 'ubuntu' in content:
                    return 'ubuntu'
                elif 'debian' in content:
                    return 'debian'
                elif 'fedora' in content:
                    return 'fedora'
                elif 'centos' in content:
                    return 'centos'
                elif 'arch' in content:
                    return 'arch'
                elif 'manjaro' in content:
                    return 'manjaro'
                elif 'mint' in content:
                    return 'mint'
        return 'linux-generico'
    except:
        return 'linux-generico'

def get_python_command():
    """Obtiene el comando Python correcto"""
    if get_system() == 'windows':
        return ['python']
    else:
        try:
            subprocess.run(['python3', '--version'], capture_output=True, check=True)
            return ['python3']
        except:
            return ['python']

def print_banner():
    """Muestra el banner de XONIDATE"""
    sistema = get_system()
    distro = get_linux_distro()
    
    sistema_texto = {
        'windows': 'WINDOWS',
        'linux': f'LINUX ({distro.upper()})' if distro else 'LINUX',
        'darwin': 'MACOS'
    }.get(sistema, 'DESCONOCIDO')
    
    banner = f"""
{Colors.BLUE}{Colors.BOLD}═══════════════════════════════════════════════════════════
                    XONIDATE 2026 v2.0                    
              Generador Automático de Citas            
              Crea encuentros únicos con un clic           
                                                          
              Sistema detectado: {sistema_texto}            
                                                          
              Desarrollado por: Darian Alberto            
              Camacho Salas                               
              #Somos XONIDU
═══════════════════════════════════════════════════════════{Colors.END}
    """
    print(banner)

def check_python():
    """Verifica Python instalado"""
    try:
        cmd = get_python_command() + ['--version']
        subprocess.run(cmd, capture_output=True, check=True)
        return True
    except:
        return False

def check_command(comando):
    """Verifica si un comando existe"""
    return shutil.which(comando) is not None

def check_python_module(module_name):
    """Verifica si un módulo de Python está instalado"""
    return importlib.util.find_spec(module_name) is not None

def check_dependencies():
    """Verifica las dependencias de Python necesarias para XONIDATE"""
    print(f"\n{Colors.BOLD}Verificando dependencias de Python...{Colors.END}")
    
    dependencias = [
        ('flask', 'flask', 'Framework web', 'flask'),
        ('fpdf', 'fpdf', 'Generación de PDF', 'fpdf'),
        ('qrcode', 'qrcode', 'Códigos QR', 'qrcode'),
        ('pillow', 'pillow', 'Procesamiento de imágenes', 'PIL'),  # PIL es el nombre de importación de pillow
    ]
    
    faltantes = []
    
    for modulo, paquete, desc, import_name in dependencias:
        if check_python_module(import_name):
            print(f"{Colors.GREEN}  - {modulo}: OK{Colors.END}")
        else:
            print(f"{Colors.YELLOW}  - {modulo}: FALTANTE{Colors.END}")
            faltantes.append(paquete)
    
    return faltantes

def install_dependencies(faltantes):
    """Instala las dependencias faltantes"""
    if not faltantes:
        return True
    
    print(f"\n{Colors.BOLD}Instalando dependencias faltantes...{Colors.END}")
    
    sistema = get_system()
    distro = get_linux_distro()
    
    # Instalar paquetes Python
    if faltantes:
        print(f"Paquetes Python a instalar: {', '.join(faltantes)}")
        
        # Construir comando de instalación
        cmd = [sys.executable, '-m', 'pip', 'install']
        
        # Agregar opciones según sistema
        if sistema == 'linux':
            if distro in ['arch', 'manjaro', 'fedora']:
                cmd.append('--break-system-packages')
                print(f"{Colors.YELLOW}Usando --break-system-packages para {distro}{Colors.END}")
            else:
                cmd.append('--user')
        elif sistema == 'darwin':
            cmd.append('--user')
        
        cmd.extend(faltantes)
        
        # Intentar instalación
        try:
            print(f"Ejecutando: {' '.join(cmd)}")
            subprocess.run(cmd, check=True)
            print(f"{Colors.GREEN}Dependencias instaladas correctamente{Colors.END}")
        except subprocess.CalledProcessError as e:
            print(f"{Colors.RED}Error instalando dependencias: {e}{Colors.END}")
            print(f"\n{Colors.YELLOW}Intentando método alternativo...{Colors.END}")
            
            # Segundo intento: solo --user (para cualquier sistema)
            try:
                cmd2 = [sys.executable, '-m', 'pip', 'install', '--user'] + faltantes
                subprocess.run(cmd2, check=True)
                print(f"{Colors.GREEN}Instaladas con --user{Colors.END}")
            except:
                print(f"{Colors.RED}Fallo la instalación{Colors.END}")
                print(f"\nInstala manualmente:")
                print(f"  pip install {' '.join(faltantes)}")
                if sistema == 'linux':
                    print(f"\nO con --break-system-packages si usas Linux reciente:")
                    print(f"  pip install {' '.join(faltantes)} --break-system-packages")
                return False
    
    return True

def verificar_importaciones():
    """Verifica que todas las importaciones necesarias funcionen"""
    print(f"\n{Colors.BOLD}Verificando importaciones...{Colors.END}")
    
    modulos = [
        ('flask', 'flask'),
        ('fpdf', 'fpdf'),
        ('qrcode', 'qrcode'),
        ('PIL', 'pillow'),
    ]
    
    todos_ok = True
    for modulo, nombre in modulos:
        try:
            __import__(modulo)
            print(f"{Colors.GREEN}  - {nombre}: OK{Colors.END}")
        except ImportError:
            print(f"{Colors.RED}  - {nombre}: FALLO{Colors.END}")
            todos_ok = False
    
    return todos_ok

def crear_accesos_directos():
    """Crea accesos directos para cada sistema"""
    sistema = get_system()
    
    if sistema == 'windows':
        # Crear .bat para Windows
        with open('INICIAR_XONIDATE.bat', 'w') as f:
            f.write("""@echo off
title XONIDATE 2026 - Generador de Citas
color 1F
echo ========================================
echo      XONIDATE 2026 - Generador de Citas
echo      Desarrollado por Darian Alberto
echo ========================================
echo.
python start.py
pause
""")
        print(f"{Colors.GREEN}Creado INICIAR_XONIDATE.bat - Haz doble clic para ejecutar{Colors.END}")
    
    elif sistema == 'linux':
        # Crear .sh para Linux
        with open('INICIAR_XONIDATE.sh', 'w') as f:
            f.write("""#!/bin/bash
echo "========================================"
echo "      XONIDATE 2026 - Generador de Citas"
echo "      Desarrollado por Darian Alberto"
echo "========================================"
echo ""
python3 start.py
read -p "Presiona Enter para salir"
""")
        os.chmod('INICIAR_XONIDATE.sh', 0o755)
        print(f"{Colors.GREEN}Creado INICIAR_XONIDATE.sh - Ejecuta con: ./INICIAR_XONIDATE.sh{Colors.END}")
    
    elif sistema == 'darwin':
        # Crear .command para Mac
        with open('INICIAR_XONIDATE.command', 'w') as f:
            f.write("""#!/bin/bash
cd "$(dirname "$0")"
echo "========================================"
echo "      XONIDATE 2026 - Generador de Citas"
echo "      Desarrollado por Darian Alberto"
echo "========================================"
echo ""
python3 start.py
""")
        os.chmod('INICIAR_XONIDATE.command', 0o755)
        print(f"{Colors.GREEN}Creado INICIAR_XONIDATE.command - Haz doble clic para ejecutar{Colors.END}")

def main():
    """Función principal"""
    # Limpiar pantalla
    if get_system() == 'windows':
        os.system('cls')
    else:
        os.system('clear')
    
    # Mostrar banner
    print_banner()
    
    # Verificar Python
    if not check_python():
        print(f"\n{Colors.RED}Error: Python no está instalado{Colors.END}")
        print("Instala Python desde: https://www.python.org/downloads/")
        input(f"\n{Colors.YELLOW}Presiona Enter para salir...{Colors.END}")
        return
    
    python_version = subprocess.run(get_python_command() + ['--version'], 
                                   capture_output=True, text=True).stdout.strip()
    print(f"{Colors.BOLD}Python:{Colors.END} {python_version}")
    print(f"{Colors.BOLD}Directorio:{Colors.END} {os.path.dirname(os.path.abspath(__file__))}")
    
    # Verificar dependencias
    faltantes = check_dependencies()
    
    if faltantes:
        print(f"\n{Colors.YELLOW}Faltan dependencias{Colors.END}")
        respuesta = input("¿Instalar automáticamente? (s/n): ")
        
        if respuesta.lower() == 's':
            exito = install_dependencies(faltantes)
            if not exito:
                print(f"\n{Colors.RED}No se pudieron instalar las dependencias. Saliendo.{Colors.END}")
                input(f"\n{Colors.YELLOW}Presiona Enter para salir...{Colors.END}")
                return
        else:
            print(f"\nPuedes instalarlas manualmente con:")
            print("  pip install flask fpdf qrcode pillow")
            if get_system() == 'linux':
                print("\nSi usas Linux con Python 3.11+ y tienes el error 'externally-managed-environment':")
                print("  pip install flask fpdf qrcode pillow --break-system-packages")
            input(f"\n{Colors.YELLOW}Presiona Enter para salir...{Colors.END}")
            return
    
    # Verificar que existe xonidate.py
    if not os.path.exists('xonidate.py'):
        print(f"\n{Colors.RED}Error: No se encuentra xonidate.py{Colors.END}")
        print("Asegúrate de que xonidate.py está en el mismo directorio")
        print("\nPuedes descargarlo desde:")
        print("  https://github.com/XONIDU/xonidate")
        input(f"\n{Colors.YELLOW}Presiona Enter para salir...{Colors.END}")
        return
    
    # Verificar que las importaciones funcionan
    print(f"\n{Colors.BOLD}Verificando que todo funcione...{Colors.END}")
    if not verificar_importaciones():
        print(f"\n{Colors.RED}Error: No se pueden importar los módulos necesarios{Colors.END}")
        print("El programa no puede continuar sin estas dependencias")
        input(f"\n{Colors.YELLOW}Presiona Enter para salir...{Colors.END}")
        return
    
    print(f"\n{Colors.BOLD}Iniciando XONIDATE...{Colors.END}")
    print(f"{Colors.BOLD}Para salir en cualquier momento:{Colors.END} Ctrl+C")
    print("-" * 60)
    
    # EJECUTAR xonidate.py
    try:
        python_cmd = get_python_command()
        cmd = python_cmd + ['xonidate.py']
        print(f"Ejecutando: {' '.join(cmd)}")
        print("-" * 60)
        
        # Ejecutar xonidate.py
        resultado = subprocess.run(cmd)
        
        if resultado.returncode != 0:
            print(f"\n{Colors.RED}Error: xonidate.py terminó con código {resultado.returncode}{Colors.END}")
            
    except FileNotFoundError:
        print(f"\n{Colors.RED}Error: No se encuentra xonidate.py{Colors.END}")
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Programa detenido por el usuario{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}Error ejecutando xonidate.py: {e}{Colors.END}")
    
    print(f"\n{Colors.BLUE}Gracias por usar XONIDATE 2026{Colors.END}")
    print(f"{Colors.BLUE}Desarrollado por Darian Alberto Camacho Salas{Colors.END}")
    print(f"{Colors.BLUE}#Somos XONIDU{Colors.END}")
    
    # Pausa al final (excepto en Windows que ya tiene pausa por el .bat)
    if get_system() != 'windows':
        input(f"\n{Colors.YELLOW}Presiona Enter para salir...{Colors.END}")

if __name__ == '__main__':
    try:
        # Crear accesos directos
        crear_accesos_directos()
        
        # Ejecutar programa principal
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Saliendo...{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}Error inesperado: {e}{Colors.END}")
        input(f"\n{Colors.YELLOW}Presiona Enter para salir...{Colors.END}")
