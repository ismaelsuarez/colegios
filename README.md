# 🏫 Sistema de Gestión y Consulta de Colegios

Aplicación de **consola** para consultar y administrar datos de colegios desde un **CSV local** o una **API REST** remota. Permite **búsquedas**, **filtros**, **ordenamientos**, **estadísticas** y **CRUD** completo.

> Proyecto desarrollado para gestión educativa (UTN). Código y mensajes en **español**, con funciones sencillas y documentación estilo Google.

---

## 📋 Tabla de Contenidos

- [Características](#características)
- [Modos de Operación](#modos-de-operación)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Configuración Rápida](#configuración-rápida)
- [Ejecución](#ejecución)
- [Menú Principal](#menú-principal)
- [Estructura de Carpetas](#estructura-de-carpetas)
- [Flujo de Datos](#flujo-de-datos)
- [Guía de Uso](#guía-de-uso)
- [Ejemplos de Uso](#ejemplos-de-uso)
- [Solución de Problemas](#solución-de-problemas)
- [Participación de Integrantes](#participación-de-integrantes)
- [Video Integrador](#video-integrador)

---

## ✨ Características

- **Fuente de datos dual**:
  - **Local**: `src/base_de_datos/colegios.csv` (lectura/escritura)
  - **API**: Servidor FastAPI (HTTP GET/POST/PATCH/DELETE) en `http://149.50.150.15:8020`

- **Operaciones disponibles**:
  - 🔍 Buscar colegio por nombre
  - 🗺️ Filtrar por provincia
  - 👥 Filtrar por rango de cantidad de estudiantes
  - 📅 Filtrar por rango de año de fundación
  - 📊 Ordenar por cualquier campo (Provincia, Colegio, Cantidad de Estudiantes, Año de Creación)
  - 📈 Estadísticas generales (colegio más antiguo/nuevo, promedios, conteos por provincia)
  - ➕ Agregar colegio (CRUD)
  - ✏️ Editar colegio (CRUD)
  - 🗑️ Eliminar colegio (CRUD)

- **Compatibilidad y validación**:
  - Validación de errores comunes (acentos, espacios, datos faltantes)
  - Normalización de texto para búsquedas flexibles
  - Manejo robusto de errores
  - Interfaz amigable con mensajes claros

- **Docstrings**: Estilo Google en todos los módulos (mantenibles y legibles)

---

## 🔄 Modos de Operación

### Modo Local (CSV)
- Trabaja con `src/base_de_datos/colegios.csv`
- Si no existe, el sistema lo **crea automáticamente** con el encabezado correspondiente
- Todas las modificaciones persisten directamente en el archivo CSV
- No requiere conexión a internet

### Modo API (Servidor Remoto)
- Consume un servidor FastAPI en `http://149.50.150.15:8020`
- Usa el endpoint `/colegios`
- La API utiliza directamente el esquema de colegios con los campos:
  - `Provincia` (str)
  - `Colegio` (str)
  - `Cantidad de Estudiantes` (int)
  - `Año de Creación` (int)
- Requiere conexión a internet y que el servidor esté disponible
- Si el servidor no está disponible, el sistema vuelve automáticamente a modo local

---

## 📦 Requisitos

- **Python** >= 3.10 (probado en 3.13)
- **Sistema operativo**: Windows / Linux / macOS
- **Dependencias** (modo API): `requests`

### Instalación de Dependencias

**Windows (PowerShell/CMD)**
```bash
py -3.13 -m pip install --upgrade pip
py -3.13 -m pip install requests
```

**Linux / macOS**
```bash
python3 -m pip install --upgrade pip
python3 -m pip install requests
```

**Opcional: `requirements.txt`**
```text
requests>=2.32.0
```

> 💡 **Recomendado**: Crear un **entorno virtual** (venv) antes de instalar dependencias.

---

## 🚀 Instalación

### Opción 1: Clonar Repositorio
```bash
git clone <URL_DEL_REPOSITORIO>
cd TPI_Profesor_hualpa_com4
```

### Opción 2: Descargar ZIP
1. Abrir el repositorio en GitHub
2. `Code` → `Download ZIP`
3. Descomprimir la carpeta y abrirla en tu editor

---

## ⚙️ Configuración Rápida

### URL de la API
La URL base del servidor se define en `src/funciones/cliente_api.py`:
```python
BASE_URL = "http://149.50.150.15:8020"
```

### CSV Inicial
Si `src/base_de_datos/colegios.csv` no existe, se crea automáticamente con el encabezado:
```csv
Provincia,Colegio,Cantidad de Estudiantes,Año de Creación
```

**Codificación**: UTF-8 con BOM (para compatibilidad en Windows).

---

## ▶️ Ejecución

### Windows
```bash
py aplicacion/ejecutar.py
# Alternativa
python aplicacion/ejecutar.py
```

### Linux / macOS
```bash
python3 aplicacion/ejecutar.py
```

### Flujo de Inicio
1. El sistema verifica/crea `src/base_de_datos/colegios.csv`
2. Solicita el **modo de operación**:
   ```
   ╔══════════════════════════════════════════════════════════╗
   ║          SELECCIÓN DE FUENTE DE DATOS                    ║
   ╠══════════════════════════════════════════════════════════╣
   ║  1. 💾 Archivo CSV local                                 ║
   ║     └─ Trabaja con datos almacenados en este equipo      ║
   ║                                                           ║
   ║  2. 🌐 Servidor API remoto                               ║
   ║     └─ Conecta con servidor en http://149.50.150.15:8020 ║
   ║                                                           ║
   ║  3. ❌ Cancelar y salir                                  ║
   ╚══════════════════════════════════════════════════════════╝
   ```
3. Si eliges API, verifica `/health` con `estado_servidor()` en `http://149.50.150.15:8020`
4. Si el servidor no está disponible, vuelve automáticamente a modo local

---

## 📋 Menú Principal

```
╔══════════════════════════════════════════════════════════╗
║          MENÚ PRINCIPAL - GESTIÓN DE COLEGIOS            ║
╠══════════════════════════════════════════════════════════╣
║  CONSULTAS Y BÚSQUEDAS:                                  ║
║   1. 🔍 Buscar colegio por nombre                        ║
║   2. 🗺️  Listar colegios por provincia                   ║
║   3. 👥 Filtrar por cantidad de estudiantes              ║
║   4. 📅 Filtrar por año de fundación                      ║
║                                                           ║
║  ORGANIZACIÓN Y ANÁLISIS:                                ║
║   5. 📊 Ordenar lista de colegios                        ║
║   6. 📈 Ver estadísticas generales                        ║
║                                                           ║
║  ADMINISTRACIÓN DE DATOS:                                ║
║   7. ➕ Registrar nuevo colegio                           ║
║   8. ✏️  Modificar datos de colegio                       ║
║   9. 🗑️  Eliminar colegio del sistema                    ║
║                                                           ║
║  CONFIGURACIÓN:                                          ║
║   10. ⚙️  Cambiar fuente de datos (Local/API)            ║
║   11. 🚪 Salir del programa                              ║
╚══════════════════════════════════════════════════════════╝
```

### Notas de Uso

- **Modo Local**: Las modificaciones persisten en `src/base_de_datos/colegios.csv`
- **Modo API**: Se invocan los endpoints remotos:
  - `GET /colegios` - Listar todos los colegios (con filtros opcionales)
  - `GET /colegios/{id}` - Obtener un colegio por ID
  - `POST /colegios` - Crear un nuevo colegio
  - `PATCH /colegios/{id}` - Actualizar parcialmente un colegio
  - `DELETE /colegios/{id}` - Eliminar un colegio
- Los campos usados son directamente: `Provincia`, `Colegio`, `Cantidad de Estudiantes`, `Año de Creación` (sin mapeos ni conversiones)

---

## 📁 Estructura de Carpetas

```
TPI_Profesor_hualpa_com4/
├── aplicacion/
│   └── ejecutar.py              # Punto de entrada principal
├── src/
│   ├── base_de_datos/
│   │   └── colegios.csv         # Base de datos local (CSV)
│   └── funciones/
│       ├── __init__.py          # Paquete de funciones
│       ├── busqueda.py          # Búsquedas y filtros
│       ├── carga_datos.py       # CRUD local (agregar, editar, borrar)
│       ├── cliente_api.py       # Cliente HTTP (API remota)
│       ├── estadisticas.py      # Estadísticas generales
│       ├── inicializar.py       # Inicialización de CSV
│       ├── modo_api.py          # Lógica de modo API
│       ├── utilidades.py        # Utilidades (CSV, menús, normalización)
│       └── vista.py             # Visualización y ordenamiento
├── .vscode/
│   └── settings.json            # Configuración del IDE
├── pyrightconfig.json           # Configuración del analizador Python
└── README.md                    # Este archivo
```

---

## 🔄 Flujo de Datos

### Modo Local

1. **Lectura**: `utilidades.leer_csv()` → Lee `src/base_de_datos/colegios.csv` y retorna lista de diccionarios con estructura:
   ```python
   {
       "Provincia": "Córdoba",
       "Colegio": "Instituto San Martín",
       "Cantidad de Estudiantes": 520,
       "Año de Creación": 1985
   }
   ```

2. **CRUD en memoria**: Funciones en `carga_datos.py` (agregar, editar, borrar)

3. **Persistencia**: `utilidades.escribir_csv()` → Guarda cambios en `src/base_de_datos/colegios.csv`

### Modo API

1. **Cliente HTTP**: `cliente_api.py` realiza peticiones al servidor:
   - `estado_servidor()` → `GET /health`
   - `listar_colegios(q, provincia, ordenar_por, descendente)` → `GET /colegios`
   - `obtener_colegio(id)` → `GET /colegios/{id}`
   - `crear_colegio(...)` → `POST /colegios`
   - `actualizar_colegio_parcial(id, cambios)` → `PATCH /colegios/{id}`
   - `eliminar_colegio(id)` → `DELETE /colegios/{id}`

2. **Lógica de API**: `modo_api.py` contiene funciones que usan `cliente_api` y reutilizan funciones de `vista.py`, `busqueda.py`, `estadisticas.py` con los datos obtenidos de la API

3. **Esquema directo**: La API retorna y acepta datos con los campos reales del CSV (`Provincia`, `Colegio`, `Cantidad de Estudiantes`, `Año de Creación`) sin conversiones ni mapeos

---

## 📖 Guía de Uso

### Búsqueda por Nombre
Permite buscar colegios por nombre completo o parcial. La búsqueda es **insensible a mayúsculas/minúsculas** y **normaliza acentos** para mayor flexibilidad.

**Ejemplo:**
```
🔍 Ingrese el nombre del colegio a buscar: san martin
```

### Filtrar por Provincia
Filtra todos los colegios de una provincia específica.

**Ejemplo:**
```
🗺️  Ingrese la provincia: Córdoba
```

### Filtrar por Rango de Estudiantes
Filtra colegios según la cantidad de estudiantes (mínimo y máximo).

**Ejemplo:**
```
👥 Ingrese cantidad de estudiantes mínimo: 100
👥 Ingrese cantidad de estudiantes máximo: 500
```

### Filtrar por Rango de Año
Filtra colegios según el año de creación (mínimo y máximo).

**Ejemplo:**
```
📅 Ingrese año de creación mínimo: 1980
📅 Ingrese año de creación máximo: 2000
```

### Ordenar Colegios
Ordena la lista de colegios por cualquier campo disponible.

**Campos disponibles:**
- `Provincia`
- `Colegio`
- `Cantidad de Estudiantes`
- `Año de Creación`

**Ejemplo:**
```
🔢 Ingrese el campo por el cual ordenar: Provincia
⬇️  ¿Orden descendente? (s/n): n
```

### Estadísticas
Muestra estadísticas generales de todos los colegios:
- Colegio más antiguo y más nuevo
- Año promedio de creación
- Total y promedio de estudiantes
- Colegio con más y menos estudiantes
- Cantidad de colegios por provincia

### Agregar Colegio
Permite agregar un nuevo colegio al sistema. Valida que los campos obligatorios estén completos y que los valores numéricos sean válidos.

### Editar Colegio
Permite modificar los datos de un colegio existente. Puedes dejar campos en blanco para mantener el valor actual.

### Eliminar Colegio
Permite eliminar un colegio del sistema. Requiere confirmación antes de eliminar.

---

## 💡 Ejemplos de Uso

### Buscar por Nombre

**Entrada:**
```
🔍 Ingrese el nombre del colegio a buscar: San Martín
```

**Salida:**
```
✅ Colegios encontrados con el nombre 'San Martín': (1 encontrado(s))
  🏫 Instituto San Martín | Provincia: Córdoba | Estudiantes: 520 | Año: 1985
```

### Filtrar por Provincia

**Entrada:**
```
🗺️  Ingrese la provincia: Buenos Aires
```

**Salida:**
```
✅ Colegios en Buenos Aires: (3 encontrado(s))
  🏫 Colegio Nacional | Provincia: Buenos Aires | Estudiantes: 850 | Año: 1975
  🏫 Escuela Primaria N°1 | Provincia: Buenos Aires | Estudiantes: 320 | Año: 1990
  🏫 Instituto Técnico | Provincia: Buenos Aires | Estudiantes: 640 | Año: 1982
```

### Ver Estadísticas

**Salida:**
```
============================================================
📊 ESTADÍSTICAS GENERALES
============================================================
📅 Colegio más antiguo: Colegio Nacional (1975)
📅 Colegio más nuevo: Instituto Moderno (2010)
📅 Año promedio de creación: 1988

👥 Total de estudiantes: 15,450
👥 Promedio de estudiantes por colegio: 1,545
👥 Colegio con más estudiantes: Instituto Técnico (850)
👥 Colegio con menos estudiantes: Escuela Rural (120)

🏛️ Cantidad de colegios por provincia:
      - Buenos Aires: 3
      - Córdoba: 2
      - Santa Fe: 2
      - Mendoza: 1
============================================================
```

---

## 🔧 Solución de Problemas

### Error: "No se pudo importar módulos desde 'funciones'"

**Causa:** El IDE no encuentra los módulos.

**Solución:**
1. Verificar que estás ejecutando desde el directorio raíz del proyecto
2. Asegurarse de que `src/funciones/__init__.py` existe
3. Recargar la ventana del IDE: `Ctrl+Shift+P` → `Developer: Reload Window`

### Error: "No se pudo conectar al servidor"

**Causa:** El servidor API no está disponible o no hay conexión a internet.

**Solución:**
1. Verificar conexión a internet
2. Verificar que el servidor esté corriendo: `curl http://149.50.150.15:8020/health`
3. El sistema vuelve automáticamente a modo local si el servidor no está disponible

### Error: "No hay colegios en el archivo CSV local"

**Causa:** El archivo CSV está vacío o no existe.

**Solución:**
1. El sistema crea automáticamente el CSV si no existe
2. Agregar colegios usando la opción "Registrar nuevo colegio" del menú

### El CSV no se guarda correctamente

**Causa:** Problemas de permisos o codificación.

**Solución:**
1. Verificar permisos de escritura en `src/base_de_datos/`
2. El CSV se guarda con codificación UTF-8 con BOM (compatible con Windows)

---

## 👥 Participación de Integrantes

Este proyecto fue desarrollado de forma **colaborativa**, con roles distribuidos para asegurar claridad, funcionalidad y utilidad grupal:

### **Valentina**
Se encargó de:
- Organizar los datos y validar el archivo CSV
- Mejorar la interacción con el usuario
- Asegurar que el programa sea fácil de usar
- Redactar la documentación
- Pensar en cómo hacer que todo sea accesible para el grupo

### **Sofía**
Colaboró en:
- Las pruebas del sistema
- Revisar filtros, ordenamientos y estadísticas
- Proponer mejoras en los mensajes del menú
- Mejorar la validación de entradas
- Asegurar que el programa sea intuitivo y completo

### **Desarrollo Colaborativo**
Ambas participaron activamente en cada parte del desarrollo:
- Revisando el código
- Probando funciones
- Ajustando detalles

**Resultado:** Un programa pensado para el trabajo en grupo, con una lógica clara y una experiencia amigable.

---

## 🎥 Video Integrador

_[Espacio reservado para el enlace al video integrador]_

---

## 📝 Notas Adicionales

- **Código en español**: Todos los nombres de funciones, variables y mensajes están en español
- **Docstrings estilo Google**: Toda la documentación sigue el estilo Google para mantener consistencia
- **Compatibilidad**: Funciona en Windows, Linux y macOS
- **Validación robusta**: Maneja errores comunes como acentos, espacios y datos faltantes
- **Interfaz amigable**: Mensajes claros y fáciles de entender

---

## 📄 Licencia

Este proyecto es parte de un trabajo práctico integrador (TPI) para la materia de Programación 1.

---

## 🙏 Créditos

Desarrollado con ❤️ por Valentina y Sofía para el TPI de Programación 1.

---

**¡Gracias por usar el Sistema de Gestión y Consulta de Colegios!** 🏫✨
