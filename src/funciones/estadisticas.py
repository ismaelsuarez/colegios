"""Cálculo e impresión de estadísticas sobre una lista de colegios."""

from typing import List, Dict
from funciones.utilidades import normalizar


def contar_colegios_por_provincia_recursivo(colegios: List[Dict], indice: int = 0, conteo: Dict[str, int] = None) -> Dict[str, int]:
    """Cuenta colegios por provincia de forma recursiva.

    Implementación recursiva para cumplir con los requisitos del proyecto.

    Args:
        colegios (list[dict]): Lista de colegios.
        indice (int): Índice actual en la lista (para recursión).
        conteo (dict): Diccionario acumulativo de conteos.

    Returns:
        dict: Diccionario con provincias como claves y cantidad de colegios como valores.
    """
    if conteo is None:
        conteo = {}

    # Caso base: se recorrió toda la lista
    if indice >= len(colegios):
        return conteo

    # Procesar el elemento actual
    colegio_actual = colegios[indice]
    provincia = colegio_actual.get("Provincia", "Desconocida")
    conteo[provincia] = conteo.get(provincia, 0) + 1

    # Llamada recursiva para el siguiente elemento
    return contar_colegios_por_provincia_recursivo(colegios, indice + 1, conteo)


def sumar_estudiantes_recursivo(colegios: List[Dict], indice: int = 0) -> int:
    """Suma la cantidad de estudiantes de forma recursiva.

    Implementación recursiva para cumplir con los requisitos del proyecto.

    Args:
        colegios (list[dict]): Lista de colegios.
        indice (int): Índice actual en la lista (para recursión).

    Returns:
        int: Total de estudiantes.
    """
    # Caso base: se recorrió toda la lista
    if indice >= len(colegios):
        return 0

    # Procesar el elemento actual
    estudiantes_actual = colegios[indice].get("Cantidad de Estudiantes", 0)

    # Llamada recursiva para el siguiente elemento y sumar
    return estudiantes_actual + sumar_estudiantes_recursivo(colegios, indice + 1)


def mostrar_estadisticas(colegios: List[Dict]) -> None:
    """Imprime estadísticas generales de una lista de colegios.

    Args:
        colegios (list[dict]): Lista de colegios. Cada colegio debe contener:
            - 'Provincia' (str)
            - 'Colegio' (str)
            - 'Cantidad de Estudiantes' (int)
            - 'Año de Creación' (int)
    """
    if not colegios:
        print("\n⚠️ No hay datos disponibles para mostrar estadísticas.")
        return

    # Colegio más antiguo y más nuevo
    colegio_mas_antiguo = min(colegios, key=lambda x: x.get("Año de Creación", 9999))
    colegio_mas_nuevo = max(colegios, key=lambda x: x.get("Año de Creación", 0))

    # Promedio de año de creación
    años = [c.get("Año de Creación", 0) for c in colegios if c.get("Año de Creación", 0) > 0]
    promedio_año = sum(años) / len(años) if años else 0

    # Total de estudiantes (usando función recursiva)
    total_estudiantes = sumar_estudiantes_recursivo(colegios)
    promedio_estudiantes = total_estudiantes / len(colegios) if colegios else 0

    # Colegios con más y menos estudiantes
    colegio_mas_estudiantes = max(colegios, key=lambda x: x.get("Cantidad de Estudiantes", 0))
    colegio_menos_estudiantes = min(colegios, key=lambda x: x.get("Cantidad de Estudiantes", 999999))

    # Conteo por provincia (usando función recursiva)
    colegios_por_provincia = contar_colegios_por_provincia_recursivo(colegios)

    print("\n" + "=" * 60)
    print("📊 ESTADÍSTICAS GENERALES")
    print("=" * 60)
    print(f"📅 Colegio más antiguo: {colegio_mas_antiguo.get('Colegio')} ({colegio_mas_antiguo.get('Año de Creación')})")
    print(f"📅 Colegio más nuevo: {colegio_mas_nuevo.get('Colegio')} ({colegio_mas_nuevo.get('Año de Creación')})")
    print(f"📅 Año promedio de creación: {int(promedio_año)}")
    print("")
    print(f"👥 Total de estudiantes: {total_estudiantes:,}")
    print(f"👥 Promedio de estudiantes por colegio: {int(promedio_estudiantes):,}")
    print(f"👥 Colegio con más estudiantes: {colegio_mas_estudiantes.get('Colegio')} ({colegio_mas_estudiantes.get('Cantidad de Estudiantes'):,})")
    print(f"👥 Colegio con menos estudiantes: {colegio_menos_estudiantes.get('Colegio')} ({colegio_menos_estudiantes.get('Cantidad de Estudiantes'):,})")
    print("")
    print("🏛️ Cantidad de colegios por provincia:")
    for provincia, cantidad in sorted(colegios_por_provincia.items()):
        print(f"      - {provincia}: {cantidad}")
    print("=" * 60)
