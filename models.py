from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


#Creating model table for our CRUD database
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def create(self):
        db.session.add(self)
        db.session.commit()

    def update(self, values):
        for key, value in values.items():
            setattr(self, key, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Tache(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    date_echeance = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('taches', lazy=True))

    def __init__(self, titre, description, date_echeance, user_id):
        self.titre = titre
        self.description = description
        self.date_echeance = date_echeance
        self.user_id = user_id

    def create(self):
        db.session.add(self)
        db.session.commit()

    def update(self, values):
        for key, value in values.items():
            setattr(self, key, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()