from .extensions import db
from .models import Team

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
