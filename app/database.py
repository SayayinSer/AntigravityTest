from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL limpia (Sin parámetros conflictivos de colación en el string)
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:123456@localhost/antigravity_test?charset=utf8mb4"

# Engine con Collation explícita compatible con versiones anteriores de MySQL (5.7, MariaDB 10.x)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        "collation": "utf8mb4_general_ci"  # Forzar colación universalmente compatible
    },
    pool_recycle=3600,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
