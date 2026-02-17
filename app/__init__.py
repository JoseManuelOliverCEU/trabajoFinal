from flask import Flask
from .config import Config
from .extensions import db, migrate
from .api import api_bp
from .dashapp import init_dash
from .seed import seed_teams

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(api_bp)
    init_dash(app)

    @app.cli.command("seed")
    def seed_command():
        n = seed_teams()
        print(f"Seed OK. Created: {n}")

    return app
