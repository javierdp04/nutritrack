# Requisitos y casos de uso

## Actores

- **Usuario estándar** — nivel técnico básico, usa la web para seguimiento nutricional.
- **Administrador** — gestiona usuarios y modera contenido.
- **Premium** (futuro) — no implementar todavía.

## Casos de uso

### CU-01 Registrarse [P0]
- Inputs: nombre (3–20 chars), email válido, contraseña (mín. 8 chars).
- Valida formato → comprueba email no duplicado → crea cuenta.
- Errores: email ya registrado, datos inválidos.

### CU-02 Iniciar sesión [P0]
- Inputs: email, contraseña.
- Valida credenciales → devuelve sesión/token → redirige al dashboard.
- Admin accede al mismo dashboard pero con vista de usuarios.
- Error: credenciales incorrectas.

### CU-03 Introducir datos físicos [P0]
- Precondición: sesión iniciada.
- Inputs: edad (15–100), peso (30–250 kg), altura (120–220 cm), actividad (bajo/medio/alto), objetivo (perder/mantener/ganar).
- Valida → calcula TMB y GET → guarda.
- Error: datos inválidos.

### CU-04 Consultar plan de dieta [P0]
- Precondición: CU-03 completado.
- Sistema calcula dieta a partir de GET ajustado por objetivo → muestra.
- Error: faltan datos físicos → redirigir a CU-03.

### CU-05 Registrar peso [P0]
- Precondición: sesión iniciada.
- Inputs: peso actual (kg, precisión 0.1). Fecha automática.
- Valida → guarda en histórico (no sobrescribe).

### CU-06 Consultar progreso [P0]
- Precondición: al menos un registro de peso.
- Muestra histórico + gráfico de evolución + diferencia vs peso anterior.

### CU-07 Consultar recetas [P1]
- Muestra lista de recetas con título, calorías, ingredientes, preparación.

### CU-08 Gestionar usuarios [P1, admin]
- Admin lista y elimina usuarios.

## Restricciones clave

- Web only. No móvil nativo en esta versión.
- Navegador moderno + conexión a internet.
- No integrar APIs externas todavía.
