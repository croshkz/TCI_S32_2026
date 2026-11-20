import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'
import { requestsA, simularApi } from '../test/api'
import Login from './Login'

describe('Login', () => {
  it('ingresa con el usuario sin espacios y guarda la sesión', async () => {
    simularApi({
      'POST /api/auth/login': {
        body: {
          access_token: 'token-de-prueba',
          token_type: 'bearer',
          expira_en: 28800,
          usuario: { nombre: 'Mantenimiento Demo', rol: 'MANTENIMIENTO' },
        },
      },
    })
    const onIngreso = vi.fn()
    render(<Login onIngreso={onIngreso} />)

    await userEvent.type(screen.getByLabelText('Usuario'), '  mantenimiento ')
    await userEvent.type(screen.getByLabelText('Contraseña'), 'planta2026')
    await userEvent.click(screen.getByRole('button', { name: 'Ingresar' }))

    await vi.waitFor(() => expect(onIngreso).toHaveBeenCalledOnce())
    expect(onIngreso).toHaveBeenCalledWith({ nombre: 'Mantenimiento Demo', rol: 'MANTENIMIENTO' })
    const [login] = requestsA('POST /api/auth/login')
    expect(await login.json()).toEqual({ usuario: 'mantenimiento', password: 'planta2026' })
    expect(sessionStorage.getItem('planta.sesion')).toContain('token-de-prueba')
  })

  it('muestra el error de la API y limpia la contraseña si las credenciales son inválidas', async () => {
    simularApi({
      'POST /api/auth/login': {
        status: 401,
        body: { codigo: 'CREDENCIALES_INVALIDAS', mensaje: 'Usuario o contraseña incorrectos.' },
      },
    })
    const onIngreso = vi.fn()
    render(<Login onIngreso={onIngreso} />)

    await userEvent.type(screen.getByLabelText('Usuario'), 'operario')
    await userEvent.type(screen.getByLabelText('Contraseña'), 'equivocada')
    await userEvent.click(screen.getByRole('button', { name: 'Ingresar' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('Usuario o contraseña incorrectos.')
    expect(screen.getByLabelText('Contraseña')).toHaveValue('')
    expect(onIngreso).not.toHaveBeenCalled()
    expect(sessionStorage.getItem('planta.sesion')).toBeNull()
  })
})
