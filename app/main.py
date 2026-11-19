# app/main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, SessionLocal
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# Esto crea las tablas en SQLite físicamente
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="WOON Hoodies API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.get("/hoodies/", response_model=list[schemas.HoodieBase])
def obtener_catalogo(db: Session = Depends(get_db)):
    catalogo = db.query(models.Hoodie).all()
    return catalogo

@app.post("/pedidos/", response_model=schemas.PedidoResponse)
def crear_pedido(pedido: schemas.PedidoCreate, db: Session = Depends(get_db)):
    # Buscar al cliente y al producto
    cliente = db.query(models.Cliente).filter(models.Cliente.id == pedido.cliente_id).first()
    hoodie = db.query(models.Hoodie).filter(models.Hoodie.id == pedido.hoodie_id).first()

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    if not hoodie:
        raise HTTPException(status_code=404, detail="Hoodie no encontrada")
    if hoodie.stock < pedido.cantidad:
        raise HTTPException(status_code=400, detail="Stock insuficiente")

    # Cálculos base
    subtotal = hoodie.precio * pedido.cantidad
    
    # Lógica de descuentos basada en el BPMN
    porcentaje_base = 0.10 if subtotal > 1000 else 0.05
    
    bono_tipo = 0.0
    if cliente.tipo_cliente == "1":
        bono_tipo = 0.05
    elif cliente.tipo_cliente == "2":
        bono_tipo = 0.02

    porcentaje_total = porcentaje_base + bono_tipo
    descuento_dinero = round(subtotal * porcentaje_total, 2)
    total_final = round(subtotal - descuento_dinero, 2)

    # Guardar en base de datos
    nuevo_pedido = models.Pedido(
        cliente_id=pedido.cliente_id,
        hoodie_id=pedido.hoodie_id,
        cantidad=pedido.cantidad,
        subtotal=subtotal,
        descuento_aplicado=descuento_dinero,
        total=total_final
    )
    
    # Restar stock
    hoodie.stock -= pedido.cantidad
    
    db.add(nuevo_pedido)
    db.commit()
    db.refresh(nuevo_pedido)

    return nuevo_pedido

app.mount("/", StaticFiles(directory="static", html=True), name="static")