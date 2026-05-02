"""
Módulo de validación de datos de entrada para formularios y API.
"""

import re
from datetime import date

EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")

GENEROS = {"hombre", "mujer"}
NIVELES = {"bajo", "medio", "alto"}
OBJETIVOS = {"perder", "mantener", "ganar"}


class ValidationError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


def _require(cond: bool, msg: str):
    if not cond:
        raise ValidationError(msg)


def validate_register(data: dict):
    nombre = (data.get("nombre") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    _require(3 <= len(nombre) <= 20, "El nombre debe tener entre 3 y 20 caracteres.")
    _require(bool(EMAIL_RE.match(email)), "Email no válido.")
    _require(len(password) >= 8, "La contraseña debe tener al menos 8 caracteres.")
    return nombre, email, password


def validate_login(data: dict):
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    _require(bool(email) and bool(password), "Email y contraseña son obligatorios.")
    return email, password


def validate_datos_fisicos(data: dict):
    try:
        fecha_str = (data.get("fecha_nacimiento") or "").strip()
        fecha_nacimiento = date.fromisoformat(fecha_str)
        peso = float(data["peso"])
        altura = int(data["altura"])
    except (KeyError, TypeError, ValueError):
        raise ValidationError("Datos inválidos.")

    genero = (data.get("genero") or "").strip().lower()
    nivel = (data.get("nivel_actividad") or "").strip().lower()
    objetivo = (data.get("objetivo") or "").strip().lower()

    hoy = date.today()
    edad = hoy.year - fecha_nacimiento.year - (
        (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day)
    )

    _require(fecha_nacimiento <= hoy, "La fecha de nacimiento no puede ser futura.")
    _require(15 <= edad <= 100, "La edad calculada debe estar entre 15 y 100 años.")
    _require(30 <= peso <= 250, "Peso fuera de rango (30–250 kg).")
    _require(120 <= altura <= 220, "Altura fuera de rango (120–220 cm).")
    _require(genero in GENEROS, "Género inválido.")
    _require(nivel in NIVELES, "Nivel de actividad inválido.")
    _require(objetivo in OBJETIVOS, "Objetivo inválido.")

    return {
        "fecha_nacimiento": fecha_nacimiento, "edad": edad,
        "peso": round(peso, 1), "altura": altura,
        "genero": genero, "nivel_actividad": nivel, "objetivo": objetivo,
    }


def validate_peso(data: dict) -> float:
    try:
        peso = float(data["peso"])
    except (KeyError, TypeError, ValueError):
        raise ValidationError("Peso inválido.")
    _require(30 <= peso <= 250, "Peso fuera de rango (30–250 kg).")
    return round(peso, 1)
