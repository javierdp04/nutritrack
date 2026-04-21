from app import create_app
from auth_utils import hash_password
from models import Receta, Usuario, db


RECETAS = [
    {
        "titulo": "Avena con frutas",
        "calorias": 350,
        "ingredientes": "50 g avena\n200 ml leche\n1 plátano\n10 g miel\nCanela",
        "preparacion": "Cocinar la avena con la leche 3 minutos. Añadir plátano en rodajas, miel y canela por encima.",
    },
    {
        "titulo": "Ensalada de pollo y quinoa",
        "calorias": 520,
        "ingredientes": "120 g pollo a la plancha\n80 g quinoa\nTomate cherry\nAguacate\nLimón\nAceite de oliva",
        "preparacion": "Cocer la quinoa. Mezclar con el pollo troceado, el tomate y el aguacate. Aliñar con limón y aceite.",
    },
    {
        "titulo": "Salmón al horno con verduras",
        "calorias": 600,
        "ingredientes": "180 g salmón\nCalabacín\nPimiento rojo\nCebolla\nAceite de oliva\nSal y pimienta",
        "preparacion": "Hornear el salmón 15 minutos a 200ºC sobre una cama de verduras aliñadas.",
    },
    {
        "titulo": "Tortilla francesa con espinacas",
        "calorias": 280,
        "ingredientes": "2 huevos\nEspinacas frescas\nSal\nAceite de oliva",
        "preparacion": "Saltear las espinacas. Batir los huevos, verter y cuajar. Doblar y servir.",
    },
    {
        "titulo": "Yogur griego con nueces",
        "calorias": 260,
        "ingredientes": "200 g yogur griego\n20 g nueces\n10 g miel",
        "preparacion": "Servir el yogur en un bol y añadir las nueces y la miel por encima.",
    },
    {
        "titulo": "Arroz integral con garbanzos",
        "calorias": 480,
        "ingredientes": "80 g arroz integral\n100 g garbanzos cocidos\nCebolla\nPimiento\nComino\nAceite de oliva",
        "preparacion": "Sofreír cebolla y pimiento, añadir los garbanzos y el comino. Servir sobre el arroz cocido.",
    },
    {
        "titulo": "Crema de calabaza",
        "calorias": 220,
        "ingredientes": "300 g calabaza\n1 patata pequeña\n1 cebolla\nCaldo de verduras\nAceite de oliva",
        "preparacion": "Cocer las verduras en caldo 20 minutos y triturar hasta obtener una crema fina.",
    },
    {
        "titulo": "Sandwich integral de pavo",
        "calorias": 400,
        "ingredientes": "2 rebanadas de pan integral\n60 g pavo\nLechuga\nTomate\nMostaza",
        "preparacion": "Montar el sandwich con todos los ingredientes y tostar ligeramente.",
    },
]


def seed():
    app = create_app()
    with app.app_context():
        db.create_all()

        if Usuario.query.filter_by(email="admin@nutritrack.local").first() is None:
            admin = Usuario(
                nombre="Admin",
                email="admin@nutritrack.local",
                password_hash=hash_password("admin1234"),
                rol="admin",
            )
            db.session.add(admin)

        if Receta.query.count() == 0:
            for r in RECETAS:
                db.session.add(Receta(**r))

        db.session.commit()
        print(f"Seed OK. Recetas: {Receta.query.count()}, usuarios: {Usuario.query.count()}")


if __name__ == "__main__":
    seed()
