from flask import Flask
from .config import Config
from .extensions import db, migrate, login_manager
from .api import api_bp
from .auth import auth_bp
from .dashapp import init_dash
from .models import User
from .seed import seed_teams, seed_users


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # 👇 IMPORTANTE: login view (si algún endpoint usa @login_required)
    login_manager.login_view = "auth.login"

    # 👇 IMPORTANTE: user_loader para Flask-Login (ESTO ARREGLA TU ERROR)
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Blueprints
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(auth_bp)

    # Dash
    init_dash(app)

    # CLI seed
    @app.cli.command("seed")
    def seed_command():
        n = seed_teams()
        seed_users()
        print(f"Seed OK. Teams created: {n}")

    return app