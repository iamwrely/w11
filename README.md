# Gestor de Clientes

Aplicación web sencilla construida con Flask para administrar información básica de clientes: crear, editar, buscar y eliminar registros. Utiliza SQLite como base de datos local para un despliegue rápido y sin configuraciones complejas.

## Requisitos

- Python 3.10 o superior
- `pip` para instalar dependencias

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate  # En Windows usa `.venv\\Scripts\\activate`
pip install -r requirements.txt
```

## Ejecución

Inicializa la base de datos (se creará el archivo `clients.db` en la carpeta del proyecto) y ejecuta el servidor de desarrollo:

```bash
flask --app app.py --debug run
```

Abre <http://127.0.0.1:5000> en tu navegador para acceder al gestor de clientes.

## Funcionalidades

- Listado de clientes con búsqueda por nombre, correo, teléfono o empresa.
- Formulario para crear y editar clientes con validaciones básicas.
- Eliminación de clientes con confirmación en el navegador.
- Diseño responsive sencillo con estilos CSS personalizados.

## Estructura del proyecto

```
.
├── app.py              # Aplicación Flask y rutas principales
├── requirements.txt    # Dependencias necesarias
├── static/
│   └── style.css       # Estilos de la interfaz
└── templates/
    ├── base.html       # Plantilla base
    ├── client_form.html# Formulario para crear/editar
    └── index.html      # Listado principal de clientes
```

## Personalización

- Cambia el valor de `SECRET_KEY` en `app.py` por uno propio para habilitar sesiones seguras.
- Puedes extender el modelo `Client` con nuevos campos (por ejemplo, dirección o fecha de seguimiento) y añadirlos a los formularios.
- Integra autenticación, exportación de datos u otras funciones según tus necesidades.
