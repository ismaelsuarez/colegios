"""Funciones de búsqueda y filtrado de colegios."""

from typing import List, Dict
from funciones.utilidades import normalizar
from funciones.vista import mostrar_colegios


def buscar_colegio_recursivo(colegios: List[Dict], nombre: str, indice: int = 0, resultados: List[Dict] = None) -> List[Dict]:
    """Busca colegios de forma recursiva que contengan el texto ingresado en el nombre.

    Implementación recursiva para cumplir con los requisitos del proyecto.

    Args:
        colegios (list[dict]): Lista de colegios donde buscar.
        nombre (str): Texto a buscar.
        indice (int): Índice actual en la lista (para recursión).
        resultados (list[dict]): Lista acumulativa de resultados.

    Returns:
        list[dict]: Lista de colegios que coinciden con la búsqueda.
    """
    if resultados is None:
        resultados = []

    # Caso base: se recorrió toda la lista
    if indice >= len(colegios):
        return resultados

    # Procesar el elemento actual
    colegio_actual = colegios[indice]
    nombre_colegio = normalizar(colegio_actual.get("Colegio", ""))
    nombre_buscar = normalizar(nombre)

    if nombre_buscar in nombre_colegio:
        resultados.append(colegio_actual)

    # Llamada recursiva para el siguiente elemento
    return buscar_colegio_recursivo(colegios, nombre, indice + 1, resultados)


def buscar_colegio(colegios: List[Dict], nombre: str) -> List[Dict]:
    """Busca colegios que contengan el texto ingresado en el nombre.

    Esta función utiliza la implementación recursiva internamente.

    Args:
        colegios (list[dict]): Lista de colegios donde buscar.
        nombre (str): Texto a buscar.

    Returns:
        list[dict]: Lista de colegios que coinciden con la búsqueda.
    """
    if not colegios or not nombre:
        return []

    # Usar búsqueda recursiva
    resultados = buscar_colegio_recursivo(colegios, nombre)

    if resultados:
        print(f"\n✅ Se encontraron {len(resultados)} colegio(s) con el nombre '{nombre}':")
        # Mostrar colegios con índice numérico para facilitar identificación
        for i, colegio in enumerate(resultados, 1):
            print(
                f"{i}. {colegio.get('Colegio', '')} | "
                f"Provincia: {colegio.get('Provincia', '')} | "
                f"Estudiantes: {colegio.get('Cantidad de Estudiantes', 0)} | "
                f"Año: {colegio.get('Año de Creación', 0)}"
            )
    else:
        print(f"\n⚠️ No se encontró ningún colegio que contenga '{nombre}'.")

    return resultados


def filtrar_por_provincia(colegios: List[Dict], provincia: str) -> List[Dict]:
    """Filtra colegios por provincia.

    Args:
        colegios (list[dict]): Lista de colegios a filtrar.
        provincia (str): Nombre de la provincia.

    Returns:
        list[dict]: Lista de colegios filtrados.
    """
    if not colegios or not provincia:
        return []

    provincia_normalizada = normalizar(provincia)
    resultados = [
        c for c in colegios
        if provincia_normalizada in normalizar(c.get("Provincia", ""))
    ]

    if resultados:
        print(f"\n✅ Colegios en la provincia '{provincia}': ({len(resultados)} encontrado(s))")
        mostrar_colegios(resultados)
    else:
        print(f"\n⚠️ No se encontraron colegios en la provincia '{provincia}'.")

    return resultados


def filtrar_por_rango_estudiantes(colegios: List[Dict], minimo: int, maximo: int) -> List[Dict]:
    """Filtra colegios por rango de cantidad de estudiantes.

    Args:
        colegios (list[dict]): Lista de colegios a filtrar.
        minimo (int): Cantidad mínima de estudiantes.
        maximo (int): Cantidad máxima de estudiantes.

    Returns:
        list[dict]: Lista de colegios filtrados.
    """
    if not colegios:
        return []

    resultados = [
        c for c in colegios
        if minimo <= c.get("Cantidad de Estudiantes", 0) <= maximo
    ]

    if resultados:
        print(f"\n✅ Colegios con {minimo:,} a {maximo:,} estudiantes: ({len(resultados)} encontrado(s))")
        mostrar_colegios(resultados)
    else:
        print(f"\n⚠️ No se encontraron colegios en ese rango de estudiantes.")

    return resultados


def filtrar_por_rango_año(colegios: List[Dict], minimo: int, maximo: int) -> List[Dict]:
    """Filtra colegios por rango de año de creación.

    Args:
        colegios (list[dict]): Lista de colegios a filtrar.
        minimo (int): Año mínimo de creación.
        maximo (int): Año máximo de creación.

    Returns:
        list[dict]: Lista de colegios filtrados.
    """
    if not colegios:
        return []

    resultados = [
        c for c in colegios
        if minimo <= c.get("Año de Creación", 0) <= maximo
    ]

    if resultados:
        print(f"\n✅ Colegios creados entre {minimo} y {maximo}: ({len(resultados)} encontrado(s))")
        mostrar_colegios(resultados)
    else:
        print(f"\n⚠️ No se encontraron colegios creados en ese rango de años.")

    return resultados
