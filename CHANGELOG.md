# Changelog

Todas las modificaciones notables del proyecto **WOON Hoodies** están documentadas en este archivo.

## [v1.1.0] - 2026-11-19
### Agregado
- Nueva pantalla independiente de Registro de Clientes (`static/registro.html`) conectada a `POST /clientes/`.
- Barra de navegación neo-brutalista en `static/index.html` y `static/registro.html` para alternar entre Catálogo/Pedidos y Registro.

### Corregido
- Validación estricta en `app/schemas.py` para rechazar contraseñas que contengan espacios en blanco.

## [v1.0.0] - 2026-11-18
### Agregado
- Interfaz web funcional con diseño neo-brutalista conectada a la API (`static/index.html`).
- Suite de 5 pruebas automatizadas con `pytest` cubriendo validación de contraseñas, catálogo y descuentos (`test_main.py`).
- Flujo de Integración Continua (CI) con GitHub Actions (`.github/workflows/ci.yml`).
- Archivo `requirements.txt` y documentación de reproducibilidad en `README.md`.

### Corregido
- Corrección de precisión de punto flotante en el cálculo de descuentos y totales aplicando redondeo a 2 decimales (`round(..., 2)`).

## [v0.1.0] - 2026-11-18
### Agregado
- Estructura base del proyecto con FastAPI y persistencia en SQLite.
- Registro de clientes con validación estricta de contraseñas (8-16 caracteres, mayúscula, número, sin espacios).
- Consulta de catálogo de hoodies y script semilla (`poblar.py`).
- Módulo de pedidos con cálculo automático de descuentos según monto y tipo de cliente.