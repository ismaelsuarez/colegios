"""Punto de entrada de la aplicación de gestión de colegios.

Este módulo:
- Ajusta `sys.path` para permitir importaciones relativas desde `src/` y la raíz.
- Inicializa la base de datos y carga el CSV de colegios.
- Permite elegir entre modo local (archivos) y modo API (servidor).
- Ejecuta el bucle del menú principal para consultar y gestionar datos.
"""

import sys
import os

script_path = os.path.abspath(__file__)
app_dir = os.path.dirname(script_path)
project_root = os.path.dirname(app_dir)
src_dir = os.path.join(project_root, 'src')

if project_root not in sys.path:
    sys.path.append(project_root)
if src_dir not in sys.path:
    sys.path.append(src_dir)

try:
    from funciones.inicializar import init_db
    from funciones.vista import *
    from funciones.estadisticas import *
    from funciones.utilidades import *
    from funciones.carga_datos import *
    from funciones.busqueda import *
    from funciones import cliente_api
    from funciones.modo_api import *
except ImportError as e:
    print(f"⚠️ Error: No se pudo importar módulos desde 'funciones': {e}")
    print(f"   Raíz del proyecto calculada: {project_root}")
    sys.exit(1)

db_path = init_db(project_root)
if db_path is None:
    print("⚠️ Error: No se pudo inicializar la base de datos.")
    sys.exit(1)

colegios = leer_csv(db_path)

# Indicador global de modo de operación. False = local, True = API.
MODO_API = False


def elegir_modo():
    """Permite al usuario elegir entre modo local y modo API."""
    global MODO_API

    opcion = seleccionar_modo()

    if opcion == 1:
        MODO_API = False
        print("\n✅ Modo: Archivo CSV local")
        print(f"   Ubicación: {db_path}")
        # Recargar datos locales
        global colegios
        colegios = leer_csv(db_path)
        if colegios:
            print(f"   ✅ Se cargaron {len(colegios)} colegio(s).")
        else:
            print("   ⚠️ No hay colegios en el archivo CSV local.")
        return True

    elif opcion == 2:
        MODO_API = True
        print("\n✅ Modo: Servidor API remoto")
        print(f"   URL: http://149.50.150.15:8020")
        try:
            estado = cliente_api.estado_servidor()
            print(f"   ✅ Conexión exitosa: {estado.get('status', 'OK')}")
        except Exception as e:
            print(f"   ⚠️ Error al conectar con el servidor: {e}")
            print("   Se volverá a modo local automáticamente...")
            MODO_API = False
            colegios = leer_csv(db_path)
            return True

        return True

    elif opcion == 3:
        print("\n👋 ¡Hasta luego!")
        return False

    else:
        print("\n⚠️ Opción inválida. Intente nuevamente.")
        return elegir_modo()


def main():
    """Función principal que ejecuta el bucle del menú."""
    global colegios, MODO_API

    print("=" * 70)
    print("🏫 SISTEMA DE GESTIÓN Y CONSULTA DE COLEGIOS 🏫")
    print("=" * 70)

    if not elegir_modo():
        sys.exit(0)

    while True:
        try:
            opcion = menu_principal()

            if opcion == 1:
                # Buscar colegio por nombre
                if MODO_API:
                    nombre = input("\n📝 Ingrese el nombre del colegio a buscar: ").strip()
                    if nombre:
                        buscar_colegio_api(nombre)
                else:
                    nombre = input("\n📝 Ingrese el nombre del colegio a buscar: ").strip()
                    if nombre:
                        buscar_colegio(colegios, nombre)

            elif opcion == 2:
                # Filtrar por provincia
                if MODO_API:
                    provincia = input("\n🗺️  Ingrese la provincia: ").strip()
                    if provincia:
                        filtrar_provincia_api(provincia)
                else:
                    provincia = input("\n🗺️  Ingrese la provincia: ").strip()
                    if provincia:
                        filtrar_por_provincia(colegios, provincia)

            elif opcion == 3:
                # Filtrar por rango de cantidad de estudiantes
                minimo, maximo = pedir_rango("cantidad de estudiantes")
                if minimo is not None and maximo is not None:
                    if MODO_API:
                        filtrar_rango_estudiantes_api(minimo, maximo)
                    else:
                        filtrar_por_rango_estudiantes(colegios, minimo, maximo)

            elif opcion == 4:
                # Filtrar por rango de año de creación
                minimo, maximo = pedir_rango("año de creación")
                if minimo is not None and maximo is not None:
                    if MODO_API:
                        filtrar_rango_año_api(minimo, maximo)
                    else:
                        filtrar_por_rango_año(colegios, minimo, maximo)

            elif opcion == 5:
                # Ordenar colegios
                print("\n📊 Campos disponibles para ordenar:")
                print("   - Provincia")
                print("   - Colegio")
                print("   - Cantidad de Estudiantes")
                print("   - Año de Creación")
                campo = input("\n🔢 Ingrese el campo por el cual ordenar: ").strip()
                orden = input("⬇️  ¿Orden descendente? (s/n): ").strip().lower()
                descendente = orden == 's'

                if campo:
                    if MODO_API:
                        ordenar_colegios_api(campo, descendente)
                    else:
                        colegios_ordenados = ordenar_colegios(colegios, campo, descendente)
                        mostrar_colegios(colegios_ordenados)

            elif opcion == 6:
                # Mostrar estadísticas
                if MODO_API:
                    estadisticas_api()
                else:
                    mostrar_estadisticas(colegios)

            elif opcion == 7:
                # Agregar un colegio
                if MODO_API:
                    agregar_colegio_api()
                else:
                    if agregar_colegio(colegios, db_path):
                        colegios = leer_csv(db_path)

            elif opcion == 8:
                # Editar un colegio
                if MODO_API:
                    editar_colegio_api()
                else:
                    if editar_colegio(colegios, db_path):
                        colegios = leer_csv(db_path)

            elif opcion == 9:
                # Borrar colegio
                if MODO_API:
                    borrar_colegio_api()
                else:
                    if borrar_colegio(colegios, db_path):
                        colegios = leer_csv(db_path)

            elif opcion == 10:
                # Cambiar modo de servidor
                if not elegir_modo():
                    break

            elif opcion == 11:
                # Salir
                print("\n👋 ¡Gracias por usar el Sistema de Gestión de Colegios!")
                break

            else:
                print("\n⚠️ Opción inválida. Por favor ingrese un número del 1 al 11.")

        except KeyboardInterrupt:
            print("\n\n⚠️ Operación cancelada por el usuario.")
            respuesta = input("¿Desea salir del sistema? (s/n): ").strip().lower()
            if respuesta == 's':
                print("\n👋 ¡Hasta luego!")
                break
        except ValueError:
            print("\n⚠️ Entrada inválida. Por favor ingrese un número.")
        except Exception as e:
            print(f"\n⚠️ Error inesperado: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()
