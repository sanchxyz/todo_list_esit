from __init__ import create_app 
from flask_migrate import Migrate
from models import db


if __name__ == '__main__':
    app = create_app()
    Migrate = Migrate(app, db)
    app.run(host='0.0.0.0', port=5000, debug=True)
