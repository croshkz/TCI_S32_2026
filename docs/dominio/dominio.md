# Dominio del TCI — Sistema de Gestión de Stock y Mantenimiento de Planta

**Documentación canónica del dominio · Desarrollo de Software 2026 · Comisión S32**

> Fuente de verdad del dominio. Las **decisiones de cátedra** y los **huecos deliberados** están en la **sección 7** (no son ambigüedades: son decisiones tomadas o espacio dejado a propósito para el modelado). Ante cualquier contradicción con otros documentos, **este documento manda**.

---

## 1. Descripción textual (lenguaje natural)

Una **fábrica de producción farmacéutica** necesita un sistema para gestionar el **mantenimiento de su planta**, que opera en **tres turnos** (mañana, tarde y noche) con maquinaria de producción como **calderas, fraccionadores y bandas de transporte**. Para sostener esa operación continua, la planta mantiene un **almacén de repuestos e insumos**.

El interesado —el **área de mantenimiento**— pide que el sistema se centre en el **seguimiento del stock** de los repuestos. La operación es la siguiente: **cada repuesto tiene un código QR o de barras**; cuando un repuesto se usa, un empleado **escanea ese código** y el sistema **descuenta del stock la cantidad usada** automáticamente. El sistema debe **avisar cuando el stock de un repuesto llega a su umbral mínimo**, que es un **valor propio de cada repuesto**. Además, de cada repuesto se debe poder **reconstruir su historia**: cuándo se pidió, cuándo se recibió y en qué máquina o reparación se utilizó. Por último, el sistema debe **gestionar las ubicaciones** de los repuestos dentro del almacén.

Alrededor de ese núcleo de stock, el área de mantenimiento tiene otros procesos:

- Los **operarios de máquina** reportan **incidencias** o solicitan **reparaciones técnicas** en cualquier turno, **adjuntando fotos** desde su celular e **identificando la máquina** por su código QR o de barras. Una incidencia puede requerir **cero o más repuestos**.
- Los **empleados de mantenimiento** **ingresan repuestos** al almacén escaneando su código, **consultan la existencia** de un repuesto (por nombre, descripción, nombre de máquina, código QR o de barras) y **registran qué repuestos usaron** (y en qué cantidad) en cada reparación.
- Cuando **no hay stock disponible** de un repuesto, el empleado lo reporta y puede **generar un pedido de compra**, que se envía con su **grado de urgencia** a los **encargados de todos los turnos** y a la **gerencia de producción**.
- Los **encargados** mantienen una **lista de compras** que se arma según el **umbral mínimo** de cada repuesto, y que también puede alimentarse con **requerimientos específicos** o **previsión de necesidades**.
- Cuando una compra **se entrega**, los encargados **cargan el stock y su ubicación**; pueden **delegar** la tarea y luego **supervisarla**.
- Se pueden **reservar** repuestos para un **mantenimiento o reparación preventiva planificada**; un repuesto reservado **no se usa en otra incidencia**, salvo **autorización de un encargado** y **aviso inmediato** del cambio. Cuando el mantenimiento preventivo **se ejecuta**, el sistema **descuenta el stock físico y libera la reserva**.
- Al ingresar una **nueva máquina** (o un nuevo ejemplar), se **registra** y se arma la **lista de repuestos** a mantener en stock.
- El sistema **reconoce un repuesto a partir de una foto** e informa su **nombre, código, máquinas a las que aplica, existencia de stock y ubicación**.
- **Cada incidente, cambio de parte, solicitud de compra e informe de resolución** se **almacena** y se **notifica por correo electrónico**.

El sistema se usa **desde el celular** (operarios y mantenimiento, en la planta) y **desde la PC** (encargados y gerencia, en oficinas, para ver tableros de seguimiento de incidencias, triage de reportes activos, calendario de reparaciones planificadas, situación de cada máquina e histórico estadístico). Debe ser **fácil de usar**, de **acceso rápido**, **integrado al correo** de los usuarios, con **respuestas rápidas** y pensado como un **producto que crece**.

---

## 2. Glosario

| Término | Definición |
|---|---|
| **Repuesto / Insumo** | Pieza o material para reparar o mantener máquinas. Tiene **código único** (QR/barcode), nombre, descripción, **stock físico**, **umbral mínimo** y **ubicación**. |
| **Máquina** | Equipo de producción (caldera, fraccionador, banda de transporte, etc.). Se identifica por su **código QR o de barras**. Puede haber **varios ejemplares** de un mismo modelo. |
| **Stock físico** | Cantidad **entera ≥ 0** de unidades existentes de un repuesto. |
| **Stock reservado** | Unidades **apartadas** por reservas activas. |
| **Stock disponible** | `stock físico − stock reservado`. Es el valor sobre el que se evalúa la disponibilidad. |
| **Umbral mínimo** | Valor **entero ≥ 0** propio de cada repuesto. Se alerta cuando `stock disponible ≤ umbral mínimo`. |
| **Lista de compras** | **Vista derivada** (no entidad persistida): repuestos en estado "bajo umbral" + requerimientos manuales agregados por el encargado. |
| **Ubicación** | Código alfanumérico (ej. `A-03-12`) + descripción opcional. *Decisión de cátedra (sección 7)*. |
| **Línea de uso** | Registro de **cuántas unidades** (`cantidad ≥ 1`) de un repuesto se usaron en una reparación. |
| **Incidencia** | Reporte de un problema en una máquina. Puede requerir **0 o más** repuestos. |
| **Reparación** | Trabajo técnico de mantenimiento; consume repuestos por **líneas de uso** (descuenta stock). |
| **Pedido de compra** | Solicitud de reposición de repuestos, con **grado de urgencia**. |
| **Reserva** | Apartado de repuestos para un mantenimiento preventivo planificado. |
| **Movimiento de stock** | Registro **inmutable** de un cambio de stock (tipos: `entrada`, `salida`, `reserva`, `liberación`, `consumo`). |
| **Turno** | `mañana`, `tarde` o `noche`. |

---

## 3. Actores (4 roles)

| Rol | Qué hace |
|---|---|
| **Operario de máquina** | Reporta incidencias y solicita reparaciones (fotos + QR de máquina), en cualquier turno. |
| **Empleado de mantenimiento** | Ingresa repuestos (escaneo), consulta existencia, registra uso de repuestos. |
| **Encargado de mantenimiento** | Mantiene la lista de compras, carga el stock recibido (o delega y supervisa), **autoriza la liberación de reservas**. |
| **Gerencia / Administración** | **Solo lectura**: ve los tableros y recibe las notificaciones de pedidos de compra. |

> **Decisión de cátedra (sección 7):** "Gerencia de producción" y "Personal administrativo" tienen el mismo permiso efectivo (ver tableros). Se **fusionan** en un único rol de consulta.

---

## 4. Reglas de negocio

- **RN-01 — Descuento por uso.** Usar un repuesto en una reparación descuenta del **stock físico** la `cantidad` de la línea de uso (entera ≥ 1). El stock físico resultante debe ser **≥ 0**: si no alcanza, el uso se rechaza.
- **RN-02 — Umbral.** Cada repuesto tiene un `umbral mínimo`. Cuando `stock disponible ≤ umbral mínimo`, se genera una **alerta** y el repuesto aparece en la **lista de compras**.
- **RN-03 — Faltante → compra.** Si no hay **stock disponible** para una solicitud, el empleado lo reporta y puede **generar un pedido de compra**.
- **RN-04 — Urgencia.** El pedido de compra se envía con su **grado de urgencia** a los **encargados de todos los turnos** y a la **gerencia**.
- **RN-05 — Reserva.** Un repuesto **reservado** no se usa en otra incidencia. La liberación exige **autorización de un usuario con rol Encargado** y **aviso inmediato** del cambio y su impacto sobre lo planificado.
- **RN-06 — Trazabilidad.** De cada repuesto se reconstruye su historia **interna**: pedido de compra → recepción (RN-08) → uso. *La logística externa con proveedores queda fuera del alcance* (sección 7).
- **RN-07 — Nueva maquinaria.** Al ingresar una nueva máquina, se **registra** y se genera la **lista de repuestos** a mantener en stock.
- **RN-08 — Carga de compra.** Al recibir una compra, se **carga el stock físico y su ubicación**; la tarea puede **delegarse** y **supervisarse**.
- **RN-09 — Notificación por correo.** Se notifican por correo: **incidentes, cambios de parte, solicitudes de compra, informes de resolución y alertas de umbral**. *(Implementación vía puerto de notificación con adaptador falso por defecto, sección 7.)*
- **RN-10 — Consumo de reserva.** Al **ejecutar** el mantenimiento preventivo, se **descuenta el stock físico y se libera la reserva** en la **misma transacción**.

---

## 5. Entidades

**Máquina** (código, tipo, ejemplar, estado) · **Repuesto** (código, nombre, descripción, stock físico, umbral mínimo, ubicación) · **Línea de uso** (repuesto, cantidad, reparación) · **Incidencia** (máquina, fotos, estado, turno) · **Reparación** · **Pedido de compra** (repuestos, urgencia, estado) · **Reserva** (repuestos, motivo, estado) · **Movimiento de stock** (tipo, fecha, usuario, referencia) · **Informe de resolución** · **Usuario** (rol).

---

## 6. Requisitos no funcionales

### Del interesado
- **Mobile-first** (celular); tableros en PC.
- **Fácil de usar** y de **acceso rápido**.
- **Integrado al correo electrónico** de los usuarios.
- **Respuestas rápidas**.
- **Reconocimiento** por código QR / de barras y por **foto de repuesto**.
- Uso en **planta** (celular) y **oficinas** (PC).

### De la cátedra (propios de la materia)
- Arquitectura **multicapa** justificada.
- **Prototipo reutilizable y escalable**.
- **Seguridad**: autenticación y **autorización por rol**.
- **Portabilidad**: entorno **reproducible** (Docker) y despliegue en ambiente arbitrario.

### Notas técnicas (anticipar, no chocar)
- **Cámara del navegador (`getUserMedia`) requiere contexto seguro** (HTTPS o `localhost`). El escaneo QR no funciona sobre HTTP plano en un celular de la red. Esto condiciona M2/M3 (se resuelve con despliegue sobre HTTPS o PWA).
- **Correo real es un pozo de tiempo.** RN-09 se implementa con un **puerto de notificación** y un **adaptador falso** (log o Mailhog) como implementación por defecto. Es además la excusa pedagógica para enseñar **puertos y adaptadores**.

---

## 7. Decisiones de cátedra y huecos deliberados

### Decisiones de cátedra (resoluciones tomadas; no son ambigüedades)
1. **Roles:** "Gerencia de producción" y "Personal administrativo" se **fusionan** en un rol de consulta (mismo permiso efectivo).
2. **Lista de compras** es una **vista derivada**, no una entidad persistida; el **Pedido de compra** es la entidad que materializa líneas de esa lista.
3. **Cantidad por línea de uso:** cada uso registra una `cantidad ≥ 1` (no es siempre 1); RN-01 descuenta esa cantidad.
4. **Turno del encargado:** el turno se deriva del **timestamp** del reporte; autoriza cualquier usuario con rol **Encargado** (la gestión de personal/turnos está fuera de alcance).
5. **Urgencia:** valores `normal` y `urgente`. **Ubicación:** código alfanumérico + descripción opcional.

### Huecos deliberados (se dejan abiertos a propósito — se resuelven en las muestras)
1. **Estados de Incidencia, Reserva, Pedido y Máquina:** **no se definen acá**. Se piden como **máquinas de estado en M1** (es el artefacto de modelado de mayor valor).
2. **Concurrencia (RN-01):** no se especifica qué pasa si dos empleados descuentan la última unidad a la vez. Es **requisito explícito de M4**: la decisión (`CHECK` a nivel base, `SELECT FOR UPDATE`, o versionado optimista) se documenta como **ADR**.
3. **Devoluciones y ajuste por conteo físico:** **fuera del alcance** del MVP (se deja como extensión posible: un tipo de movimiento `ajuste`).
