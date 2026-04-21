# NutriTrack — Backend (Flask)

API REST en Flask + SQLAlchemy + SQLite. Autenticación JWT, contraseñas con bcrypt.

## Arranque

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# (opcional) cargar recetas + usuario admin
python seed.py

python app.py
```

Servidor en `http://localhost:5000`. El frontend Astro (puerto 4321) está permitido vía CORS.

## Variables de entorno

- `SECRET_KEY` — clave de firma JWT (por defecto `dev-secret-change-me`, cambiar en producción).
- `JWT_EXP_HOURS` — caducidad del token, por defecto 24.
- `DATABASE_URL` — SQLAlchemy URL. Por defecto `sqlite:///nutritrack.db`.
- `CORS_ORIGINS` — coma-separado, por defecto `http://localhost:4321`.

## Credenciales del seed

- Admin: `admin@nutritrack.local` / `admin1234` (cambiar antes de producción).

## Endpoints

Ver `docs/api.md`. Todo el contrato está implementado.
