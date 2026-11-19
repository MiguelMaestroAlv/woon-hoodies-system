import uuid
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app import models

client = TestClient(app)

def test_1_registro_contrasena_invalida():
    """Debe rechazar contraseñas sin mayúscula (Error 422)"""
    response = client.post("/clientes/", json={
        "nombre": "Test Invalido",
        "correo": f"fail_{uuid.uuid4()}@test.com",
        "contrasena": "sinmayusculas123",
        "tipo_cliente": "1"
    })
    assert response.status_code == 422

def test_2_registro_contrasena_valida():
    """Debe aceptar contraseñas que cumplan todas las reglas (Status 200)"""
    response = client.post("/clientes/", json={
        "nombre": "Test Valido",
        "correo": f"ok_{uuid.uuid4()}@test.com",
        "contrasena": "WoonSeguro2026",
        "tipo_cliente": "1"
    })
    assert response.status_code == 200

def test_3_obtener_catalogo():
    """Debe devolver el catálogo en formato lista (Status 200)"""
    response = client.get("/hoodies/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_4_descuento_mayor_1000_tipo_1():
    """Monto > $1,000 (10%) + Cliente Tipo 1 (5%) = 15% de descuento"""
    db = SessionLocal()
    cliente = models.Cliente(
        nombre="Test Tipo 1",
        correo=f"tipo1_{uuid.uuid4()}@test.com",
        contrasena="WoonSeguro2026",
        tipo_cliente="1"
    )
    hoodie = models.Hoodie(
        nombre="WOON Test Hoodie",
        color="Negro",
        precio=1200.0,
        stock=10
    )
    db.add(cliente)
    db.add(hoodie)
    db.commit()
    db.refresh(cliente)
    db.refresh(hoodie)
    db.close()

    response = client.post("/pedidos/", json={
        "cliente_id": cliente.id,
        "hoodie_id": hoodie.id,
        "cantidad": 1
    })
    assert response.status_code == 200
    data = response.json()
    assert data["subtotal"] == 1200.0
    assert data["descuento_aplicado"] == 180.0
    assert data["total"] == 1020.0

def test_5_pedido_cliente_inexistente():
    """Debe retornar 404 si el cliente no existe"""
    response = client.post("/pedidos/", json={
        "cliente_id": 99999,
        "hoodie_id": 1,
        "cantidad": 1
    })
    assert response.status_code == 404