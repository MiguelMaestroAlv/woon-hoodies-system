from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Ruta donde se creará el archivo de la base de datos local
SQLALCHEMY_DATABASE_URL = "sqlite:///./woon_hoodies.db"

# Motor de conexión y sesión
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base que usarán nuestras tablas
Base = declarative_base()

