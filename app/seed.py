import os
from .extensions import db
from .models import Team, User

PL_2526 = [
    "Arsenal",
    "Aston Villa",
    "AFC Bournemouth",
    "Brentford",
    "Brighton & Hove Albion",
    "Burnley",
    "Chelsea",
    "Crystal Palace",
    "Everton",
    "Fulham",
    "Leeds United",
    "Liverpool",
    "Manchester City",
    "Manchester United",
    "Newcastle United",
    "Nottingham Forest",
    "Sunderland",
    "Tottenham Hotspur",
    "West Ham United",
    "Wolverhampton Wanderers",
]

def seed_teams():
    created = 0
    for name in PL_2526:
        if not Team.query.filter_by(name=name).first():
            db.session.add(Team(name=name))
            created += 1
    db.session.commit()
    return created

def seed_users():
    admin_username = os.getenv("ADMIN_USERNAME")
    admin_password = os.getenv("ADMIN_PASSWORD")

    user_username = os.getenv("USER_USERNAME")
    user_password = os.getenv("USER_PASSWORD")

    if not admin_password or not user_password:
        raise RuntimeError("Usuario y Contraseña incorrectos")

    # Admin
    if not User.query.filter_by(username=admin_username).first():
        admin = User(username=admin_username, role="admin")
        admin.set_password(admin_password)
        db.session.add(admin)

    # Usuario normal
    if not User.query.filter_by(username=user_username).first():
        user = User(username=user_username, role="user")
        user.set_password(user_password)
        db.session.add(user)

    db.session.commit()