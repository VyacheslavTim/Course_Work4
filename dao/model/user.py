from marshmallow import Schema, fields
from setup_db import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    name = db.Column(db.String)
    surname = db.Column(db.String)
    favorite_genre = db.Column(db.Integer, db.ForeignKey("genre.id"))


class UserSchema(Schema):
    id = fields.Integer()
    username = fields.String()
    password = fields.String()
    name = fields.String()
    surname = fields.String()
    favorite_genre = fields.String()



