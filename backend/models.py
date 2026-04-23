"""
Este modulo se encarga de inicializar la base de datos y de definir las tablas que la componen
"""

from datetime import datetime, date
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Usuario(db.Model):
    __tablename__ = "usuarios"

    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.LargeBinary, nullable=False)
    rol = db.Column(db.String(16), nullable=False, default="estandar")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    datos_fisicos = db.relationship(
        "DatosFisicos", backref="usuario", uselist=False,
        cascade="all, delete-orphan",
    )
    registros_peso = db.relationship(
        "RegistroPeso", backref="usuario",
        cascade="all, delete-orphan", order_by="RegistroPeso.fecha.desc()",
    )

    def to_public(self):
        return {
            "id_usuario": self.id_usuario,
            "nombre": self.nombre,
            "email": self.email,
            "rol": self.rol,
            "created_at": self.created_at.isoformat(),
        }


class DatosFisicos(db.Model):
    __tablename__ = "datos_fisicos"

    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id_usuario"), primary_key=True)
    edad = db.Column(db.Integer, nullable=False)
    peso = db.Column(db.Float, nullable=False)
    altura = db.Column(db.Integer, nullable=False)
    genero = db.Column(db.String(8), nullable=False)
    nivel_actividad = db.Column(db.String(8), nullable=False)
    objetivo = db.Column(db.String(10), nullable=False)
    tmb = db.Column(db.Float, nullable=False)
    get = db.Column(db.Float, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "edad": self.edad,
            "peso": self.peso,
            "altura": self.altura,
            "genero": self.genero,
            "nivel_actividad": self.nivel_actividad,
            "objetivo": self.objetivo,
            "tmb": round(self.tmb, 1),
            "get": round(self.get, 1),
        }


class RegistroPeso(db.Model):
    __tablename__ = "registros_peso"

    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id_usuario"), nullable=False, index=True)
    peso = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.Date, nullable=False, default=date.today)

    def to_dict(self):
        return {"peso": self.peso, "fecha": self.fecha.isoformat()}


class Receta(db.Model):
    __tablename__ = "recetas"

    id_receta = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    ingredientes = db.Column(db.Text, nullable=False)
    preparacion = db.Column(db.Text, nullable=False)
    calorias = db.Column(db.Integer, nullable=False)

    def to_summary(self):
        ings = [i.strip() for i in self.ingredientes.split("\n") if i.strip()]
        return {
            "id_receta": self.id_receta,
            "titulo": self.titulo,
            "calorias": self.calorias,
            "ingredientes_resumen": ", ".join(ings[:4]),
        }

    def to_detail(self):
        return {
            "id_receta": self.id_receta,
            "titulo": self.titulo,
            "calorias": self.calorias,
            "ingredientes": [i.strip() for i in self.ingredientes.split("\n") if i.strip()],
            "preparacion": self.preparacion,
        }
