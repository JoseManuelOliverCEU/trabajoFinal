from flask import Flask, jsonify
from flask_login import LoginManager, login_user, logout_user
from app.security import admin_required
from app.models import User

def make_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "test-secret"

    login_manager = LoginManager()
    login_manager.init_app(app)

    # user_loader obligatorio para que funcione current_user
    @login_manager.user_loader
    def load_user(user_id):
        # En unit tests podemos devolver un usuario “fake” por id
        # (no usamos DB)
        if user_id == "1":
            return User(id=1, username="admin", role="admin")
        if user_id == "2":
            return User(id=2, username="user", role="user")
        return None

    @app.get("/protected")
    @admin_required
    def protected():
        return jsonify(ok=True)

    return app

def test_admin_required_unauthenticated():
    app = make_app()
    client = app.test_client()

    r = client.get("/protected")
    assert r.status_code == 401
    assert r.get_json()["error"] == "login required"

def test_admin_required_user_forbidden():
    app = make_app()
    client = app.test_client()

    with app.test_request_context():
        login_user(User(id=2, username="user", role="user"))
        r = client.get("/protected")
        assert r.status_code == 403
        assert r.get_json()["error"] == "admin required"
        logout_user()

def test_admin_required_admin_ok():
    app = make_app()
    client = app.test_client()

    with app.test_request_context():
        login_user(User(id=1, username="admin", role="admin"))
        r = client.get("/protected")
        assert r.status_code == 200
        assert r.get_json()["ok"] is True
        logout_user()