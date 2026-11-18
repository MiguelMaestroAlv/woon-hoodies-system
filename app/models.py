from sqlalchemy import Column, Integer, String, Float, ForeignKey
from .database import Base

class Cliente(Base):
    __tablename__ = "clientes"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    correo = Column(String, unique=True, index=True)
    contrasena = Column(String)  # Más adelante le pondremos la validación estricta
    tipo_cliente = Column(String, default="regular") # 'regular' o 'vip'

class Hoodie(Base):
    __tablename__ = "hoodies"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    color = Column(String)
    precio = Column(Float)
    stock = Column(Integer)

class Pedido(Base):
    __tablename__ = "pedidos"
    
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    hoodie_id = Column(Integer, ForeignKey("hoodies.id"))
    cantidad = Column(Integer)
    subtotal = Column(Float)
    descuento_aplicado = Column(Float)
    total = Column(Float)