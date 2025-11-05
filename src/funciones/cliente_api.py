"""Cliente HTTP para interactuar con la API de colegios.

Este módulo proporciona funciones para realizar peticiones HTTP a la API
en http://149.50.150.15:8020.
"""

import requests
from typing import List, Dict, Optional


BASE_URL = "http://149.50.150.15:8020"

def establecer_base_url(url: str) -> None:
    """Permite cambiar la URL base del servidor (útil para pruebas).
    
    Args:
        url (str): Nueva URL base del servidor.
    """
    global BASE_URL
    BASE_URL = (url or "").rstrip("/")


def _url(endpoint: str) -> str:
    """Construye la URL completa del endpoint.

    Args:
        endpoint (str): Ruta del endpoint (ej: '/colegios', '/health').

    Returns:
        str: URL completa.
    """
    return f"{BASE_URL}{endpoint}"


def estado_servidor() -> Dict:
    """Verifica el estado del servidor.

    Returns:
        dict: Diccionario con el estado del servidor.

    Raises:
        requests.HTTPError: Si la respuesta no es correcta.
        requests.ConnectionError: Si no se puede conectar al servidor.
    """
    try:
        resp = requests.get(_url("/health"), timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.ConnectionError as e:
        raise requests.ConnectionError(
            f"No se pudo conectar al servidor en {BASE_URL}. "
            f"Verifica que el servidor esté corriendo y el puerto 8020 esté abierto. "
            f"Error: {e}"
        ) from e


def listar_colegios(
    q: Optional[str] = None,
    provincia: Optional[str] = None,
    ordenar_por: Optional[str] = None,
    descendente: bool = False,
) -> List[Dict]:
    """Lista colegios con filtros y orden opcional.

    Args:
        q (str | None): Texto para buscar por colegio o provincia.
        provincia (str | None): Filtro por provincia.
        ordenar_por (str | None): Campo de orden (ej.: 'Provincia', 'Colegio', 'Cantidad de Estudiantes', 'Año de Creación').
        descendente (bool): Si True, orden descendente.

    Returns:
        list[dict]: Lista de colegios con estructura: Provincia, Colegio, Cantidad de Estudiantes, Año de Creación.

    Raises:
        requests.HTTPError: Si la respuesta no es correcta.
    """
    params: Dict[str, str] = {}
    if q:
        params["q"] = q
    if provincia:
        params["Provincia"] = provincia
    if ordenar_por:
        params["sort_by"] = ordenar_por
    if descendente:
        params["desc"] = "true"

    resp = requests.get(_url("/colegios"), params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()


def obtener_colegio(id_colegio: int) -> Dict:
    """Obtiene un colegio por su ID.

    Args:
        id_colegio (int): ID del colegio.

    Returns:
        dict: Datos del colegio.

    Raises:
        requests.HTTPError: Si la respuesta no es correcta.
    """
    resp = requests.get(_url(f"/colegios/{id_colegio}"), timeout=10)
    resp.raise_for_status()
    return resp.json()


def crear_colegio(
    provincia: str,
    colegio: str,
    cantidad_estudiantes: int,
    año_creacion: int,
) -> Dict:
    """Crea un nuevo colegio.

    Args:
        provincia (str): Nombre de la provincia.
        colegio (str): Nombre del colegio.
        cantidad_estudiantes (int): Cantidad de estudiantes.
        año_creacion (int): Año de creación.

    Returns:
        dict: Datos del colegio creado.

    Raises:
        requests.HTTPError: Si la respuesta no es correcta.
    """
    payload = {
        "Provincia": provincia,
        "Colegio": colegio,
        "Cantidad de Estudiantes": cantidad_estudiantes,
        "Año de Creación": año_creacion,
    }
    resp = requests.post(_url("/colegios"), json=payload, timeout=10)
    resp.raise_for_status()
    return resp.json()


def actualizar_colegio_parcial(id_colegio: int, cambios: Dict) -> Dict:
    """Actualiza parcialmente un colegio.

    Args:
        id_colegio (int): ID del colegio.
        cambios (dict): Diccionario con los campos a actualizar.

    Returns:
        dict: Datos del colegio actualizado.

    Raises:
        requests.HTTPError: Si la respuesta no es correcta.
    """
    resp = requests.patch(_url(f"/colegios/{id_colegio}"), json=cambios, timeout=10)
    resp.raise_for_status()
    return resp.json()


def eliminar_colegio(id_colegio: int) -> bool:
    """Elimina un colegio.

    Args:
        id_colegio (int): ID del colegio a eliminar.

    Returns:
        bool: True si se eliminó correctamente.

    Raises:
        requests.HTTPError: Si la respuesta no es correcta.
    """
    resp = requests.delete(_url(f"/colegios/{id_colegio}"), timeout=10)
    resp.raise_for_status()
    return True
