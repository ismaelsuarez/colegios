"""Funciones para mostrar y ordenar colegios."""

from typing import List, Dict
from funciones.utilidades import normalizar


def mostrar_colegios_recursivo(colegios: List[Dict], indice: int = 0) -> None:
    """Muestra los colegios de forma recursiva.

    Implementación recursiva para cumplir con los requisitos del proyecto.

    Args:
        colegios (list[dict]): Lista de diccionarios con colegios.
        indice (int): Índice actual en la lista (para recursión).
    """
    # Caso base: se recorrió toda la lista
    if indice >= len(colegios):
        return

    # Procesar el elemento actual
    c = colegios[indice]
    provincia = c.get("Provincia", "")
    colegio = c.get("Colegio", "")
    cantidad = c.get("Cantidad de Estudiantes", 0)
    año = c.get("Año de Creación", 0)
    print(f"  🏫 {colegio} | Provincia: {provincia} | Estudiantes: {cantidad:,} | Año: {año}")

    # Llamada recursiva para el siguiente elemento
    mostrar_colegios_recursivo(colegios, indice + 1)


def mostrar_colegios(colegios: List[Dict]) -> None:
    """Muestra los colegios con todos sus datos de forma prolija.

    Esta función utiliza la implementación recursiva internamente.

    Args:
        colegios (list[dict]): Lista de diccionarios con colegios.
    """
    if not colegios:
        print("  No hay colegios para mostrar.")
        return

    # Usar función recursiva
    mostrar_colegios_recursivo(colegios)


def ordenar_colegios(colegios: List[Dict], campo: str, descendente: bool = False) -> List[Dict]:
    """Ordena la lista de colegios por el campo especificado.

    Args:
        colegios (list[dict]): Lista de colegios a ordenar.
        campo (str): Campo por el cual ordenar. Opciones: 'Provincia', 'Colegio',
            'Cantidad de Estudiantes', 'Año de Creación'.
        descendente (bool): Si True, orden descendente; si False, ascendente.

    Returns:
        list[dict]: Lista ordenada de colegios.
    """
    if not colegios:
        return []

    # Validar campo
    campos_validos = ["Provincia", "Colegio", "Cantidad de Estudiantes", "Año de Creación"]
    if campo not in campos_validos:
        print(f"⚠️ Campo inválido. Campos válidos: {', '.join(campos_validos)}")
        return colegios

    try:
        # Ordenar
        colegios_ordenados = sorted(
            colegios,
            key=lambda x: (
                normalizar(x.get(campo, "")) if campo in ["Provincia", "Colegio"]
                else x.get(campo, 0)
            ),
            reverse=descendente
        )
        return colegios_ordenados
    except Exception as e:
        print(f"⚠️ Error al ordenar: {e}")
        return colegios
