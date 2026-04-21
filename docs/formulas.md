# Fórmulas nutricionales

## TMB (Mifflin-St Jeor)

```
Hombres: TMB = 10*peso_kg + 6.25*altura_cm − 5*edad + 5
Mujeres: TMB = 10*peso_kg + 6.25*altura_cm − 5*edad − 161
```

## GET

```
GET = TMB * factor_actividad
```

Factores:
- Bajo: 1.2
- Medio: 1.55
- Alto: 1.725

## Ajuste por objetivo

- Perder peso: `GET − 300..500 kcal` (usar −500 por defecto)
- Mantener: `GET`
- Ganar masa: `GET + 300..500 kcal` (usar +400 por defecto)

## Unidades

- Peso: kg (precisión 0.1)
- Altura: cm (entero)
- Edad: años (entero)
- Energía: kcal (entero en salida al usuario)

## Validación de rangos

- Edad: 15–100
- Peso: 30–250 kg
- Altura: 120–220 cm

Cualquier valor fuera de rango o negativo → error de validación antes de calcular.
