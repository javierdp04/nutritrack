"""
Este modulo contiene diferentes funciones para facilitar la autentificaction
"""
from datetime import datetime, timedelta, timezone
from functools import wraps

import bcrypt
import jwt
from flask import current_app, g, jsonify, request

from models import Usuario


def hash_password(plain: str) -> bytes:
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt())


def verify_password(plain: str, hashed: bytes) -> bool:
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed)
    except ValueError:
        return False


def generate_token(usuario: Usuario) -> str:
    payload = {
        "sub": usuario.id_usuario,
        "rol": usuario.rol,
        "exp": datetime.now(tz=timezone.utc)
        + timedelta(hours=current_app.config["JWT_EXP_HOURS"]),
    }
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")


def _error(message: str, code: str, status: int):
    return jsonify({"error": message, "code": code}), status


def _decode():
    header = request.headers.get("Authorization", "")
    if not header.startswith("Bearer "):
        return None, _error("Falta token de autenticación.", "AUTH_REQUIRED", 401)
    token = header.removeprefix("Bearer ").strip()
    try:
        payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None, _error("Token expirado.", "AUTH_REQUIRED", 401)
    except jwt.InvalidTokenError:
        return None, _error("Token inválido.", "AUTH_REQUIRED", 401)

    usuario = Usuario.query.get(payload.get("sub"))
    if usuario is None:
        return None, _error("Usuario no encontrado.", "AUTH_REQUIRED", 401)
    return usuario, None


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        usuario, err = _decode()
        if err:
            return err
        g.usuario = usuario
        return fn(*args, **kwargs)

    return wrapper


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        usuario, err = _decode()
        if err:
            return err
        if usuario.rol != "admin":
            return _error("Se requieren privilegios de administrador.", "FORBIDDEN", 403)
        g.usuario = usuario
        return fn(*args, **kwargs)

    return wrapper
