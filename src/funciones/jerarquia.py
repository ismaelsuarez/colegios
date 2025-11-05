"""Gestión de estructura jerárquica de base de datos para colegios.

Este módulo implementa una organización jerárquica de los datos donde:
- colegios.csv es el archivo central/maestro
- Los datos se organizan en subcarpetas por diferentes criterios:
  - por_provincia/: Subcarpetas con archivos CSV agrupados por provincia
  - por_estudiantes/: Subcarpetas con archivos CSV agrupados por cantidad de estudiantes
  - por_año/: Subcarpetas con archivos CSV agrupados por año de creación

Esto permite una organización jerárquica de los datos cumpliendo con los requisitos
del proyecto de tener una estructura de base de datos separada jerárquicamente.
"""

import os
import csv
import shutil
from pathlib import Path
from typing import List, Dict


def obtener_ruta_subgrupos(ruta_db_central: str) -> Path:
    """Obtiene la ruta base para los subgrupos jerárquicos.

    Args:
        ruta_db_central (str): Ruta del archivo CSV central (ej: 'src/base_de_datos/colegios.csv').

    Returns:
        Path: Ruta base para los subgrupos (ej: 'src/base_de_datos/subgrupos').
    """
    db_dir = Path(ruta_db_central).parent
    return db_dir / "subgrupos"


def inicializar_estructura_jerarquica(ruta_db_central: str) -> None:
    """Inicializa la estructura jerárquica de carpetas para subgrupos.

    Crea las carpetas base para organizar datos por provincia, cantidad de estudiantes y año.

    Args:
        ruta_db_central (str): Ruta del archivo CSV central.
    """
    base_subgrupos = obtener_ruta_subgrupos(ruta_db_central)

    # Crear estructura de carpetas jerárquica
    carpetas = [
        base_subgrupos / "por_provincia",
        base_subgrupos / "por_estudiantes",
        base_subgrupos / "por_año",
    ]

    for carpeta in carpetas:
        carpeta.mkdir(parents=True, exist_ok=True)


def limpiar_nombre_archivo(nombre: str) -> str:
    """Limpia un nombre para usarlo como nombre de archivo.

    Elimina caracteres especiales y normaliza espacios.

    Args:
        nombre (str): Nombre a limpiar.

    Returns:
        str: Nombre limpio para archivo.
    """
    # Reemplazar caracteres problemáticos
    nombre = str(nombre).replace("/", "-").replace("\\", "-")
    nombre = nombre.replace(":", "-").replace("*", "-")
    nombre = nombre.replace("?", "-").replace('"', "-")
    nombre = nombre.replace("<", "-").replace(">", "-")
    nombre = nombre.replace("|", "-").strip()
    return nombre if nombre else "SinNombre"


def organizar_por_provincia(colegios: List[Dict], ruta_db_central: str) -> None:
    """Organiza los colegios en subcarpetas agrupados por provincia.

    Crea archivos CSV en subcarpetas por_provincia/ organizados por provincia.

    Args:
        colegios (list[dict]): Lista de colegios a organizar.
        ruta_db_central (str): Ruta del archivo CSV central.
    """
    base_subgrupos = obtener_ruta_subgrupos(ruta_db_central)
    carpeta_provincia = base_subgrupos / "por_provincia"

    # Agrupar colegios por provincia
    colegios_por_provincia = {}
    for colegio in colegios:
        provincia = colegio.get("Provincia", "Desconocida")
        if provincia not in colegios_por_provincia:
            colegios_por_provincia[provincia] = []
        colegios_por_provincia[provincia].append(colegio)

    # Crear archivo CSV para cada provincia
    for provincia, lista_colegios in colegios_por_provincia.items():
        nombre_archivo = limpiar_nombre_archivo(provincia) + ".csv"
        ruta_archivo = carpeta_provincia / nombre_archivo

        fieldnames = ["Provincia", "Colegio", "Cantidad de Estudiantes", "Año de Creación"]
        with open(ruta_archivo, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for c in lista_colegios:
                writer.writerow({
                    "Provincia": str(c["Provincia"]),
                    "Colegio": str(c["Colegio"]),
                    "Cantidad de Estudiantes": int(c["Cantidad de Estudiantes"]),
                    "Año de Creación": int(c["Año de Creación"]),
                })


def organizar_por_estudiantes(colegios: List[Dict], ruta_db_central: str) -> None:
    """Organiza los colegios en subcarpetas agrupados por cantidad de estudiantes.

    Crea archivos CSV en subcarpetas por_estudiantes/ organizados por rangos de estudiantes.

    Args:
        colegios (list[dict]): Lista de colegios a organizar.
        ruta_db_central (str): Ruta del archivo CSV central.
    """
    base_subgrupos = obtener_ruta_subgrupos(ruta_db_central)
    carpeta_estudiantes = base_subgrupos / "por_estudiantes"

    # Agrupar colegios por rango de estudiantes
    colegios_por_rango = {}
    for colegio in colegios:
        estudiantes = colegio.get("Cantidad de Estudiantes", 0)
        
        # Definir rangos
        if estudiantes < 300:
            rango = "Menos_300"
        elif estudiantes < 500:
            rango = "300_499"
        elif estudiantes < 700:
            rango = "500_699"
        else:
            rango = "700_o_mas"
        
        if rango not in colegios_por_rango:
            colegios_por_rango[rango] = []
        colegios_por_rango[rango].append(colegio)

    # Crear archivo CSV para cada rango
    for rango, lista_colegios in colegios_por_rango.items():
        nombre_archivo = limpiar_nombre_archivo(rango) + ".csv"
        ruta_archivo = carpeta_estudiantes / nombre_archivo

        fieldnames = ["Provincia", "Colegio", "Cantidad de Estudiantes", "Año de Creación"]
        with open(ruta_archivo, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for c in lista_colegios:
                writer.writerow({
                    "Provincia": str(c["Provincia"]),
                    "Colegio": str(c["Colegio"]),
                    "Cantidad de Estudiantes": int(c["Cantidad de Estudiantes"]),
                    "Año de Creación": int(c["Año de Creación"]),
                })


def organizar_por_año(colegios: List[Dict], ruta_db_central: str) -> None:
    """Organiza los colegios en subcarpetas agrupados por año de creación.

    Crea archivos CSV en subcarpetas por_año/ organizados por décadas.

    Args:
        colegios (list[dict]): Lista de colegios a organizar.
        ruta_db_central (str): Ruta del archivo CSV central.
    """
    base_subgrupos = obtener_ruta_subgrupos(ruta_db_central)
    carpeta_año = base_subgrupos / "por_año"

    # Agrupar colegios por década
    colegios_por_decada = {}
    for colegio in colegios:
        año = colegio.get("Año de Creación", 0)
        
        # Definir décadas
        if año < 1970:
            decada = "Antes_1970"
        elif año < 1980:
            decada = "1970_1979"
        elif año < 1990:
            decada = "1980_1989"
        elif año < 2000:
            decada = "1990_1999"
        else:
            decada = "2000_o_despues"
        
        if decada not in colegios_por_decada:
            colegios_por_decada[decada] = []
        colegios_por_decada[decada].append(colegio)

    # Crear archivo CSV para cada década
    for decada, lista_colegios in colegios_por_decada.items():
        nombre_archivo = limpiar_nombre_archivo(decada) + ".csv"
        ruta_archivo = carpeta_año / nombre_archivo

        fieldnames = ["Provincia", "Colegio", "Cantidad de Estudiantes", "Año de Creación"]
        with open(ruta_archivo, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for c in lista_colegios:
                writer.writerow({
                    "Provincia": str(c["Provincia"]),
                    "Colegio": str(c["Colegio"]),
                    "Cantidad de Estudiantes": int(c["Cantidad de Estudiantes"]),
                    "Año de Creación": int(c["Año de Creación"]),
                })


def sincronizar_estructura_jerarquica(colegios: List[Dict], ruta_db_central: str) -> None:
    """Sincroniza la estructura jerárquica completa con los datos actuales.

    Esta función:
    1. Inicializa la estructura de carpetas si no existe
    2. Organiza los datos en subcarpetas por provincia, estudiantes y año
    3. Mantiene la sincronización entre el archivo central y los subgrupos

    Args:
        colegios (list[dict]): Lista completa de colegios desde el archivo central.
        ruta_db_central (str): Ruta del archivo CSV central.
    """
    # Inicializar estructura si no existe
    inicializar_estructura_jerarquica(ruta_db_central)

    # Organizar datos en subgrupos jerárquicos
    organizar_por_provincia(colegios, ruta_db_central)
    organizar_por_estudiantes(colegios, ruta_db_central)
    organizar_por_año(colegios, ruta_db_central)


def leer_desde_subgrupo(ruta_subgrupo: str) -> List[Dict]:
    """Lee colegios desde un archivo CSV de un subgrupo jerárquico.

    Args:
        ruta_subgrupo (str): Ruta al archivo CSV del subgrupo.

    Returns:
        list[dict]: Lista de colegios leídos del subgrupo.
    """
    colegios = []
    if not os.path.exists(ruta_subgrupo):
        return colegios

    try:
        with open(ruta_subgrupo, "r", encoding="utf-8-sig", newline="") as f:
            lector = csv.DictReader(f)
            for fila in lector:
                provincia = fila.get("Provincia", "").strip()
                colegio = fila.get("Colegio", "").strip()
                cantidad_str = fila.get("Cantidad de Estudiantes", "").strip()
                año_str = fila.get("Año de Creación", "").strip()

                if not provincia or not colegio:
                    continue

                try:
                    cantidad_estudiantes = int(cantidad_str) if cantidad_str else 0
                    año_creacion = int(año_str) if año_str else 0
                except ValueError:
                    continue

                colegios.append({
                    "Provincia": provincia,
                    "Colegio": colegio,
                    "Cantidad de Estudiantes": cantidad_estudiantes,
                    "Año de Creación": año_creacion,
                })
    except Exception:
        pass

    return colegios


def obtener_info_estructura_jerarquica(ruta_db_central: str) -> Dict:
    """Obtiene información sobre la estructura jerárquica actual.

    Args:
        ruta_db_central (str): Ruta del archivo CSV central.

    Returns:
        dict: Diccionario con información sobre la estructura jerárquica.
    """
    base_subgrupos = obtener_ruta_subgrupos(ruta_db_central)

    info = {
        "ruta_base": str(base_subgrupos),
        "por_provincia": {},
        "por_estudiantes": {},
        "por_año": {},
    }

    # Contar archivos en cada subcarpeta
    for tipo in ["por_provincia", "por_estudiantes", "por_año"]:
        carpeta = base_subgrupos / tipo
        if carpeta.exists():
            archivos = list(carpeta.glob("*.csv"))
            info[tipo] = {
                "cantidad_archivos": len(archivos),
                "archivos": [arch.name for arch in archivos],
            }
        else:
            info[tipo] = {
                "cantidad_archivos": 0,
                "archivos": [],
            }

    return info

