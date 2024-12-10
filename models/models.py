from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

db = SQLAlchemy()

def generate_salt():
    return os.urandom(16).hex()

class Departamento(db.Model):
    __tablename__ = 'departamentos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False, unique=True)

    def as_dict(self):
        return {
            'id': self.id,
            'nome': self.nome
        }
    
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    salt = db.Column(db.String(32), nullable=False)
    senha_hash = db.Column(db.String(128), nullable=False)
    tipo_usuario = db.Column(db.String(50), nullable=False)
    departamento_id = db.Column(db.Integer, db.ForeignKey('departamentos.id'), nullable=True)

    departamento = db.relationship('Departamento', backref='usuarios')

    def set_password(self, senha):
        self.salt = generate_salt()
        self.senha_hash = generate_password_hash(senha + self.salt)

    def check_password(self, senha):
        return check_password_hash(self.senha_hash, senha + self.salt)

    def as_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'tipo_usuario': self.tipo_usuario,
            'departamento': self.departamento.nome if self.departamento else None
        }