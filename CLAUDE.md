# NutriTrack — Contexto del proyecto

Aplicación web gratuita de seguimiento nutricional. Proyecto académico (Ingeniería del Software, Grupo A2 Alpha).

## Stack

- **Frontend**: Astro + HTML + CSS + JavaScript
- **Backend**: Flask (Python) — API REST
- **Comunicación**: HTTP + JSON, modelo cliente-servidor
- **Auth**: email + contraseña, hash con bcrypt, control de roles (usuario/admin)
- **Sin APIs externas** en esta versión

## Qué hace

El usuario introduce datos físicos (edad, peso, altura, actividad, objetivo), el sistema calcula TMB y GET, y le devuelve una recomendación calórica + dieta + seguimiento de peso histórico + recetas.

## Roles

1. **Usuario estándar** — registro, datos físicos, dieta, seguimiento peso, recetas
2. **Administrador** — gestiona usuarios y modera recetas
3. **Premium** — futuro, no implementar

## Estructura sugerida del repo

```
/frontend    → proyecto Astro
/backend     → app Flask (API REST)
/docs        → documentación del proyecto
```

## Archivos de referencia (leer según tarea)

- `docs/requirements.md` — requisitos funcionales, casos de uso, actores
- `docs/formulas.md` — fórmulas nutricionales (TMB, GET, ajuste objetivo)
- `docs/data-model.md` — entidades y esquema de base de datos
- `docs/api.md` — endpoints REST
- `docs/ui-screens.md` — pantallas, inputs, validaciones
- `docs/nfr.md` — requisitos no funcionales (rendimiento, seguridad, etc.)

## Reglas duras

- No generar recomendaciones si el usuario no ha introducido datos físicos (CU-04 depende de CU-03).
- Validar en cliente **y** en servidor.
- Contraseñas siempre hasheadas (bcrypt), nunca en claro.
- Rutas privadas protegidas por autenticación.
- Registro histórico de peso: no sobrescribir, se acumula.

## Prioridades de casos de uso

- **P0 (esencial)**: registro, login, datos físicos, consultar dieta, registrar peso, consultar progreso
- **P1 (importante)**: consultar recetas, gestión de usuarios (admin)

## Convenciones del equipo

- Javier trabaja en Linux (Pop!_OS), VS Code.
- Código en español para identificadores de dominio (usuario, peso, dieta) está bien; mantener consistencia.
- Commits y PRs en español.
