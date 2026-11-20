import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it } from 'vitest'
import { formularioEnviado, REPUESTO, requestsA, simularApi } from '../test/api'
import CargarStock from './CargarStock'

function simularCarga() {
  simularApi({
    'GET /api/repuestos/REP-6204': { body: REPUESTO },
    'GET /api/ubicaciones': { body: ['A-03-12', 'A-03-13', 'B-01-04'] },
    'POST /api/repuestos/REP-6204/recepciones': {
      status: 201,
      body: { stock_fisico: 22, stock_reservado: 0, stock_disponible: 22 },
    },
  })
}

async function abrirPantalla() {
  render(<CargarStock />)
  expect(await screen.findByText('Rodamiento 6204')).toBeInTheDocument()
  expect(await screen.findByRole('option', { name: 'A-03-13' })).toBeInTheDocument()
  return screen.getByRole('button', { name: 'Cargar stock' })
}

describe('Cargar stock recibido (RN-08)', () => {
  it('no permite enviar hasta completar el lote', async () => {
    simularCarga()
    const enviar = await abrirPantalla()

    expect(enviar).toBeDisabled()
    await userEvent.type(screen.getByLabelText('Lote'), '   ')
    expect(enviar).toBeDisabled()
    await userEvent.type(screen.getByLabelText('Lote'), 'L-2026-045')
    expect(enviar).toBeEnabled()
  })

  it('envía lote, cantidad y ubicación, y después limpia el formulario', async () => {
    simularCarga()
    const enviar = await abrirPantalla()

    await userEvent.type(screen.getByLabelText('Lote'), 'L-2026-045')
    await userEvent.clear(screen.getByLabelText('Cantidad recibida'))
    await userEvent.type(screen.getByLabelText('Cantidad recibida'), '10')
    await userEvent.selectOptions(screen.getByLabelText('Ubicación en depósito'), 'A-03-13')
    await userEvent.click(enviar)

    expect(await screen.findByText('Stock cargado. Stock resultante: 22')).toBeInTheDocument()
    const [recepcion] = requestsA('POST /api/repuestos/REP-6204/recepciones')
    const datos = formularioEnviado(recepcion)
    expect(datos.get('lote')).toBe('L-2026-045')
    expect(datos.get('cantidad')).toBe('10')
    expect(datos.get('ubicacion')).toBe('A-03-13')

    // Regresión del #25: el lote es un input controlado y antes quedaba con el valor anterior.
    expect(screen.getByLabelText('Lote')).toHaveValue('')
    expect(screen.getByLabelText('Cantidad recibida')).toHaveValue(1)
    expect(enviar).toBeDisabled()
  })
})
