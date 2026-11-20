import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it } from 'vitest'
import { REPUESTO, requestsA, simularApi } from '../test/api'
import RegistrarUso from './RegistrarUso'

const AVISO_UMBRAL = 'El stock llegó al mínimo. El repuesto pasa a la lista de compras.'

const DESTINOS = [
  { id: 'INC-0001', maquina: 'Caldera 2' },
  { id: 'INC-0002', maquina: 'Fraccionador 1' },
]

function simularUso(respuesta: { status?: number; body: unknown }) {
  simularApi({
    'GET /api/repuestos/REP-6204': { body: REPUESTO },
    'GET /api/destinos-uso': { body: DESTINOS },
    'POST /api/repuestos/REP-6204/usos': respuesta,
  })
}

async function registrar(cantidad: number) {
  render(<RegistrarUso />)
  expect(await screen.findByText('Rodamiento 6204')).toBeInTheDocument()
  expect(await screen.findByRole('option', { name: 'INC-0001 · Caldera 2' })).toBeInTheDocument()

  const campoCantidad = screen.getByLabelText('Cantidad')
  await userEvent.clear(campoCantidad)
  await userEvent.type(campoCantidad, String(cantidad))
  await userEvent.click(screen.getByRole('button', { name: 'Registrar uso' }))
}

describe('Registrar uso de repuesto', () => {
  it('envía destino y cantidad, y muestra el aviso de stock mínimo cuando la API informa alerta (RN-02)', async () => {
    simularUso({
      status: 201,
      body: { stock_fisico: 5, stock_reservado: 0, stock_disponible: 5, alerta_umbral: true },
    })

    await registrar(4)

    expect(await screen.findByText('Uso registrado. Stock resultante: 5')).toBeInTheDocument()
    expect(screen.getByText(AVISO_UMBRAL)).toBeInTheDocument()
    const [uso] = requestsA('POST /api/repuestos/REP-6204/usos')
    expect(await uso.json()).toEqual({ destino_id: 'INC-0001', cantidad: 4 })
  })

  it('no muestra el aviso si el stock queda por encima del mínimo', async () => {
    simularUso({
      status: 201,
      body: { stock_fisico: 9, stock_reservado: 0, stock_disponible: 9, alerta_umbral: false },
    })

    await registrar(3)

    expect(await screen.findByText('Uso registrado. Stock resultante: 9')).toBeInTheDocument()
    expect(screen.queryByText(AVISO_UMBRAL)).not.toBeInTheDocument()
  })

  it('muestra el mensaje de la API cuando rechaza el uso por stock insuficiente (RN-01)', async () => {
    simularUso({
      status: 409,
      body: { codigo: 'STOCK_INSUFICIENTE', mensaje: 'La cantidad supera el stock disponible (12).' },
    })

    await registrar(20)

    expect(await screen.findByRole('alert')).toHaveTextContent('La cantidad supera el stock disponible (12).')
    expect(screen.queryByText(/Uso registrado/)).not.toBeInTheDocument()
    expect(screen.queryByText(AVISO_UMBRAL)).not.toBeInTheDocument()
  })
})
