# ADR-0005: Notificaciones detrás de un puerto, con adaptador de log

- **Estado:** Aceptado
- **Fecha:** 2026-11-02
- **Responsable:** Nahuel Hernández Ulanio

## Contexto

RN-02, RN-05 y RN-09 piden avisar las alertas de umbral y las liberaciones de reservas, en principio por correo. Para la entrega no hay servidor de correo disponible, y los tests no deberían mandar mails.

## Decisión

- Las notificaciones pasan por la interfaz `Notificador` (`app/notificaciones.py`), con un método por tipo de aviso (`alerta_umbral`, `reserva_liberada`).
- El adaptador por defecto, `NotificadorLog`, escribe el aviso en el log de la API (`docker compose logs api`).
- Los tests reemplazan el notificador por un `NotificadorFalso` que guarda los avisos en memoria, para verificar que se emitieron.
- Los services avisan **después** del `commit`: si la operación falla, no se notifica nada.

## Alternativas consideradas

- **Enviar los mails directamente desde los services:** acopla las reglas a SMTP y vuelve lentos y frágiles los tests.

## Consecuencias

- Para enviar correos de verdad alcanza con escribir un adaptador SMTP y devolverlo en `get_notificador`, sin tocar las reglas de negocio.
- Hoy los avisos solo se ven en el log (ver *Limitaciones conocidas* en el README).
