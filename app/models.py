from datetime import datetime
from .extensions import db

class Team(db.Model):
    __tablename__ = "teams"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    city = db.Column(db.String(120), nullable=True)
    stadium = db.Column(db.String(120), nullable=True)
    founded_year = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "city": self.city,
            "stadium": self.stadium,
            "founded_year": self.founded_year,
            "created_at": self.created_at.isoformat(),
        }
