from app.configs.database import db
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Lead(db.Model):
    id: int
    name: str
    email: str
    phone: str
    creation_date: datetime
    last_visit: datetime
    visits: int

    __tablename__ = 'leads'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    phone = db.Column(db.String(255), nullable=False, unique=True)
    creation_date = db.Column(db.DateTime(), nullable=False)
    last_visit = db.Column(db.DateTime(), nullable=True)
    visits = db.Column(db.Integer(), nullable=True)