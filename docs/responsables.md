# Responsables por caso de uso

Cada caso de uso tiene **un** responsable. El responsable no hace todo el trabajo: se asegura de que el caso de uso funcione de punta a punta (contrato, backend, front y tests), revisa los PR que lo tocan y lleva el seguimiento de sus issues.

| Caso de uso | Reglas | Responsable | Backend | Front | Tests |
| --- | --- | --- | --- | --- | --- |
| **CU-01** Registrar uso de repuesto | RN-01, RN-02, RN-05 | Tiziano Hurst | `POST /repuestos/{codigo}/usos` | `RegistrarUso.tsx` | `test_rn01_descuento_por_uso.py`, `test_rn02_umbral.py` |
| **CU-02** Reportar incidencia y pasarla a reparación | — | Cristian Hrynkiewicz | `POST /incidencias`, `POST /incidencias/{codigo}/reparacion` | `Incidencia.tsx` | `test_incidencias.py` |
| **CU-03** Cargar stock recibido | RN-08 | Cristian Hrynkiewicz | `POST /repuestos/{codigo}/recepciones` | `CargarStock.tsx` | `test_rn08_recepcion.py` |
| **CU-04** Reservar, liberar y ejecutar reservas | RN-05, RN-10 | Nahuel Hernández Ulanio | `/reservas`, `/reservas/{codigo}/liberacion`, `/reservas/{codigo}/ejecucion` | Sin pantalla (Swagger) | `test_rn05_reservas.py` |
| **CU-05** Iniciar sesión | — | Nahuel Hernández Ulanio | `POST /auth/login`, `GET /auth/me` | `Login.tsx` | `test_auth_jwt.py`, `test_auth_y_endpoints.py` |
| **CU-06** Consultar trazabilidad de un repuesto | RN-06 | Tiziano Hurst | `GET /repuestos/{codigo}/movimientos` | Sin pantalla (Swagger) | `test_rn06_trazabilidad.py` |

La especificación completa de CU-01 está en [spec/EntregaM1.md](spec/EntregaM1.md). Las decisiones de arquitectura y sus responsables están en [adr/](adr/README.md).

## Pendiente por caso de uso

| Caso de uso | Pendiente |
| --- | --- |
| CU-01 | Escaneo del código con la cámara (hoy se ingresa a mano). Consumo de reserva desde el uso (escenario 5a) y desafectación (7a). |
| CU-02 | Pasar una incidencia a `RESUELTA`. Pantalla para pasar a reparación. |
| CU-03 | Delegación y supervisión de la carga (RN-08). |
| CU-04 | Pantalla de reservas en el front. |
| CU-05 | Alta de usuarios y cambio de contraseña. |
| CU-06 | Pantalla de historial en el front. Pedidos de compra como primer eslabón de la cadena (RN-03, RN-06). |
