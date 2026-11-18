from app.database import SessionLocal
from app import models

db = SessionLocal()

# Creamos un cliente Tipo 1 y una hoodie de $1,200
cliente_prueba = models.Cliente(nombre="Ximena", correo="ximena@test.com", contrasena="Woon2026", tipo_cliente="1")
hoodie_prueba = models.Hoodie(nombre="WOON Classic Oversize", color="Negro", precio=1200.0, stock=50)

db.add(cliente_prueba)
db.add(hoodie_prueba)
db.commit()

print("Datos inyectados con éxito. Cliente ID: 1, Hoodie ID: 1")