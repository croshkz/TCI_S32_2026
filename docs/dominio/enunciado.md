# Sistema de Gestión de Stock y Mantenimiento de Planta

**Enunciado del Trabajo de Campo Integrador · Desarrollo de Software 2026 · Comisión S32**

---

## El cliente y su contexto

Una fábrica de producción farmacéutica trabaja en tres turnos —mañana, tarde y noche— con maquinaria que no puede detenerse: calderas, fraccionadores, bandas de transporte y otros equipos de producción. Para sostener esa operación continua, la planta mantiene un **almacén de repuestos e insumos**: las piezas necesarias para reparar y mantener cada máquina.

El problema de hoy es que no saben, en tiempo real, **cuánto repuesto tienen, dónde está guardado y en qué se usó**. Llevan el stock en planillas y papeles, y eso les cuesta paradas de máquina por repuestos que creían tener y no estaban, o compras duplicadas de piezas que ya tenían olvidadas en un rincón del depósito.

---

## La necesidad central: el seguimiento del stock

El interesado —el área de mantenimiento— necesita un sistema para **llevar el seguimiento del stock** de los repuestos. La forma de trabajar es simple y gira alrededor de una idea:

> **Cada repuesto tiene un código QR o de barras en su envase. Cuando un repuesto se usa, se escanea ese código y el sistema descuenta la unidad del stock automáticamente.**

Sobre esa base, el interesado pide lo siguiente:

- **Seguimiento del stock en tiempo real.** Saber cuántas unidades hay de cada repuesto, sin depender de planillas.
- **Descuento por escaneo.** Al usar un repuesto en una máquina, un empleado escanea su código QR o de barras con el celular y el stock se descuenta solo, sin tipear nada.
- **Alertas de umbral.** Cada repuesto tiene un stock mínimo propio. Cuando el stock llega a ese umbral, el sistema tiene que **avisar** para reponer la pieza antes de que falte.
- **Trazabilidad de cada repuesto.** De cada pieza se debe poder reconstruir su historia: **cuándo se compró, cuándo se recibió y en qué máquina o reparación se utilizó**. Nada se pierde: se sabe de dónde vino y a dónde fue cada repuesto.
- **Gestión de ubicaciones.** Saber **dónde está guardado** cada repuesto dentro del almacén (estantería, sector, pasillo) para encontrarlo rápido.

En una sola frase, lo que el interesado quiere es: *"escaneo el código, se descuenta el stock, me avisa cuando va a faltar, y siempre sé dónde está y en qué se usó cada repuesto".*

---

## El resto de la operación de mantenimiento

Alrededor de ese núcleo de stock, el área de mantenimiento tiene otros procesos que el sistema debería acompañar:

- Los **operarios de máquina** reportan incidencias o piden reparaciones técnicas en cualquier turno, sacando **fotos** con su celular e identificando la máquina leyendo su **código QR o de barras**. Una incidencia puede necesitar ningún repuesto o varios.
- Los **empleados de mantenimiento** ingresan repuestos al almacén escaneando su código, consultan si hay stock de una pieza (por nombre, descripción o código) y registran qué repuesto usaron en cada reparación. Cada uso **descuenta stock**.
- Cuando **no hay stock** de una pieza, el empleado lo reporta y se genera un **pedido de compra** con un grado de urgencia, que se notifica por **correo** a los encargados de todos los turnos y a la **gerencia de producción**.
- Los encargados mantienen una **lista de compras** que se arma automáticamente cuando un repuesto llega a su umbral mínimo, y también puede sumar pedidos puntuales o previsión de demanda.
- Cuando llega una compra, los encargados **cargan el stock y su ubicación** (pueden delegar la tarea y luego supervisarla).
- Se pueden **reservar** repuestos para un mantenimiento preventivo planificado; un repuesto reservado no se usa en otra cosa, salvo autorización del encargado del turno y aviso inmediato del cambio.
- Al ingresar una **máquina nueva**, se registra y se arma la lista de repuestos que hay que mantener en stock para ese equipo.
- El sistema reconoce un repuesto **a partir de una foto**: informa el nombre, el código, en qué máquinas se usa, cuánto stock hay y dónde está.
- La información completa de cada producto debe aparecer **al escanear su código**.

---

## Qué se espera de la solución

El sistema se usa **desde el celular** (operarios y mantenimiento, en la planta) y **desde la PC** (encargados y gerencia, en oficinas, para ver los **tableros de seguimiento**: incidencias, reparaciones planificadas, estado de cada máquina e histórico estadístico).

Tiene que ser **fácil de usar y rápido**, estar **integrado al correo electrónico** de los usuarios para que cada evento relevante les llegue por mail, y pensarse como un **producto que crece**: hoy arranca con el stock y el escaneo, y después se le suman el resto de los procesos de mantenimiento.
