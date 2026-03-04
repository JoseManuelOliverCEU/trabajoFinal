from functools import wraps
from flask import jsonify
from flask_login import current_user

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({"error": "login required"}), 401
        if getattr(current_user, "role", None) != "admin":
            return jsonify({"error": "admin required"}), 403
        return fn(*args, **kwargs)
    return wrapper