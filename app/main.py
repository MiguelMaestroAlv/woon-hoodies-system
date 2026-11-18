# app/main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, SessionLocal

# Esto crea las tablas en SQLite físicamente
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="WOON Hoodies API")

# Dependencia para conectarnos a la base de datos en cada petición
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/clientes/")
def registrar_cliente(cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    # 1. Verificar si el correo ya existe
    db_cliente = db.query(models.Cliente).filter(models.Cliente.correo == cliente.correo).first()
    if db_cliente:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    
    # 2. Guardar el nuevo cliente (la contraseña ya viene validada desde schemas.py)
    nuevo_cliente = models.Cliente(
        nombre=cliente.nombre,
        correo=cliente.correo,
        contrasena=cliente.contrasena
    )
    db.add(nuevo_cliente)
    db.commit()
    db.refresh(nuevo_cliente)
    
    return {"mensaje": "Cliente registrado exitosamente", "cliente": nuevo_cliente.nombre}