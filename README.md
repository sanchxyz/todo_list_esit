# TODO List   

Este es un proyecto educativo que implementa una aplicación de lista de tareas utilizando Flask como framework principal. Su propósito es demostrar el uso de bases de datos relacionales, autenticación de usuarios, y organización de rutas con Blueprints.

## Enlace al Proyecto Desplegado

Puedes acceder al proyecto desplegado en Railway haciendo clic en el siguiente enlace:

[TODO List ESIT en Railway](https://todolistesit-production.up.railway.app)

---

## Descripción del Proyecto

El proyecto **TODO List ESIT** permite a los usuarios:

- Registrarse y autenticarse mediante un sistema básico de gestión de usuarios.
- Crear, listar y eliminar tareas asociadas a su cuenta.
- Verificar el estado de autenticación y asegurar que cada usuario tenga acceso solo a sus propias tareas.

La aplicación está diseñada para fines educativos y no cuenta con medidas de seguridad avanzadas, como el cifrado de datos sensibles en la base de datos o la protección contra ataques CSRF. **No debe usarse en un entorno de producción.**

---

## Tecnologías Utilizadas

- **Backend**: Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-Session
- **Base de Datos**: SQLite (local)
- **Frontend**: HTML, Jinja2
- **Despliegue**: Railway

---

## Clonar y Ejecutar Localmente

Sigue estos pasos para clonar y ejecutar el proyecto en tu entorno local:

### Requisitos Previos

- Python 3.10 o superior
- Pip (administrador de paquetes de Python)
- Git

### Pasos

1. **Clona el repositorio**:

   ```bash
   git clone git@github.com:sanchxyz/todo_list_esit.git
   cd todo_list_esit
   ```

2. **Crea un entorno virtual**:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # En Windows: .venv\Scripts\activate
   ```

3. **Instala las dependencias**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Inicia la aplicación**:

   ```bash
   python run.py
   ```

   Por defecto, la aplicación estará disponible en [http://127.0.0.1:5000](http://127.0.0.1:5000).

---

## Notas Importantes

- El archivo de configuración `.flaskenv` debe estar presente en la raíz del proyecto para establecer las variables de entorno necesarias.
- El proyecto utiliza una base de datos SQLite, que es adecuada para desarrollo local y pruebas, pero no para entornos de producción.
- Si decides modificar el proyecto o desplegarlo en un entorno diferente, considera actualizar las configuraciones de la base de datos y los secretos de la aplicación.
- Comandos para configurar las variables de entorno de Flask:
  ```bash
  export FLASK_APP=run.py
  export PYTHONPATH=$(pwd)
  ```

---

Contribuciones y sugerencias son bienvenidas. Si tienes alguna duda o encuentras un problema, no dudes en crear un issue en el repositorio.

