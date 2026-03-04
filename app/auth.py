from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from .models import User
from .extensions import db

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    if not username or not password:
        return jsonify({"error": "username and password required"}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "invalid credentials"}), 401

    login_user(user)
    return jsonify({"status": "ok", "role": user.role, "username": user.username})

@auth_bp.post("/logout")
@login_required
def logout():
    logout_user()
    return jsonify({"status": "ok"})

@auth_bp.get("/me")
def me():
    if not current_user.is_authenticated:
        return jsonify({"authenticated": False}), 200
    return jsonify({
        "authenticated": True,
        "username": current_user.username,
        "role": current_user.role
    })