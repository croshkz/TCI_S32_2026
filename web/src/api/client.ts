import createClient from 'openapi-fetch'
import type { components, paths } from './schema'

export type Rol = components['schemas']['Rol']
export type Repuesto = components['schemas']['Repuesto']
export type Usuario = components['schemas']['Usuario']
export type DestinoUso =
  paths['/destinos-uso']['get']['responses'][200]['content']['application/json'][number]
export type ApiError = components['schemas']['Error']

type Health = paths['/health']['get']['responses'][200]['content']['application/json']

export const ETIQUETAS_ROL: Record<Rol, string> = {
  OPERARIO: 'Operario',
  MANTENIMIENTO: 'Mantenimiento',
  ENCARGADO: 'Encargado',
  CONSULTA: 'Gerencia (consulta)',
}

// El token vive en sessionStorage: sobrevive a un F5 pero se borra al cerrar la pestaña.
const CLAVE_SESION = 'planta.sesion'
export const EVENTO_SESION_VENCIDA = 'planta:sesion-vencida'

type Sesion = { token: string; usuario: Usuario }

function leerSesion(): Sesion | null {
  try {
    const guardada = sessionStorage.getItem(CLAVE_SESION)
    return guardada ? (JSON.parse(guardada) as Sesion) : null
  } catch {
    return null
  }
}

let sesion: Sesion | null = leerSesion()

export function usuarioActual(): Usuario | null {
  return sesion?.usuario ?? null
}

export function cerrarSesion() {
  sesion = null
  try {
    sessionStorage.removeItem(CLAVE_SESION)
  } catch {
    // sin storage disponible: la sesión ya quedó borrada en memoria
  }
}

export const api = createClient<paths>({ baseUrl: '/api' })

api.use({
  onRequest({ request }) {
    if (sesion) request.headers.set('Authorization', `Bearer ${sesion.token}`)
    return request
  },
  onResponse({ request, response }) {
    // Token vencido o inválido: se cierra la sesión y la app vuelve al login.
    if (response.status === 401 && !request.url.endsWith('/auth/login')) {
      cerrarSesion()
      window.dispatchEvent(new Event(EVENTO_SESION_VENCIDA))
    }
    return response
  },
})

export async function iniciarSesion(usuario: string, password: string): Promise<Usuario> {
  const { data, error } = await api.POST('/auth/login', { body: { usuario, password } })
  if (!data) throw new Error(mensajeDeError(error, 'No se pudo iniciar sesión.'))
  sesion = { token: data.access_token, usuario: data.usuario }
  try {
    sessionStorage.setItem(CLAVE_SESION, JSON.stringify(sesion))
  } catch {
    // sin storage: la sesión queda solo en memoria
  }
  return data.usuario
}

export async function obtenerHealth(): Promise<Health> {
  const respuesta = await fetch('/health')
  if (!respuesta.ok) throw new Error(`HTTP ${respuesta.status}`)
  return respuesta.json()
}

export function mensajeDeError(error: unknown, porDefecto: string): string {
  if (error && typeof error === 'object' && 'mensaje' in error && typeof error.mensaje === 'string') {
    return error.mensaje
  }
  return porDefecto
}
