from app.database import SessionLocal
from app import models, auth

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

        # 4. ROLES DE SEGURIDAD
        roles = {
            "OficialSeguridad": "Acceso total a gestión de usuarios y sistema",
            "Gerente": "Acceso a reportes y supervisión",
            "Operador": "Carga de datos y gestión de órdenes",
            "Invitado": "Solo lectura"
        }
        db_roles = {}
        for r_name, r_desc in roles.items():
            role = db.query(models.Role).filter_by(name=r_name).first()
            if not role:
                role = models.Role(name=r_name, description=r_desc)
                db.add(role)
            db_roles[r_name] = role
        db.flush()

        # 5. USUARIOS INICIALES (Password: 123456 para todos)
        hashed_pass = auth.get_password_hash("123456")
        
        users_to_create = [
            {"user": "SU", "name": "Super Usuario", "role": "OficialSeguridad"},
            {"user": "operador", "name": "Operador Base", "role": "Operador"},
            {"user": "gerente", "name": "Gerente de Taller", "role": "Gerente"},
            {"user": "visitante", "name": "Invitado", "role": "Invitado"},
        ]

        for u_data in users_to_create:
            user = db.query(models.User).filter_by(username=u_data["user"]).first()
            if not user:
                user = models.User(
                    username=u_data["user"],
                    full_name=u_data["name"],
                    hashed_password=hashed_pass
                )
                user.roles.append(db_roles[u_data["role"]])
                db.add(user)
        
        db.commit()
        print("¡Módulo de Seguridad y Datos Maestros inicializados!")
    except Exception as e:
        print(f"Error en seeding: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
