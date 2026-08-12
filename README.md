# 📄 Herramientas de Documentos

Aplicación de escritorio para **automatizar el trabajo con documentos de Word (.docx)**. Integra tres utilidades en una sola interfaz limpia con pestañas:

- **📝 Reemplazar Variables** — Rellena plantillas reemplazando variables por valores definidos.
- **📄 Unir Documentos** — Combina varios documentos Word en uno solo, respetando el orden indicado.
- **📊 Excel → Word** — Genera uno o varios documentos Word a partir de un archivo Excel y una plantilla.

Construida con **Python + CustomTkinter**.

---

## ✨ Características

### 📝 Reemplazar Variables
- Selecciona una plantilla `.docx` y una ubicación de salida.
- Agrega, edita y elimina variables (nombre → valor) desde una tabla.
- Basado en **`docxtpl`**: soporta plantillas con sintaxis Jinja2 (`{{ variable }}`).
- Si no indicas ruta de salida, sobrescribe el documento original.

### 📄 Unir Documentos
- Agrega múltiples documentos Word y define el **orden de unión** (subir/bajar).
- Elimina o limpia documentos de la lista con confirmación.
- Indica la ruta de salida y genera el documento combinado con **`docxcompose`**.
- La unión corre en segundo plano con **indicador de progreso**, sin bloquear la interfaz.
- El botón "Unir" se **deshabilita** automáticamente cuando la lista está vacía.

### 📊 Excel → Word
- Selecciona un archivo Excel, una plantilla `.docx` y una carpeta de salida.
- Cada fila del Excel se usa como datos para generar un documento Word con la plantilla (un documento por fila).
- Basado en **`pandas`** y **`docxtpl`** (`excelOperaciones.generar_documentos`).
- La generación corre en segundo plano con **indicador de progreso**, sin bloquear la interfaz.
- El botón "Generar" se **deshabilita** automáticamente hasta que se seleccionen los tres archivos.

### 🎨 General
- Interfaz en pestañas con tema claro/oscuro automático (`System`).
- Barra de estado en cada pestaña con feedback de cada acción.
- Manejo de errores con diálogos informativos (sin cierres inesperados).

---

## 🚀 Instalación

### Requisitos
- Python **3.10+**
- `pip` / `venv`

### Pasos

```bash
# 1. Clona el repositorio
git clone https://github.com/tu-usuario/herramientas-documentos.git
cd herramientas-documentos

# 2. Crea y activa un entorno virtual
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
# .venv\Scripts\activate         # Windows

# 3. Instala las dependencias
pip install -r requirements.txt
```

### Ejecutar

```bash
python app.py
```

---

## 📦 Dependencias

| Paquete          | Uso                                    |
|------------------|----------------------------------------|
| `customtkinter`  | Interfaz gráfica moderna               |
| `tkinter`        | Widgets base (tablas, diálogos)        |
| `docxtpl`        | Reemplazo de variables en plantillas   |
| `docxcompose`    | Unión de documentos Word               |
| `python-docx`    | Lectura de documentos `.docx`          |
| `pandas`         | Lectura de archivos Excel              |

---

## 🗂️ Estructura del proyecto

```
.
├── app.py                    # Punto de entrada: ventana principal + pestañas
├── wordOperaciones.py        # Lógica de negocio (reemplazo y unión)
├── excelOperaciones.py       # Lógica de negocio (Excel → Word)
├── tabs/
│   ├── __init__.py
│   ├── tab_reemplazar.py     # Pestaña "Reemplazar Variables"
│   ├── tab_unir.py           # Pestaña "Unir Documentos"
│   └── tab_excel_word.py     # Pestaña "Excel → Word"
├── requirements.txt
└── README.md
```

---

## 📖 Cómo usar

### Reemplazar variables
1. Ve a la pestaña **📝 Reemplazar Variables**.
2. Pulsa **Examinar** para seleccionar la plantilla `.docx`.
3. (Opcional) Indica dónde guardar el resultado.
4. Pulsa **+ Agregar** y define cada variable (nombre y valor).
5. Pulsa **Generar Documento**.

> Las variables en la plantilla se escriben como `{{ nombre }}`. La app acepta además valores de distintos tipos (texto, números, fechas).

### Unir documentos
1. Ve a la pestaña **📄 Unir Documentos**.
2. Pulsa **＋ Agregar documentos** y selecciona uno o varios `.docx`.
3. Ordena la lista con **↑ Subir** / **↓ Bajar**.
4. Pulsa **Unir documentos**, elige la ruta de salida y espera el indicador de progreso.

### Excel → Word
1. Ve a la pestaña **📊 Excel → Word**.
2. Pulsa **Examinar** para seleccionar el archivo Excel (`.xlsx` / `.xls`).
3. Selecciona la plantilla `.docx` para los documentos.
4. Indica la carpeta de salida donde se guardarán los documentos.
5. Pulsa **Generar Documentos** y espera el indicador de progreso.

> Cada fila del Excel genera un documento `documento_N.docx` en la carpeta de salida. Las columnas del Excel deben coincidir con las variables de la plantilla (`{{ columna }}`).

---

## 🧩 Agregar una nueva pestaña

El proyecto está modularizado para facilitar su extensión:

1. Crea `tabs/tab_nueva.py` con una clase `ctk.CTkFrame` (mira las pestañas existentes como referencia).
2. Regístrala en `app.py`:

```python
from tabs.tab_nueva import NuevaTab

NuevaTab(tabview.add("🎯 Nueva Funcionalidad"))
```

---

## 📄 Licencia

Este proyecto es de uso libre. Sin restricciones de distribución o modificación.

---

*Hecho con 💙 en Python.*
