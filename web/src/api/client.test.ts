import { describe, expect, it, vi } from 'vitest'
import { REPUESTO, requestsA, simularApi } from '../test/api'
import { api, EVENTO_SESION_VENCIDA, iniciarSesion, usuarioActual } from './client'

const LOGIN_OK = {
  body: {
    access_token: 'token-de-prueba',
    token_type: 'bearer',
    expira_en: 28800,
    usuario: { nombre: 'Encargado Demo', rol: 'ENCARGADO' },
  },
}

function escucharSesionVencida() {
  const escucha = vi.fn()
  window.addEventListener(EVENTO_SESION_VENCIDA, escucha)
  return escucha
}

describe('cliente de la API', () => {
  it('después de iniciar sesión manda el token en cada request', async () => {
    simularApi({
      'POST /api/auth/login': LOGIN_OK,
      'GET /api/repuestos/REP-6204': { body: REPUESTO },
    })

    await iniciarSesion('encargado', 'planta2026')
    await api.GET('/repuestos/{codigo}', { params: { path: { codigo: 'REP-6204' } } })

    const [consulta] = requestsA('GET /api/repuestos/REP-6204')
    expect(consulta.headers.get('Authorization')).toBe('Bearer token-de-prueba')
  })

  it('un 401 en un endpoint protegido cierra la sesión y avisa a la app', async () => {
    simularApi({
      'POST /api/auth/login': LOGIN_OK,
      'GET /api/repuestos/REP-6204': {
        status: 401,
        body: { codigo: 'NO_AUTENTICADO', mensaje: 'Tu sesión venció.' },
      },
    })
    await iniciarSesion('encargado', 'planta2026')
    const sesionVencida = escucharSesionVencida()

    await api.GET('/repuestos/{codigo}', { params: { path: { codigo: 'REP-6204' } } })

    expect(sesionVencida).toHaveBeenCalledOnce()
    expect(usuarioActual()).toBeNull()
    expect(sessionStorage.getItem('planta.sesion')).toBeNull()
  })

  it('un 401 en el login no se trata como sesión vencida', async () => {
    simularApi({
      'POST /api/auth/login': {
        status: 401,
        body: { codigo: 'CREDENCIALES_INVALIDAS', mensaje: 'Usuario o contraseña incorrectos.' },
      },
    })
    const sesionVencida = escucharSesionVencida()

    await expect(iniciarSesion('encargado', 'mala')).rejects.toThrow('Usuario o contraseña incorrectos.')
    expect(sesionVencida).not.toHaveBeenCalled()
  })
})
