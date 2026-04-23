"""
Módulo principal de la aplicación Flask que maneja las rutas y endpoints de la API.
"""

from flask import Flask, g, jsonify, request
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError

from config import Config
from models import DatosFisicos, RegistroPeso, Receta, Usuario, db
from auth_utils import (
    admin_required, generate_token, hash_password, login_required,
    verify_password,
)
from calculations import get as calc_get, plan_dieta, recomendacion_kcal, tmb as calc_tmb
from validators import (
    ValidationError, validate_datos_fisicos, validate_login,
    validate_peso, validate_register,
)


def create_app(config_class=Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)
    CORS(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}}, supports_credentials=False)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    @app.errorhandler(ValidationError)
    def _on_validation(err: ValidationError):
        return jsonify({"error": err.message, "code": "VALIDATION_ERROR"}), 400

    @app.errorhandler(404)
    def _on_404(_):
        return jsonify({"error": "Recurso no encontrado.", "code": "NOT_FOUND"}), 404

    @app.errorhandler(500)
    def _on_500(_):
        return jsonify({"error": "Error interno.", "code": "INTERNAL"}), 500

    # ---------- Auth ----------

    @app.post("/api/register")
    def register():
        nombre, email, password = validate_register(request.get_json(silent=True) or {})

        usuario = Usuario(
            nombre=nombre, email=email,
            password_hash=hash_password(password), rol="estandar",
        )
        db.session.add(usuario)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return jsonify({"error": "Email ya registrado.", "code": "CONFLICT"}), 409

        return jsonify({"ok": True}), 200

    @app.post("/api/login")
    def login():
        email, password = validate_login(request.get_json(silent=True) or {})
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario is None or not verify_password(password, usuario.password_hash):
            return jsonify({"error": "Credenciales incorrectas.", "code": "AUTH_REQUIRED"}), 401

        return jsonify({
            "token": generate_token(usuario),
            "rol": usuario.rol,
            "nombre": usuario.nombre,
        }), 200

    # ---------- Datos físicos ----------

    @app.get("/api/datos-fisicos")
    @login_required
    def get_datos_fisicos():
        df: DatosFisicos | None = g.usuario.datos_fisicos
        if df is None:
            return jsonify({"error": "Sin datos físicos.", "code": "NOT_FOUND"}), 404
        data = df.to_dict()
        data["recomendacion_kcal"] = recomendacion_kcal(df.get, df.objetivo)
        return jsonify(data)

    @app.post("/api/datos-fisicos")
    @login_required
    def save_datos_fisicos():
        data = validate_datos_fisicos(request.get_json(silent=True) or {})
        
        tmb_value = calc_tmb(data["genero"], data["peso"], data["altura"], data["edad"])
        get_value = calc_get(tmb_value, data["nivel_actividad"])
        kcal = recomendacion_kcal(get_value, data["objetivo"])

        df = g.usuario.datos_fisicos or DatosFisicos(id_usuario=g.usuario.id_usuario)
        df.edad = data["edad"]
        df.peso = data["peso"]
        df.altura = data["altura"]
        df.genero = data["genero"]
        df.nivel_actividad = data["nivel_actividad"]
        df.objetivo = data["objetivo"]
        df.tmb = tmb_value
        df.get = get_value
        db.session.add(df)
        db.session.commit()

        return jsonify({
            "tmb": round(tmb_value, 1),
            "get": round(get_value, 1),
            "recomendacion_kcal": kcal,
        })

    # ---------- Peso ----------

    @app.post("/api/peso")
    @login_required
    def crear_peso():
        peso = validate_peso(request.get_json(silent=True) or {})
        registro = RegistroPeso(id_usuario=g.usuario.id_usuario, peso=peso)
        db.session.add(registro)
        db.session.commit()
        return jsonify(registro.to_dict()), 201

    @app.get("/api/peso")
    @login_required
    def listar_peso():
        registros = g.usuario.registros_peso
        return jsonify([r.to_dict() for r in registros])

    # ---------- Dieta ----------

    @app.get("/api/dieta")
    @login_required
    def dieta():
        df: DatosFisicos | None = g.usuario.datos_fisicos
        if df is None:
            return jsonify({
                "error": "Faltan datos físicos.",
                "code": "NOT_FOUND",
            }), 404
        return jsonify(plan_dieta(df.get, df.objetivo))

    # ---------- Recetas ----------

    @app.get("/api/recetas")
    def listar_recetas():
        try:
            page = max(1, int(request.args.get("page", 1)))
            limit = min(100, max(1, int(request.args.get("limit", 20))))
        except ValueError:
            page, limit = 1, 20

        q = (request.args.get("q") or "").strip().lower()
        query = Receta.query
        if q:
            query = query.filter(Receta.titulo.ilike(f"%{q}%"))

        total = query.count()
        items = (
            query.order_by(Receta.id_receta.asc())
            .offset((page - 1) * limit).limit(limit).all()
        )
        return jsonify({
            "items": [r.to_summary() for r in items],
            "page": page, "limit": limit, "total": total,
        })

    @app.get("/api/recetas/<int:id_receta>")
    def detalle_receta(id_receta: int):
        r = Receta.query.get(id_receta)
        if r is None:
            return jsonify({"error": "Receta no encontrada.", "code": "NOT_FOUND"}), 404
        return jsonify(r.to_detail())

    # ---------- Admin ----------

    @app.get("/api/admin/usuarios")
    @admin_required
    def admin_listar_usuarios():
        usuarios = Usuario.query.order_by(Usuario.created_at.desc()).all()
        return jsonify([u.to_public() for u in usuarios])

    @app.delete("/api/admin/usuarios/<int:id_usuario>")
    @admin_required
    def admin_borrar_usuario(id_usuario: int):
        if id_usuario == g.usuario.id_usuario:
            return jsonify({
                "error": "Un admin no puede eliminarse a sí mismo.",
                "code": "FORBIDDEN",
            }), 403
        usuario = Usuario.query.get(id_usuario)
        if usuario is None:
            return jsonify({"error": "Usuario no encontrado.", "code": "NOT_FOUND"}), 404
        db.session.delete(usuario)
        db.session.commit()
        return jsonify({"ok": True})

    return app


if __name__ == "__main__":
    create_app().run(debug=True, port=5000)
