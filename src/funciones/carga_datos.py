"""Funciones CRUD para gestión de colegios en modo local.

Este módulo proporciona funciones para agregar, editar y borrar colegios
en el archivo CSV local.
"""

from typing import List, Dict
from funciones.vista import mostrar_colegios
from funciones.utilidades import normalizar


def agregar_colegio(colegios: List[Dict], ruta_csv: str) -> bool:
    """Agrega un nuevo colegio a la lista y lo guarda en el CSV.

    Args:
        colegios (list[dict]): Lista actual de colegios.
        ruta_csv (str): Ruta del archivo CSV donde guardar.

    Returns:
        bool: True si se agregó correctamente, False en caso contrario.
    """
    print("\n📝 Agregar nuevo colegio")
    print("-" * 40)

    try:
        provincia = input("Provincia: ").strip()
        colegio = input("Colegio: ").strip()
        cantidad_str = input("Cantidad de Estudiantes: ").strip()
        año_str = input("Año de Creación: ").strip()

        if not provincia or not colegio:
            print("⚠️ La provincia y el colegio son campos obligatorios.")
            return False

        # Validar campos numéricos
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

        nuevo_colegio = {
            "Provincia": provincia,
            "Colegio": colegio,
            "Cantidad de Estudiantes": cantidad_estudiantes,
            "Año de Creación": año_creacion
        }

        colegios.append(nuevo_colegio)

        # Guardar en CSV
        from funciones.utilidades import escribir_csv
        if escribir_csv(ruta_csv, colegios):
            print(f"\n✅ Colegio '{colegio}' agregado correctamente.")
            return True
        else:
            print("\n⚠️ Error al guardar en el archivo CSV.")
            colegios.pop()  # Revertir el cambio
            return False

    except KeyboardInterrupt:
        print("\n\n⚠️ Operación cancelada.")
        return False
    except Exception as e:
        print(f"\n⚠️ Error al agregar el colegio: {e}")
        return False


def editar_colegio(colegios: List[Dict], ruta_csv: str) -> bool:
    """Edita un colegio existente.

    Args:
        colegios (list[dict]): Lista actual de colegios.
        ruta_csv (str): Ruta del archivo CSV donde guardar.

    Returns:
        bool: True si se editó correctamente, False en caso contrario.
    """
    if not colegios:
        print("\n⚠️ No hay colegios para editar.")
        return False

    print("\n✏️ Editar colegio")
    print("-" * 40)
    nombre_buscar = input("Ingrese el nombre del colegio a editar: ").strip()

    if not nombre_buscar:
        print("⚠️ Debe ingresar un nombre.")
        return False

    # Buscar colegio
    nombre_normalizado = normalizar(nombre_buscar)
    indices_encontrados = [
        i for i, c in enumerate(colegios)
        if nombre_normalizado in normalizar(c.get("Colegio", ""))
    ]

    if not indices_encontrados:
        print(f"\n⚠️ No se encontró ningún colegio con el nombre '{nombre_buscar}'.")
        return False

    if len(indices_encontrados) > 1:
        print(f"\n⚠️ Se encontraron {len(indices_encontrados)} colegios. Mostrando resultados:")
        for i, idx in enumerate(indices_encontrados, 1):
            print(f"{i}. {colegios[idx].get('Colegio')} ({colegios[idx].get('Provincia')})")
        
        try:
            opcion = int(input("\nIngrese el número del colegio a editar: ")) - 1
            if 0 <= opcion < len(indices_encontrados):
                idx_editar = indices_encontrados[opcion]
            else:
                print("⚠️ Opción inválida.")
                return False
        except ValueError:
            print("⚠️ Debe ingresar un número.")
            return False
    else:
        idx_editar = indices_encontrados[0]

    colegio_original = colegios[idx_editar].copy()
    print(f"\n📋 Colegio a editar: {colegio_original.get('Colegio')}")

    try:
        print("\nDeje en blanco para mantener el valor actual.")
        nueva_provincia = input(f"Provincia [{colegio_original.get('Provincia')}]: ").strip()
        nuevo_colegio = input(f"Colegio [{colegio_original.get('Colegio')}]: ").strip()
        nueva_cantidad_str = input(f"Cantidad de Estudiantes [{colegio_original.get('Cantidad de Estudiantes')}]: ").strip()
        nuevo_año_str = input(f"Año de Creación [{colegio_original.get('Año de Creación')}]: ").strip()

        # Aplicar cambios
        if nueva_provincia:
            colegios[idx_editar]["Provincia"] = nueva_provincia
        if nuevo_colegio:
            colegios[idx_editar]["Colegio"] = nuevo_colegio
        if nueva_cantidad_str:
            try:
                cantidad = int(nueva_cantidad_str)
                if cantidad < 0:
                    print("⚠️ La cantidad de estudiantes no puede ser negativa.")
                    return False
                colegios[idx_editar]["Cantidad de Estudiantes"] = cantidad
            except ValueError:
                print("⚠️ La cantidad de estudiantes debe ser un número entero.")
                return False
        if nuevo_año_str:
            try:
                año = int(nuevo_año_str)
                if año < 1800 or año > 2100:
                    print("⚠️ El año de creación debe ser un valor razonable (1800-2100).")
                    return False
                colegios[idx_editar]["Año de Creación"] = año
            except ValueError:
                print("⚠️ El año debe ser un número entero.")
                return False

        # Guardar en CSV
        from funciones.utilidades import escribir_csv
        if escribir_csv(ruta_csv, colegios):
            print(f"\n✅ Colegio actualizado correctamente.")
            return True
        else:
            print("\n⚠️ Error al guardar en el archivo CSV.")
            colegios[idx_editar] = colegio_original  # Revertir cambios
            return False

    except KeyboardInterrupt:
        print("\n\n⚠️ Operación cancelada.")
        colegios[idx_editar] = colegio_original
        return False
    except Exception as e:
        print(f"\n⚠️ Error al editar el colegio: {e}")
        colegios[idx_editar] = colegio_original
        return False


def borrar_colegio(colegios: List[Dict], ruta_csv: str) -> bool:
    """Borra un colegio de la lista.

    Args:
        colegios (list[dict]): Lista actual de colegios.
        ruta_csv (str): Ruta del archivo CSV donde guardar.

    Returns:
        bool: True si se borró correctamente, False en caso contrario.
    """
    if not colegios:
        print("\n⚠️ No hay colegios para borrar.")
        return False

    print("\n🗑️ Borrar colegio")
    print("-" * 40)
    nombre_buscar = input("Ingrese el nombre del colegio a borrar: ").strip()

    if not nombre_buscar:
        print("⚠️ Debe ingresar un nombre.")
        return False

    # Buscar colegio
    nombre_normalizado = normalizar(nombre_buscar)
    indices_encontrados = [
        i for i, c in enumerate(colegios)
        if nombre_normalizado in normalizar(c.get("Colegio", ""))
    ]

    if not indices_encontrados:
        print(f"\n⚠️ No se encontró ningún colegio con el nombre '{nombre_buscar}'.")
        return False

    if len(indices_encontrados) > 1:
        print(f"\n⚠️ Se encontraron {len(indices_encontrados)} colegios. Mostrando resultados:")
        for i, idx in enumerate(indices_encontrados, 1):
            print(f"{i}. {colegios[idx].get('Colegio')} ({colegios[idx].get('Provincia')})")
        
        try:
            opcion = int(input("\nIngrese el número del colegio a borrar: ")) - 1
            if 0 <= opcion < len(indices_encontrados):
                idx_borrar = indices_encontrados[opcion]
            else:
                print("⚠️ Opción inválida.")
                return False
        except ValueError:
            print("⚠️ Debe ingresar un número.")
            return False
    else:
        idx_borrar = indices_encontrados[0]

    colegio_borrar = colegios[idx_borrar]
    print(f"\n⚠️ Está por borrar: {colegio_borrar.get('Colegio')} ({colegio_borrar.get('Provincia')})")
    confirmar = input("¿Está seguro? (s/n): ").strip().lower()

    if confirmar != 's':
        print("⚠️ Operación cancelada.")
        return False

    try:
        colegios.pop(idx_borrar)

        # Guardar en CSV
        from funciones.utilidades import escribir_csv
        if escribir_csv(ruta_csv, colegios):
            print(f"\n✅ Colegio '{colegio_borrar.get('Colegio')}' borrado correctamente.")
            return True
        else:
            print("\n⚠️ Error al guardar en el archivo CSV.")
            colegios.insert(idx_borrar, colegio_borrar)  # Revertir cambio
            return False

    except Exception as e:
        print(f"\n⚠️ Error al borrar el colegio: {e}")
        return False
