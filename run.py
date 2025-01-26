"""
Punto de entrada para ejecutar la aplicación Flask.
Este archivo inicializa la aplicación y la ejecuta en un servidor local.
"""

from __init__ import create_app  # Importar la función create_app desde __init__.py
from flask_migrate import Migrate  # Importar la extensión Migrate para manejar migraciones de la base de datos
from models import db  # Importar la instancia de la base de datos

# Verificar si este archivo es el punto de entrada principal
if __name__ == '__main__':
    # Crear la aplicación Flask utilizando la función create_app
    app = create_app()

    # Configurar la extensión Migrate para manejar migraciones de la base de datos
    Migrate(app, db)

    # Ejecutar la aplicación en un servidor local
    # - host='0.0.0.0': La aplicación estará disponible en todas las interfaces de red.
    # - port=5000: La aplicación escuchará en el puerto 5000.
    # - debug=True: Habilita el modo de depuración (útil durante el desarrollo).
    app.run(host='0.0.0.0', port=5000, debug=True)