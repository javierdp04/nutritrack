# Pantallas (frontend Astro)

## 1. Registro — `/register`
Campos: nombre, email, contraseña. Validación en cliente antes de POST. Link a login.

## 2. Login — `/login`
Campos: email, contraseña. Link a "¿Olvidaste tu contraseña?" (placeholder, funcionalidad futura).

## 3. Dashboard — `/` (protegida)
Muestra:
- Saludo + nombre del usuario
- Recomendación calórica diaria (kcal)
- Objetivo activo
- Peso actual + progreso hacia meta (barra)
- Energía consumida hoy (si aplica)
- Accesos directos: Plan de comidas, Seguimiento de peso, Recetas
- Gráfico resumen semanal

## 4. Datos físicos — `/datos-fisicos` (protegida)
Formulario con edad, peso, altura, género, nivel actividad, objetivo.
Al enviar muestra TMB, GET y recomendación calórica.

## 5. Seguimiento de peso — `/peso` (protegida)
- Input: peso actual + botón "Registrar"
- Histórico en tabla
- Gráfico de evolución (línea)
- Diferencia vs último peso y total perdido/ganado

## 6. Recetas — `/recetas` (protegida)
- Grid de tarjetas con foto, título, kcal, ingredientes resumidos
- Buscador
- Detalle al clicar: ingredientes completos, preparación, macros

## 7. Admin — `/admin/usuarios` (solo rol admin)
Tabla de usuarios con acciones (ver, eliminar).

## Reglas de UI

- Unidades: kg, cm, kcal.
- Mensajes de error claros en cada input y a nivel de formulario.
- Mensajes de confirmación tras acciones críticas (registro, guardar peso, etc.).
- Rutas protegidas redirigen a `/login` si no hay sesión.
- Si `/dieta` se accede sin datos físicos → redirigir a `/datos-fisicos` con aviso.
- Tiempo de respuesta objetivo: <2s en el 95% de acciones.
