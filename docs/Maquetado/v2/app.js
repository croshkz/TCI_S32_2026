console.log("app.js cargado ✅")

const form = document.querySelector("#form-incidencia");

console.log(form);

const codigoInput = document.querySelector("#codigo-maquina");
const btnEnviar = document.querySelector("#btn-enviar");

function actualizarBoton() {
  btnEnviar.disabled = codigoInput.value.trim() === ""; //trim elimina espacios antes y dsp del string//
}
codigoInput.addEventListener("input", actualizarBoton);
actualizarBoton(); //deshabilita el botón enviar del formulario

form.addEventListener("submit", (event) => {
	event.preventDefault()
	const incidencia = {
  codigoMaquina: document.querySelector("#codigo-maquina").value,
  descripcion: document.querySelector("#descripcion").value,
  turno: document.querySelector("#turno").value,
  };
  renderizarPreview(incidencia);
  console.table(incidencia);
  const preview = document.querySelector("#preview-incidencia");
  preview.hidden = false;
  form.reset();
  document.querySelector("#codigo-maquina").focus(); //pone cursor en el primer campo del formulario
  actualizarBoton() //deshabilita nuevamente el botón enviar al vaciar el formulario
});

function renderizarPreview(incidencia)  {
const contenedor = document.querySelector("#preview-incidencia");
const NOMBRES_TURNO = { manana: "Mañana", tarde: "Tarde", noche: "Noche" };
const turnoLegible = NOMBRES_TURNO[incidencia.turno] ?? incidencia.turno;
contenedor.textContent = `Incidencia registrada: ${incidencia.codigoMaquina} · Turno ${turnoLegible}\n Descripción: ${incidencia.descripcion}`;
contenedor.style.whiteSpace = "pre-line";   // fuerza el salto de linea de descripción //
}

console.log ("fin")