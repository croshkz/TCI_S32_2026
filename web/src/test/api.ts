import { vi } from 'vitest'

type Respuesta = { status?: number; body?: unknown }
type Manejador = Respuesta | ((request: Request) => Respuesta | Promise<Respuesta>)

/**
 * Responde los requests según la ruta, con claves del tipo "POST /api/auth/login".
 * Una ruta no declarada responde 501, así el test falla en vez de colgarse.
 */
export function simularApi(rutas: Record<string, Manejador>) {
  vi.mocked(fetch).mockImplementation(async (entrada, init) => {
    const request =
      entrada instanceof Request ? entrada : new Request(new URL(String(entrada), window.location.origin), init)
    const clave = `${request.method} ${new URL(request.url).pathname}`
    const manejador = rutas[clave]
    const { status = 200, body } = manejador
      ? typeof manejador === 'function'
        ? await manejador(request)
        : manejador
      : { status: 501, body: { codigo: 'NO_SIMULADO', mensaje: `Ruta no simulada en el test: ${clave}` } }
    return new Response(body === undefined ? null : JSON.stringify(body), {
      status,
      headers: { 'Content-Type': 'application/json' },
    })
  })
}

/** Devuelve los requests que recibió la API simulada para una ruta, en orden. */
export function requestsA(clave: string): Request[] {
  return vi
    .mocked(fetch)
    .mock.calls.map(([entrada]) => entrada)
    .filter((entrada): entrada is Request => entrada instanceof Request)
    .filter((request) => `${request.method} ${new URL(request.url).pathname}` === clave)
}

export const formulariosEnviados = new WeakMap<Request, FormData>()

/** Devuelve el FormData que mandó un request multipart (ver setup.ts). */
export function formularioEnviado(request: Request): FormData {
  const datos = formulariosEnviados.get(request)
  if (!datos) throw new Error(`El request ${request.method} ${request.url} no mandó un formulario`)
  return datos
}

export const REPUESTO = {
  codigo: 'REP-6204',
  nombre: 'Rodamiento 6204',
  lote: 'L-2026-031',
  ubicacion: 'A-03-12',
  umbral_minimo: 5,
  stock_fisico: 12,
  stock_reservado: 0,
  stock_disponible: 12,
}
