import os
from flask import Flask
from dotenv import load_dotenv

load_dotenv()


def create_app():
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
    )
    app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key")

    from .routes.quiz import bp as quiz_bp
    from .routes.words import bp as words_bp
    from .routes.settings import bp as settings_bp

    app.register_blueprint(quiz_bp)
    app.register_blueprint(words_bp)
    app.register_blueprint(settings_bp)

    return app
