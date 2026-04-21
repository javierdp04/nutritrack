# API REST

Base URL: `/api`. Todo en JSON. Auth por token (JWT o similar) en header `Authorization: Bearer <token>`.

## Auth

### POST /api/register
```json
{ "nombre": "...", "email": "...", "password": "..." }
```
200 → `{ "ok": true }` · 400 datos inválidos · 409 email existe.

### POST /api/login
```json
{ "email": "...", "password": "..." }
```
200 → `{ "token": "...", "rol": "estandar|admin" }` · 401 credenciales.

## Datos físicos

### GET /api/datos-fisicos
Devuelve los datos vigentes del usuario autenticado + TMB, GET y recomendación calórica.

### POST /api/datos-fisicos
```json
{
  "edad": 25, "peso": 75, "altura": 175,
  "genero": "hombre", "nivel_actividad": "medio",
  "objetivo": "perder"
}
```
200 → `{ "tmb": ..., "get": ..., "recomendacion_kcal": ... }` · 400 validación.

## Peso (histórico)

### POST /api/peso
```json
{ "peso": 75.3 }
```
Fecha se asigna en servidor.

### GET /api/peso
Devuelve array ordenado por fecha desc: `[{ "peso": 75.3, "fecha": "2026-04-22" }, ...]`.

## Dieta

### GET /api/dieta
Devuelve plan generado a partir de los datos físicos del usuario.
404 si no hay datos físicos → el frontend debe redirigir a CU-03.

## Recetas

### GET /api/recetas
Lista. Paginación opcional `?page=1&limit=20`.

### GET /api/recetas/:id
Detalle.

## Admin (requieren rol `admin`)

### GET /api/admin/usuarios
Lista.

### DELETE /api/admin/usuarios/:id
Borra usuario y datos asociados.

## Errores estándar

```json
{ "error": "mensaje legible", "code": "VALIDATION_ERROR" }
```

Códigos: `VALIDATION_ERROR`, `AUTH_REQUIRED`, `FORBIDDEN`, `NOT_FOUND`, `CONFLICT`, `INTERNAL`.
