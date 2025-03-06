#installer.py
import subprocess
import os
import sys
from utils.logging.dependency_injection import get_logger
import winshell
from win32com.client import Dispatch

# Configuración del logger
logger = get_logger()

def crear_acceso_directo(ruta_archivo_bat, directorio_script):
    escritorio = winshell.desktop()
    ruta_acceso_directo = os.path.join(escritorio, "profebot.lnk")
    ruta_icono = os.path.join(directorio_script, "SCR","config", "logo.ico")

    if not os.path.isfile(ruta_icono):
        logger.error(f"El archivo de icono '{ruta_icono}' no existe.")
        return False

    try:
        shell = Dispatch('WScript.Shell')
        acceso_directo = shell.CreateShortCut(ruta_acceso_directo)
        acceso_directo.Targetpath = ruta_archivo_bat
        acceso_directo.WorkingDirectory = directorio_script
        acceso_directo.IconLocation = ruta_icono  
        acceso_directo.save()
        logger.info(f"Acceso directo {'actualizado' if os.path.isfile(ruta_acceso_directo) else 'creado'} exitosamente.")
        return True
    except Exception as e:
        logger.error(f"Error al crear/actualizar el acceso directo: {e}", exc_info=True)
        return False

def main():
    directorio_script = os.path.dirname(os.path.abspath(__file__))
    limpieza_pantalla()
    print("directorio_script: ",directorio_script,"\n")
    logger.info("Iniciando instalador")

    #instalar_dependencias(directorio_script)
    ruta_archivo_bat = os.path.join(directorio_script, 'profebot.bat')
    if not os.path.isfile(ruta_archivo_bat):
        logger.info(f"Creando archivo 'profebot.bat'")
        crear_archivo_bat(directorio_script, sys.executable)
    
    crear_acceso_directo(ruta_archivo_bat, directorio_script)

def instalar_dependencias(directorio_script):
    ruta_requirements = os.path.join(directorio_script, 'requirements.txt')
    if os.path.isfile(ruta_requirements):
        with open(ruta_requirements) as file:
            for package in [line.strip() for line in file if line.strip() and not line.startswith('#')]:
                try:
                    subprocess.run([sys.executable, "-m", "pip", "install",

 package], capture_output=True, text=True, check=True)
                    logger.info(f"Instalado o actualizado: {package}")
                except subprocess.CalledProcessError as e:
                    logger.error(f"Error al instalar la dependencia {package}: {e.output}")
        logger.info("Verificación y actualización de dependencias completada.")
    else:
        logger.warning("Archivo 'requirements.txt' no encontrado. No se instalaron dependencias adicionales.")

def crear_archivo_bat(directorio_script, python_executable):
    ruta_main_py = os.path.join(directorio_script, 'SCR', 'main.py')
    ruta_archivo_bat = os.path.join(directorio_script, 'profebot.bat')

    contenido_bat = (
        "@echo off\n"
        "setlocal\n"
        "\n"
        "set \"SCRIPT_DIR=%~dp0\"\n"
        "\n"
        "cd /d \"%SCRIPT_DIR%\"\n"
        "\"{}\" \"{}\"\n".format(python_executable, ruta_main_py) +
        "pause\n"
        "endlocal\n"
    )

    with open(ruta_archivo_bat, 'w') as archivo_bat:
        archivo_bat.write(contenido_bat)
    logger.info("Archivo 'profebot.bat' creado exitosamente.")

def limpieza_pantalla():
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        logger.info("Pantalla limpiada.")
    except Exception as e:
        logger.error(f"Error al limpiar la pantalla: {e}")

if __name__ == "__main__":
    main()
