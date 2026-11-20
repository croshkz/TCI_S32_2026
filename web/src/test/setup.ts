import '@testing-library/jest-dom/vitest'
import { cleanup } from '@testing-library/react'
import { afterEach, vi } from 'vitest'
import { formulariosEnviados } from './api'

// Diferencias entre el navegador y el Request de Node que usa el entorno de test:
// - el navegador resuelve '/api/...' contra la URL de la página; Node no acepta URLs relativas.
// - el FormData de jsdom no es el de Node, así que Node lo enviaría como texto. Se guarda el
//   original para que los tests lean lo que mandó el formulario.
class RequestDelNavegador extends Request {
  constructor(entrada: RequestInfo | URL, init?: RequestInit) {
    super(typeof entrada === 'string' ? new URL(entrada, window.location.origin) : entrada, init)
    if (init?.body instanceof FormData) formulariosEnviados.set(this, init.body)
  }
}

// openapi-fetch guarda las referencias a fetch y Request al crear el cliente, así que
// se reemplazan acá, antes de que cualquier test importe src/api/client.ts.
vi.stubGlobal('Request', RequestDelNavegador)
vi.stubGlobal('fetch', vi.fn())

afterEach(() => {
  cleanup()
  vi.mocked(fetch).mockReset()
  sessionStorage.clear()
})
