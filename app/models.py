from app import db
from flask import current_app
from flask_bcrypt import Bcrypt
import os

import jwt
from datetime import datetime, timedelta

class User(db.Model):
    """This class defines the users table """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    candidate = db.relationship('Candidate', order_by='Candidate.id', cascade="all, delete-orphan")

    def __init__(self, email, password):
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode()

    def password_is_valid(self, password):
        return Bcrypt().check_password_hash(self.password, password)

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def generate_token(self, user_id):
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=120),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            jwt_string = jwt.encode(
                payload,
                current_app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
            return jwt_string

        except Exception as e:
            return ("Error in generating token in models {}".format(e))

    @staticmethod
    def decode_token(token):
        """Decodes the access token from the Authorization header."""
        try:
            payload = jwt.decode(token, current_app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return ("Expired token. Please login to get a new token")
        except jwt.InvalidTokenError:
            return ("Invalid token. Please register or login")

class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    enrolement_no = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    address = db.Column(db.String(80))
    degree_name = db.Column(db.String(80))
    admission_status = db.Column(db.Boolean)
    created_by = db.Column(db.Integer, db.ForeignKey(User.id))

    def __init__(self, enrolement_no, name, address, degree_name, admission_status):
        self.enrolement_no = enrolement_no
        self.name = name
        self.address = address
        self.degree_name = degree_name
        self.admission_status = admission_status

    def save(self):
        """Save a candidate.
        This applies for both creating a new candidate
        and updating an existing onupdate
        """
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all(user_id):
        """This method gets all the candidates for a given user."""
        return Candidate.query.filter_by(created_by=user_id)

    def delete(self):
        """Deletes a given candidate."""
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        """Return a representation of a candidate instance."""
        return "<Candidate: {}>".format(self.enrolement_no)