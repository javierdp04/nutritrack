# Requisitos no funcionales

## Rendimiento

- Respuesta <2s en el 95% de operaciones.
- Soportar ≥50 usuarios simultáneos sin degradación.
- Capacidad mínima: 1.000 usuarios, 50.000 registros de peso.

## Disponibilidad

- ≥99% mensual, excluyendo mantenimiento programado.
- Máx. 7h/mes de caída no planificada.
- Accesible 24/7 vía navegador.

## Seguridad

- Autenticación email + contraseña obligatoria para rutas privadas.
- Contraseñas hasheadas con bcrypt (o equivalente seguro).
- Control de acceso basado en roles (estandar / admin).
- Base de datos no accesible directamente desde el cliente.
- Protección RGPD: datos personales cifrados y accesibles solo por el dueño o admin.
- Validación en cliente **y** servidor (nunca confiar solo en el cliente).

## Fiabilidad

- Sin pérdida de datos tras operación confirmada.
- Errores visibles al usuario + log interno.

## Mantenibilidad

- Separación estricta frontend / backend.
- Módulos con responsabilidad única.
- Nuevas funcionalidades (premium, APIs externas) deben poder añadirse sin romper lo existente.

## Usabilidad

- Interfaz clara y consistente.
- Mensajes de error y confirmación en toda operación crítica.
- Pensado para usuario con nivel técnico básico.

## Entorno

- Desarrollo: entorno local.
- Producción: servidor con acceso a base de datos (puede ser externo).
- Sin dependencia obligatoria de APIs externas en esta versión.
