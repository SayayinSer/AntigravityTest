from app.database import SessionLocal
from app import models

def seed_data():
    db = SessionLocal()
    try:
        # 1. Marcas por defecto
        brands = ["Toyota", "Ford", "Volkswagen", "Fiat", "Chevrolet", "Renault", "Peugeot", "Honda"]
        for b_name in brands:
            if not db.query(models.Brand).filter_by(name=b_name).first():
                db.add(models.Brand(name=b_name))
        
        # 2. Tipos de Vehículo
        types = ["Sedán", "Hatchback", "SUV", "Pickup", "Utilitario", "Motocicleta", "Camión"]
        for t_name in types:
            if not db.query(models.VehicleType).filter_by(name=t_name).first():
                db.add(models.VehicleType(name=t_name))
        
        # 3. Técnicos Iniciales
        techs = ["Juan Mecánico", "Pedro Electricista", "Carlos Chapista", "Soporte General"]
        for tech_name in techs:
            if not db.query(models.Technician).filter_by(name=tech_name).first():
                db.add(models.Technician(name=tech_name))
        
        db.commit()
        print("¡Datos maestros precargados con éxito!")
    except Exception as e:
        print(f"Error al precargar datos: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
