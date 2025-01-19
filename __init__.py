from flask import Flask, render_template

def create_app():
    app = Flask(__name__)

    app.config.from_mapping(

        debug=True,
        SECRET_KEY='dev_esit'
    )

    @app.route('/')
    def index():
        return render_template('index.html')
    
    return app