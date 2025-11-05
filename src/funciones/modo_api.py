"""Funciones para modo API.

Este módulo adapta las funciones locales para trabajar con datos obtenidos
desde la API en http://149.50.150.15:8020.
"""

from typing import List, Dict, Optional
from funciones import cliente_api
from funciones.vista import mostrar_colegios, ordenar_colegios
from funciones.busqueda import buscar_colegio, filtrar_por_provincia, filtrar_por_rango_estudiantes, filtrar_por_rango_año
from funciones.estadisticas import mostrar_estadisticas


def obtener_colegios_api(
    q: Optional[str] = None,
    provincia: Optional[str] = None,
    sort_by: Optional[str] = None,
    desc: bool = False,
) -> List[Dict]:
    """Obtiene colegios desde la API con filtros opcionales.

    Args:
        q (str | None): Texto a buscar (busca en Colegio o Provincia).
        provincia (str | None): Filtro por provincia.
        sort_by (str | None): Campo de ordenamiento (Provincia, Colegio, Cantidad de Estudiantes, Año de Creación).
        desc (bool): Si True, orden descendente.

    Returns:
        list[dict]: Lista de colegios con estructura: Provincia, Colegio, Cantidad de Estudiantes, Año de Creación.
    """
    try:
        items = cliente_api.listar_colegios(
            q=q,
            provincia=provincia,
            ordenar_por=sort_by,
            descendente=desc,
        )

        # Verificar que items sea una lista
        if not isinstance(items, list):
            print(f"⚠️ Error: La API no devolvió una lista. Tipo recibido: {type(items)}")
            return []

        # Verificar si la lista está vacía
        if len(items) == 0:
            print(f"\n⚠️ La API no tiene datos disponibles.")
            print(f"   La API en http://149.50.150.15:8020 está conectada pero no contiene colegios.")
            print(f"   Necesitás cargar datos primero usando la opción 'Agregar un colegio' del menú.")
            return []

        return items
    except Exception as e:
        print(f"⚠️ Error al obtener colegios desde la API: {e}")
        import traceback
        traceback.print_exc()
        return []


def buscar_colegio_api(nombre: str) -> None:
    """Busca colegios por nombre usando la API.

    Args:
        nombre (str): Nombre del colegio a buscar.
    """
    colegios = obtener_colegios_api(q=nombre)
    if colegios:
        buscar_colegio(colegios, nombre)
    else:
        print(f"\n⚠️ No se encontraron colegios con el nombre '{nombre}'.")


def filtrar_provincia_api(provincia: str) -> None:
    """Filtra colegios por provincia usando la API.

    Args:
        provincia (str): Nombre de la provincia.
    """
    colegios = obtener_colegios_api(provincia=provincia)
    if colegios:
        filtrar_por_provincia(colegios, provincia)
    else:
        print(f"\n⚠️ No se encontraron colegios en la provincia '{provincia}'.")


def filtrar_rango_estudiantes_api(minimo: int, maximo: int) -> None:
    """Filtra colegios por rango de estudiantes usando la API.

    Args:
        minimo (int): Cantidad mínima de estudiantes.
        maximo (int): Cantidad máxima de estudiantes.
    """
    colegios = obtener_colegios_api()
    if colegios:
        filtrar_por_rango_estudiantes(colegios, minimo, maximo)
    else:
        print("\n⚠️ No se pudieron obtener datos de la API.")


def filtrar_rango_año_api(minimo: int, maximo: int) -> None:
    """Filtra colegios por rango de año de creación usando la API.

    Args:
        minimo (int): Año mínimo.
        maximo (int): Año máximo.
    """
    colegios = obtener_colegios_api()
    if colegios:
        filtrar_por_rango_año(colegios, minimo, maximo)
    else:
        print("\n⚠️ No se pudieron obtener datos de la API.")


def ordenar_colegios_api(campo: str, descendente: bool = False) -> None:
    """Ordena y muestra colegios obtenidos desde la API.

    Args:
        campo (str): Campo por el cual ordenar.
        descendente (bool): Si True, orden descendente.
    """
    colegios = obtener_colegios_api(sort_by=campo, desc=descendente)
    if colegios:
        mostrar_colegios(colegios)
    else:
        print("\n⚠️ No se pudieron obtener datos de la API.")


def estadisticas_api() -> None:
    """Muestra estadísticas de los colegios obtenidos desde la API."""
    colegios = obtener_colegios_api()
    if colegios:
        mostrar_estadisticas(colegios)
    else:
        print("\n⚠️ No se pudieron obtener datos de la API.")


def agregar_colegio_api() -> bool:
    """Agrega un nuevo colegio usando la API.

    Returns:
        bool: True si se agregó correctamente, False en caso contrario.
    """
    print("\n📝 Agregar nuevo colegio (API)")
    print("-" * 40)

    try:
        provincia = input("Provincia: ").strip()
        colegio = input("Colegio: ").strip()
        cantidad_str = input("Cantidad de Estudiantes: ").strip()
        año_str = input("Año de Creación: ").strip()

        if not provincia or not colegio:
            print("⚠️ La provincia y el colegio son campos obligatorios.")
            return False

        try:
            cantidad_estudiantes = int(cantidad_str) if cantidad_str else 0
            año_creacion = int(año_str) if año_str else 0

            if cantidad_estudiantes < 0:
                print("⚠️ La cantidad de estudiantes no puede ser negativa.")
                return False
            if año_creacion < 1800 or año_creacion > 2100:
                print("⚠️ El año de creación debe ser un valor razonable (1800-2100).")
                return False

        except ValueError:
            print("⚠️ La cantidad de estudiantes y el año deben ser números enteros.")
            return False

        nuevo_colegio = cliente_api.crear_colegio(
            provincia=provincia,
            colegio=colegio,
            cantidad_estudiantes=cantidad_estudiantes,
            año_creacion=año_creacion,
        )

        print(f"\n✅ Colegio '{colegio}' agregado correctamente en la API.")
        return True

    except Exception as e:
        print(f"\n⚠️ Error al agregar el colegio en la API: {e}")
        return False


def editar_colegio_api() -> bool:
    """Edita un colegio usando la API.

    Returns:
        bool: True si se editó correctamente, False en caso contrario.
    """
    print("\n✏️ Editar colegio (API)")
    print("-" * 40)

    try:
        # Primero buscar el colegio
        nombre_buscar = input("Ingrese el nombre del colegio a editar: ").strip()
        if not nombre_buscar:
            print("⚠️ Debe ingresar un nombre.")
            return False

        colegios = obtener_colegios_api(q=nombre_buscar)
        if not colegios:
            print(f"\n⚠️ No se encontró ningún colegio con el nombre '{nombre_buscar}'.")
            return False

        # Si hay múltiples resultados, mostrar y seleccionar
        if len(colegios) > 1:
            print(f"\n⚠️ Se encontraron {len(colegios)} colegios:")
            for i, c in enumerate(colegios, 1):
                print(f"{i}. {c.get('Colegio')} ({c.get('Provincia')}) - ID: {c.get('id')}")

            try:
                opcion = int(input("\nIngrese el número del colegio a editar: ")) - 1
                if 0 <= opcion < len(colegios):
                    colegio_editar = colegios[opcion]
                else:
                    print("⚠️ Opción inválida.")
                    return False
            except ValueError:
                print("⚠️ Debe ingresar un número.")
                return False
        else:
            colegio_editar = colegios[0]

        id_colegio = colegio_editar.get('id')
        if not id_colegio:
            print("⚠️ El colegio no tiene ID válido.")
            return False

        print(f"\n📋 Colegio a editar: {colegio_editar.get('Colegio')}")
        print("\nDeje en blanco para mantener el valor actual.")

        cambios = {}
        nueva_provincia = input(f"Provincia [{colegio_editar.get('Provincia')}]: ").strip()
        nuevo_colegio = input(f"Colegio [{colegio_editar.get('Colegio')}]: ").strip()
        nueva_cantidad_str = input(f"Cantidad de Estudiantes [{colegio_editar.get('Cantidad de Estudiantes')}]: ").strip()
        nuevo_año_str = input(f"Año de Creación [{colegio_editar.get('Año de Creación')}]: ").strip()

        if nueva_provincia:
            cambios["Provincia"] = nueva_provincia
        if nuevo_colegio:
            cambios["Colegio"] = nuevo_colegio
        if nueva_cantidad_str:
            try:
                cambios["Cantidad de Estudiantes"] = int(nueva_cantidad_str)
            except ValueError:
                print("⚠️ La cantidad de estudiantes debe ser un número entero.")
                return False
        if nuevo_año_str:
            try:
                año = int(nuevo_año_str)
                if año < 1800 or año > 2100:
                    print("⚠️ El año de creación debe ser un valor razonable (1800-2100).")
                    return False
                cambios["Año de Creación"] = año
            except ValueError:
                print("⚠️ El año debe ser un número entero.")
                return False

        if not cambios:
            print("⚠️ No se ingresaron cambios.")
            return False

        cliente_api.actualizar_colegio_parcial(id_colegio, cambios)
        print(f"\n✅ Colegio actualizado correctamente en la API.")
        return True

    except Exception as e:
        print(f"\n⚠️ Error al editar el colegio en la API: {e}")
        return False


def borrar_colegio_api() -> bool:
    """Borra un colegio usando la API.

    Returns:
        bool: True si se borró correctamente, False en caso contrario.
    """
    print("\n🗑️ Borrar colegio (API)")
    print("-" * 40)

    try:
        nombre_buscar = input("Ingrese el nombre del colegio a borrar: ").strip()
        if not nombre_buscar:
            print("⚠️ Debe ingresar un nombre.")
            return False

        colegios = obtener_colegios_api(q=nombre_buscar)
        if not colegios:
            print(f"\n⚠️ No se encontró ningún colegio con el nombre '{nombre_buscar}'.")
            return False

        # Si hay múltiples resultados, mostrar y seleccionar
        if len(colegios) > 1:
            print(f"\n⚠️ Se encontraron {len(colegios)} colegios:")
            for i, c in enumerate(colegios, 1):
                print(f"{i}. {c.get('Colegio')} ({c.get('Provincia')}) - ID: {c.get('id')}")

            try:
                opcion = int(input("\nIngrese el número del colegio a borrar: ")) - 1
                if 0 <= opcion < len(colegios):
                    colegio_borrar = colegios[opcion]
                else:
                    print("⚠️ Opción inválida.")
                    return False
            except ValueError:
                print("⚠️ Debe ingresar un número.")
                return False
        else:
            colegio_borrar = colegios[0]

        id_colegio = colegio_borrar.get('id')
        if not id_colegio:
            print("⚠️ El colegio no tiene ID válido.")
            return False

        print(f"\n⚠️ Está por borrar: {colegio_borrar.get('Colegio')} ({colegio_borrar.get('Provincia')})")
        confirmar = input("¿Está seguro? (s/n): ").strip().lower()

        if confirmar != 's':
            print("⚠️ Operación cancelada.")
            return False

        cliente_api.eliminar_colegio(id_colegio)
        print(f"\n✅ Colegio '{colegio_borrar.get('Colegio')}' borrado correctamente de la API.")
        return True

    except Exception as e:
        print(f"\n⚠️ Error al borrar el colegio de la API: {e}")
        return False
