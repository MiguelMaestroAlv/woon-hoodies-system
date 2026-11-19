# app/schemas.py
from pydantic import BaseModel, field_validator
import re

class ClienteCreate(BaseModel):
    nombre: str
    correo: str
    contrasena: str

    @field_validator('contrasena')
    def validar_contrasena(cls, v):
        if len(v) < 8 or len(v) > 16:
            raise ValueError('La contraseña debe tener entre 8 y 16 caracteres')
        if not re.search(r'[A-Z]', v):
            raise ValueError('La contraseña debe contener al menos una letra mayúscula')
        if not re.search(r'[0-9]', v):
            raise ValueError('La contraseña debe contener al menos un número')
        if ' ' in v:
            raise ValueError('La contraseña no debe contener espacios')
        return v

class HoodieBase(BaseModel):
    id: int
    nombre: str
    color: str
    precio: float
    stock: int

    class Config:
        from_attributes = True

class PedidoCreate(BaseModel):
    cliente_id: int
    hoodie_id: int
    cantidad: int

class PedidoResponse(BaseModel):
    id: int
    cliente_id: int
    hoodie_id: int
    cantidad: int
    subtotal: float
    descuento_aplicado: float
    total: float

    class Config:
        from_attributes = True