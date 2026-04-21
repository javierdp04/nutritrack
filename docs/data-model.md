# Modelo de datos

Entidades a nivel conceptual. El motor concreto (MongoDB/MySQL/PostgreSQL) lo decide el equipo; mantener los nombres y relaciones consistentes.

## Usuario

| Campo | Tipo | Notas |
|---|---|---|
| id_usuario | ID | PK |
| nombre | string | 3–20 chars |
| email | string | único, formato válido |
| password_hash | string | bcrypt, nunca en claro |
| rol | enum | `estandar` \| `admin` \| `premium` |
| created_at | datetime | |

## DatosFisicos

Relación 1:1 con Usuario (último estado vigente). El histórico de peso va aparte.

| Campo | Tipo | Notas |
|---|---|---|
| id_usuario | FK | |
| edad | int | 15–100 |
| peso | float | kg, 30–250 |
| altura | int | cm, 120–220 |
| genero | enum | `hombre` \| `mujer` (necesario para TMB) |
| nivel_actividad | enum | `bajo` \| `medio` \| `alto` |
| objetivo | enum | `perder` \| `mantener` \| `ganar` |
| tmb | float | calculado |
| get | float | calculado |
| updated_at | datetime | |

## RegistroPeso

Histórico, N:1 con Usuario.

| Campo | Tipo | Notas |
|---|---|---|
| id | ID | PK |
| id_usuario | FK | |
| peso | float | kg, precisión 0.1 |
| fecha | date | auto al crear |

## Receta

| Campo | Tipo | Notas |
|---|---|---|
| id_receta | ID | PK |
| titulo | string | |
| ingredientes | text/list | |
| preparacion | text | |
| calorias | int | kcal por porción |

## Reglas

- Borrado de usuario → borrado en cascada de sus datos físicos y registros de peso.
- Recetas son globales, no pertenecen al usuario (en esta versión).
- No permitir guardar datos físicos con campos faltantes.
