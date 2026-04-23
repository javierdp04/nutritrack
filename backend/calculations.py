"""
Este modulo contiene funciones que facilitan el calculo de ciertas metricas
"""

ACTIVITY_FACTORS = {"bajo": 1.2, "medio": 1.55, "alto": 1.725}
OBJETIVO_AJUSTE = {"perder": -500, "mantener": 0, "ganar": 400}


def tmb(genero: str, peso: float, altura: int, edad: int) -> float:
    base = 10 * peso + 6.25 * altura - 5 * edad
    return base + 5 if genero == "hombre" else base - 161


def get(tmb_value: float, nivel_actividad: str) -> float:
    return tmb_value * ACTIVITY_FACTORS[nivel_actividad]


def recomendacion_kcal(get_value: float, objetivo: str) -> int:
    return int(round(get_value + OBJETIVO_AJUSTE[objetivo]))


def plan_dieta(get_value: float, objetivo: str) -> dict:
    kcal = recomendacion_kcal(get_value, objetivo)
    return {
        "recomendacion_kcal": kcal,
        "objetivo": objetivo,
        "reparto": {
            "desayuno": int(round(kcal * 0.25)),
            "almuerzo": int(round(kcal * 0.35)),
            "merienda": int(round(kcal * 0.15)),
            "cena": int(round(kcal * 0.25)),
        },
        "macros": {
            "proteinas_g": int(round(kcal * 0.30 / 4)),
            "carbohidratos_g": int(round(kcal * 0.45 / 4)),
            "grasas_g": int(round(kcal * 0.25 / 9)),
        },
    }
