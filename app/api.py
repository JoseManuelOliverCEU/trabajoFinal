from flask import Blueprint, jsonify, request
from .extensions import db
from .models import Team
from flask_login import login_required
from .security import admin_required

api_bp = Blueprint("api", __name__, url_prefix="/api")

@api_bp.get("/health")
def health():
    return jsonify(status="ok")

@api_bp.get("/teams")
@login_required
def list_teams():
    teams = Team.query.order_by(Team.name.asc()).all()
    return jsonify([t.to_dict() for t in teams])

@api_bp.get("/teams/<int:team_id>")
def get_team(team_id):
    t = Team.query.get_or_404(team_id)
    return jsonify(t.to_dict())

@api_bp.post("/teams")
@admin_required
def create_team():
    data = request.get_json(force=True)

    name = (data.get("name") or "").strip()
    if not name:
        return jsonify(error="name is required"), 400

    if Team.query.filter_by(name=name).first():
        return jsonify(error="team already exists"), 409

    t = Team(
        name=name,
        city=(data.get("city") or "").strip() or None,
        stadium=(data.get("stadium") or "").strip() or None,
        founded_year=data.get("founded_year") or None,
    )
    db.session.add(t)
    db.session.commit()
    return jsonify(t.to_dict()), 201

@api_bp.put("/teams/<int:team_id>")
@admin_required
def update_team(team_id):
    t = Team.query.get_or_404(team_id)
    data = request.get_json(force=True)

    if "name" in data:
        name = (data.get("name") or "").strip()
        if not name:
            return jsonify(error="name cannot be empty"), 400
        # evitar choque con otro equipo
        existing = Team.query.filter(Team.name == name, Team.id != team_id).first()
        if existing:
            return jsonify(error="another team already has that name"), 409
        t.name = name

    if "city" in data:
        t.city = (data.get("city") or "").strip() or None
    if "stadium" in data:
        t.stadium = (data.get("stadium") or "").strip() or None
    if "founded_year" in data:
        t.founded_year = data.get("founded_year") or None

    db.session.commit()
    return jsonify(t.to_dict())

@api_bp.delete("/teams/<int:team_id>")
@admin_required
def delete_team(team_id):
    t = Team.query.get_or_404(team_id)
    db.session.delete(t)
    db.session.commit()
    return jsonify(deleted=True, id=team_id)
