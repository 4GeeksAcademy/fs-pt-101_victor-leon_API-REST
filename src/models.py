from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    favorites = db.relationship('Favorite', backref='user', lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
        }

class Nationality(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String(250))

    def serialize(self):
        return {
            "id": self.id,
            "country": self.country,
            "description": self.description
        }

class Stand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    ability = db.Column(db.String(250))
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), unique=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "ability": self.ability,
            "character_id": self.character_id
        }

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer)
    nationality_id = db.Column(db.Integer, db.ForeignKey('nationality.id'))
    stand = db.relationship('Stand', uselist=False, backref='character')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "nationality": self.nationality.country if self.nationality else None,
            "stand": self.stand.serialize() if self.stand else None
        }

    nationality = db.relationship('Nationality', backref='characters')

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    nationality_id = db.Column(db.Integer, db.ForeignKey('nationality.id'))

    character = db.relationship('Character')
    nationality = db.relationship('Nationality')

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character": self.character.serialize() if self.character else None,
            "nationality": self.nationality.serialize() if self.nationality else None
        }
