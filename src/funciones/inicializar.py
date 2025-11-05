"""Inicialización y verificación del archivo CSV de colegios.

Este módulo se encarga de ubicar, mover o crear el archivo `colegios.csv`
necesario para el modo local.
"""

import os
import shutil
import csv
from funciones.utilidades import limpiar_consola


def gestionar_db(directorio_base: str, ruta_objetivo: str) -> str | None:
    """Verifica, busca, mueve o crea el archivo `colegios.csv`.

    Args:
        directorio_base (str): Directorio raíz del proyecto.
        ruta_objetivo (str): Ruta donde debe estar el CSV.

    Returns:
        str | None: Ruta del archivo CSV, o None si hay error.
    """
    ruta_objetivo_norm = os.path.normpath(ruta_objetivo)

    # Si ya existe en la ubicación correcta
    if os.path.isfile(ruta_objetivo_norm):
        return ruta_objetivo_norm

    # Buscar en todo el proyecto
    archivo_encontrado = None
    for root, dirs, files in os.walk(directorio_base):
        # Evitar buscar en .git, __pycache__, etc.
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'venv', '.venv']]
        
        if 'colegios.csv' in files:
            candidato = os.path.join(root, 'colegios.csv')
            # Si está en la ubicación objetivo, ya lo retornamos arriba
            if os.path.normpath(candidato) == ruta_objetivo_norm:
                continue
            archivo_encontrado = candidato
            break

    # Si se encontró, moverlo
    if archivo_encontrado:
        try:
            directorio_destino = os.path.dirname(ruta_objetivo_norm)
            if not os.path.exists(directorio_destino):
                os.makedirs(directorio_destino, exist_ok=True)
            shutil.move(archivo_encontrado, ruta_objetivo_norm)
            print(f"✅ Archivo movido a: {ruta_objetivo_norm}")
            return ruta_objetivo_norm
        except Exception as e:
            print(f"⚠️ Error al mover el archivo: {e}")
            return None

    # Si no se encontró, crear uno nuevo
    try:
        directorio_destino = os.path.dirname(ruta_objetivo_norm)
        if not os.path.exists(directorio_destino):
            os.makedirs(directorio_destino, exist_ok=True)

        with open(ruta_objetivo_norm, 'w', encoding='utf-8-sig', newline='') as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(["Provincia", "Colegio", "Cantidad de Estudiantes", "Año de Creación"])

        print(f"✅ Archivo CSV creado en: {ruta_objetivo_norm}")
        return ruta_objetivo_norm
    except Exception as e:
        print(f"⚠️ Error al crear el archivo CSV: {e}")
        return None


def init_db(project_root: str) -> str | None:
    """Inicializa la base de datos de colegios.

    También inicializa la estructura jerárquica de subgrupos si existe el módulo.

    Args:
        project_root (str): Ruta raíz del proyecto.

    Returns:
        str | None: Ruta del archivo CSV o None si hay error.
    """
    ruta_db = os.path.join(project_root, 'src', 'base_de_datos', 'colegios.csv')
    db_path = gestionar_db(project_root, ruta_db)
    
    if db_path is None:
        return None

    # Inicializar estructura jerárquica si el archivo existe
    if db_path and os.path.exists(db_path):
        try:
            from funciones.jerarquia import inicializar_estructura_jerarquica, sincronizar_estructura_jerarquica
            from funciones.utilidades import leer_csv

            # Inicializar carpetas
            inicializar_estructura_jerarquica(db_path)

            # Sincronizar datos existentes
            colegios = leer_csv(db_path)
            if colegios:
                sincronizar_estructura_jerarquica(colegios, db_path)
                print("✅ Estructura jerárquica inicializada")
        except ImportError:
            # Si el módulo jerarquia no está disponible, continuar sin estructura jerárquica
            pass
        except Exception as e:
            # Si hay algún error, continuar sin estructura jerárquica
            print(f"⚠️  No se pudo inicializar estructura jerárquica: {e}")

    return db_path
