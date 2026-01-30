from flask import Flask
from .routes import main_bp
from .models import init_db


def create_app():
    app = Flask(__name__)
    app.register_blueprint(main_bp)

    with app.app_context():
        init_db()

    return app
