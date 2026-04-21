# NutriTrack

Aplicación web de seguimiento nutricional. Proyecto académico — Ingeniería del Software, Grupo A2 Alpha.

## Stack

- **Frontend**: Astro (HTML/CSS/JS/TS) — `frontend` corriendo en `/`
- **Backend**: Flask + SQLAlchemy + SQLite — API REST en `/backend`
- **Auth**: JWT + bcrypt
- **Base de datos**: SQLite (archivo local, fácil cambiar vía `DATABASE_URL`)

## Estructura

```
/src           → Astro (pantallas + componentes + scripts)
/public        → assets estáticos
/backend       → API Flask
/docs          → documentación del proyecto
```

## Arranque rápido

### 1. Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python seed.py            # carga recetas + admin de ejemplo
python app.py             # arranca en http://localhost:5000
```

Credenciales del admin tras `seed.py`: `admin@nutritrack.local` / `admin1234`.

### 2. Frontend

```bash
npm install
npm run dev               # arranca en http://localhost:4321
```

## Pantallas

Públicas:
- `/` — landing
- `/register` — registro (CU-01)
- `/login` — login (CU-02)

Privadas (requieren sesión):
- `/dashboard` — resumen diario
- `/datos-fisicos` — formulario + cálculo TMB/GET (CU-03)
- `/dieta` — plan calórico + reparto por comidas (CU-04)
- `/peso` — registro, histórico, gráfico (CU-05/06)
- `/recetas` y `/recetas/detail?id=X` — lista y detalle (CU-07)

Solo admin:
- `/admin/usuarios` — gestión de usuarios (CU-08)

## Cumplimiento de la documentación

- Validación en cliente **y** servidor.
- Contraseñas con bcrypt.
- Protección por JWT en `Authorization: Bearer <token>`.
- Borrado de usuario en cascada (datos físicos + histórico de peso).
- Fórmulas TMB/GET/ajuste según `docs/formulas.md`.
- Rangos validados según `docs/requirements.md`.
