import { useEffect, useState } from 'react'
import {
  cerrarSesion,
  ETIQUETAS_ROL,
  EVENTO_SESION_VENCIDA,
  obtenerHealth,
  usuarioActual,
  type Usuario,
} from './api/client'
import Incidencia from './pages/Incidencia'
import RegistrarUso from './pages/RegistrarUso'
import CargarStock from './pages/CargarStock'
import Login from './pages/Login'

const VISTAS = [
  { id: 'incidencia', etiqueta: 'Incidencia', titulo: 'Registro de Incidencia', Componente: Incidencia },
  { id: 'uso-repuesto', etiqueta: 'Registrar uso', titulo: 'Registrar uso de repuesto', Componente: RegistrarUso },
  { id: 'carga-stock', etiqueta: 'Cargar stock', titulo: 'Cargar stock', Componente: CargarStock },
] as const

type EstadoServicio = 'verificando' | 'ok' | 'caido'

function vistaDesdeHash() {
  const nombre = location.hash.slice(1)
  return VISTAS.find((vista) => vista.id === nombre) ?? VISTAS[0]
}

export default function App() {
  const [vista, setVista] = useState(vistaDesdeHash)
  const [servicio, setServicio] = useState<EstadoServicio>('verificando')
  const [usuario, setUsuario] = useState<Usuario | null>(usuarioActual)
  const [aviso, setAviso] = useState<string | null>(null)

  function ingresar(nuevo: Usuario) {
    setAviso(null)
    setUsuario(nuevo)
  }

  function salir() {
    cerrarSesion()
    setUsuario(null)
  }

  useEffect(() => {
    const alVencer = () => {
      setUsuario(null)
      setAviso('Tu sesión venció. Volvé a ingresar.')
    }
    window.addEventListener(EVENTO_SESION_VENCIDA, alVencer)
    return () => window.removeEventListener(EVENTO_SESION_VENCIDA, alVencer)
  }, [])

  useEffect(() => {
    const alCambiarHash = () => setVista(vistaDesdeHash())
    window.addEventListener('hashchange', alCambiarHash)
    return () => window.removeEventListener('hashchange', alCambiarHash)
  }, [])

  useEffect(() => {
    document.title = usuario ? vista.titulo : 'Ingresar'
  }, [vista, usuario])

  useEffect(() => {
    obtenerHealth()
      .then((health) => setServicio(health.status === 'ok' ? 'ok' : 'caido'))
      .catch(() => setServicio('caido'))
  }, [])

  const { Componente } = vista

  const pie = (
    <footer>
      <p className={`estado-servicio estado-${servicio}`} role="status">
        Servicio: {servicio === 'verificando' ? 'verificando…' : servicio === 'ok' ? 'en línea' : 'sin conexión'}
      </p>
      <p>Turno tarde</p>
      <p>- GRUPO 3 - Desarrollo de Software - S32 - UTN -</p>
      <p>- HERNANDEZ - HRYNKIEWICZ - HURST -</p>
    </footer>
  )

  if (!usuario) {
    return (
      <div className="app-container">
        <header>
          <h1>Ingresar</h1>
        </header>
        <main>
          <Login onIngreso={ingresar} aviso={aviso} />
        </main>
        {pie}
      </div>
    )
  }

  return (
    <div className="app-container">
      <header>
        <h1>{vista.titulo}</h1>
        <div className="sesion-usuario">
          <span>
            {usuario.nombre} · {ETIQUETAS_ROL[usuario.rol]}
          </span>
          <button type="button" className="btn-secundario" onClick={salir}>
            Salir
          </button>
        </div>
        <nav aria-label="Navegación principal">
          <ul>
            {VISTAS.map((item) => (
              <li key={item.id}>
                <a href={`#${item.id}`} aria-current={item.id === vista.id ? 'page' : undefined}>
                  {item.etiqueta}
                </a>
              </li>
            ))}
          </ul>
        </nav>
      </header>

      <main>
        <Componente key={`${vista.id}-${usuario.rol}`} />
      </main>

      {pie}
    </div>
  )
}
