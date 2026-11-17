import { useState, type FormEvent } from 'react'
import { iniciarSesion, type Usuario } from '../api/client'

type Props = { onIngreso: (usuario: Usuario) => void; aviso?: string | null }

export default function Login({ onIngreso, aviso }: Props) {
  const [usuario, setUsuario] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [enviando, setEnviando] = useState(false)

  async function ingresar(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault()
    setEnviando(true)
    setError(null)
    try {
      onIngreso(await iniciarSesion(usuario.trim(), password))
    } catch (motivo) {
      setError(motivo instanceof Error ? motivo.message : 'No se pudo iniciar sesión.')
      setPassword('')
    } finally {
      setEnviando(false)
    }
  }

  return (
    <section className="vista">
      {aviso && <div className="mensaje-aviso" role="status">{aviso}</div>}
      <form onSubmit={ingresar}>
        <div className="campo">
          <label htmlFor="login-usuario">Usuario</label>
          <input
            type="text"
            id="login-usuario"
            autoComplete="username"
            value={usuario}
            onChange={(evento) => setUsuario(evento.target.value)}
            required
            autoFocus
          />
        </div>

        <div className="campo">
          <label htmlFor="login-password">Contraseña</label>
          <input
            type="password"
            id="login-password"
            autoComplete="current-password"
            value={password}
            onChange={(evento) => setPassword(evento.target.value)}
            required
          />
        </div>

        <button type="submit" className="btn-principal" disabled={enviando}>
          {enviando ? 'Ingresando…' : 'Ingresar'}
        </button>
      </form>

      {error && (
        <div className="mensaje-error" role="alert">
          <p>{error}</p>
        </div>
      )}
    </section>
  )
}
