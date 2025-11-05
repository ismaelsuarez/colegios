"""Utilidades generales para gestión de colegios.

Este módulo proporciona funciones para:
- Leer y escribir archivos CSV
- Normalizar texto (quitar acentos, espacios)
- Mostrar menús
- Validaciones básicas
"""

import csv
import os
import unicodedata
from typing import List, Dict, Optional


def normalizar(texto: str) -> str:
    """Convierte texto a minúsculas, elimina espacios y acentos.

    Args:
        texto (str): Texto a normalizar.

    Returns:
        str: Texto normalizado.
    """
    if not texto:
        return ""
    texto = str(texto).lower().strip()
    texto = unicodedata.normalize('NFD', texto)
    texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
    return texto


def leer_csv(ruta_csv: str) -> List[Dict]:
    """Lee colegios desde un archivo CSV y retorna lista de diccionarios.

    Usa los nombres reales del CSV: Provincia, Colegio, Cantidad de Estudiantes, Año de Creación.

    Args:
        ruta_csv (str): Ruta al archivo CSV.

    Returns:
        list[dict]: Lista de diccionarios con los colegios. Cada diccionario tiene:
            - 'Provincia' (str)
            - 'Colegio' (str)
            - 'Cantidad de Estudiantes' (int)
            - 'Año de Creación' (int)
    """
    colegios = []
    filas_invalidas = 0

    if not os.path.exists(ruta_csv):
        return colegios

    try:
        with open(ruta_csv, 'r', encoding='utf-8-sig', newline='') as archivo:
            lector = csv.DictReader(archivo)

            for fila in lector:
                try:
                    provincia = fila.get("Provincia", "").strip()
                    colegio = fila.get("Colegio", "").strip()
                    cantidad_str = fila.get("Cantidad de Estudiantes", "").strip()
                    año_str = fila.get("Año de Creación", "").strip()

                    if not provincia or not colegio:
                        filas_invalidas += 1
                        continue

                    # Convertir campos numéricos
                    try:
                        cantidad_estudiantes = int(cantidad_str) if cantidad_str else 0
                        año_creacion = int(año_str) if año_str else 0
                    except ValueError:
                        filas_invalidas += 1
                        continue

                    colegio_dict = {
                        "Provincia": provincia,
                        "Colegio": colegio,
                        "Cantidad de Estudiantes": cantidad_estudiantes,
                        "Año de Creación": año_creacion
                    }

                    colegios.append(colegio_dict)

                except Exception:
                    filas_invalidas += 1
                    continue

        if filas_invalidas > 0:
            print(f"⚠️ Se omitieron {filas_invalidas} fila(s) con formato incorrecto.")

    except Exception as e:
        print(f"⚠️ Error al leer el archivo CSV: {e}")
        return []

    return colegios


def escribir_csv(ruta_csv: str, colegios: List[Dict]) -> bool:
    """Escribe la lista de colegios a un archivo CSV.

    Además, sincroniza la estructura jerárquica de subgrupos organizando
    los datos en subcarpetas por provincia, cantidad de estudiantes y año.

    Args:
        ruta_csv (str): Ruta donde guardar el CSV.
        colegios (list[dict]): Lista de diccionarios con los colegios.

    Returns:
        bool: True si se escribió correctamente, False en caso contrario.
    """
    campos = ["Provincia", "Colegio", "Cantidad de Estudiantes", "Año de Creación"]

    try:
        # Asegurar que el directorio existe
        directorio = os.path.dirname(ruta_csv)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio, exist_ok=True)

        with open(ruta_csv, 'w', encoding='utf-8-sig', newline='') as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=campos)
            escritor.writeheader()
            escritor.writerows(colegios)

        # Sincronizar estructura jerárquica después de escribir el archivo central
        try:
            from funciones.jerarquia import sincronizar_estructura_jerarquica
            sincronizar_estructura_jerarquica(colegios, ruta_csv)
        except ImportError:
            # Si el módulo jerarquia no está disponible, continuar sin sincronización
            pass

        return True

    except Exception as e:
        print(f"⚠️ Error al escribir el archivo CSV: {e}")
        return False


def limpiar_consola():
    """Limpia la consola."""
    os.system('cls' if os.name == 'nt' else 'clear')


def menu_principal() -> int:
    """Muestra el menú principal de operaciones y devuelve la opción elegida.

    Returns:
        int: Número de opción (1 a 11).
    """
    print("")

    print("-----MENÚ PRINCIPAL - GESTIÓN DE COLEGIOS-----")
    print("CONSULTAS Y BÚSQUEDAS: ")
    print("1.  Buscar colegio por nombre")
    print("2.  Listar colegios por provincia")
    print("3.  Filtrar por cantidad de estudiantes")
    print("4.  Filtrar por año de fundación")
    print("ORGANIZACIÓN Y ANÁLISIS:")
    print("5.  Ordenar lista de colegios")
    print("6.  Ver estadísticas generales")
    print("ADMINISTRACIÓN DE DATOS:")
    print("7. Registrar nuevo colegio")
    print("8. Modificar datos de colegio")
    print("9. Eliminar colegio del sistema")
    print("CONFIGURACIÓN:")
    print("10. Cambiar fuente de datos (Local/API)")
    print("11. Salir del programa")

    try:
        opcion = int(input("\n👉 Seleccione una opción (1-11): "))
        return opcion
    except ValueError:
        print("⚠️ Entrada inválida. Por favor ingresá un número.")
        return -1


def seleccionar_modo() -> int:
    """Muestra el menú de selección de modo y retorna la opción.

    Returns:
        int: 1 para local, 2 para API, 3 para salir.
    """
    print("")
    print("╔══════════════════════════════════════════════════════════╗")
    print("║          SELECCIÓN DE FUENTE DE DATOS                    ║")
    print("╠══════════════════════════════════════════════════════════╣")
    print("║  1. 💾 Archivo CSV local                                 ║")
    print("║     └─ Trabaja con datos almacenados en este equipo      ║")
    print("║                                                           ║")
    print("║  2. 🌐 Servidor API remoto                               ║")
    print("║     └─ Conecta con servidor en http://149.50.150.15:8020 ║")
    print("║                                                           ║")
    print("║  3. ❌ Cancelar y salir                                  ║")
    print("╚══════════════════════════════════════════════════════════╝")

    try:
        op = int(input("\n👉 Elija una opción (1, 2 o 3): "))
        return op
    except ValueError:
        print("⚠️ Entrada inválida.")
        return 0


def pedir_rango(nombre_campo: str) -> tuple[Optional[int], Optional[int]]:
    """Pide al usuario un rango de valores (mínimo y máximo).

    Args:
        nombre_campo (str): Nombre del campo para el mensaje.

    Returns:
        tuple[int | None, int | None]: Tupla (mínimo, máximo) o (None, None) si hay error.
    """
    try:
        minimo = int(input(f"Ingresá {nombre_campo} mínimo: "))
        maximo = int(input(f"Ingresá {nombre_campo} máximo: "))

        if minimo > maximo:
            print("⚠️ El mínimo no puede ser mayor que el máximo.")
            return None, None

        return minimo, maximo
    except ValueError:
        print("⚠️ Entrada inválida. Debés ingresar números.")
        return None, None
