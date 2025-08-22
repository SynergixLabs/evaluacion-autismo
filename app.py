import streamlit as st
import requests
from io import BytesIO
from PIL import Image

# Configuración de la página
st.set_page_config(
    page_title="Evaluación Autismo - SynergixLabs",
    page_icon="❤️",
    layout="centered"
)

# Estilos CSS
st.markdown("""
<style>
    body {
        background-color: #fffaf0;
        font-family: 'Segoe UI', sans-serif;
        color: #2c3e50;
    }
    h1, h2, h3 {
        color: #8e44ad;
        text-align: center;
    }
    .stButton>button {
        border-radius: 12px;
        padding: 12px 24px;
        font-size: 16px;
        margin: 10px;
        width: 120px;
    }
    .info-box {
        background-color: #f8f9fa;
        border-left: 5px solid #e74c3c;
        padding: 15px;
        margin: 20px 0;
        border-radius: 8px;
        font-family: monospace;
        white-space: pre-wrap;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

# --- TÍTULO Y LOGO ---
st.markdown("<h1 style='text-align: center;'>❤️ Evaluación de Rasgos del Espectro Autista</h1>", unsafe_allow_html=True)

# Logo de SynergixLabs (clickeable)
logo_url = "https://raw.githubusercontent.com/synergixlabs/evaluacion-autismo/main/synergixlabs.png"
link_url = "https://github.com/synergixlabs"

st.markdown(f"""
<div style="text-align: center; margin: 20px 0;">
    <a href="{link_url}" target="_blank">
        <img src="{logo_url}" alt="SynergixLabs" width="160" 
             style="border-radius: 12px; box-shadow: 0px 4px 8px rgba(0,0,0,0.1);">
    </a>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; margin-bottom: 20px; color: #7f8c8d; font-size: 14px;'>
    <em>Esta herramienta es orientativa y no sustituye un diagnóstico profesional.</em>
</div>
""", unsafe_allow_html=True)

# --- DATOS DEL NIÑO/A ---
st.subheader("Datos del niño/a")
col1, col2 = st.columns(2)
nombre = col1.text_input("Nombre del niño/a")
edad = col2.number_input("Edad", min_value=1, max_value=18, value=5)

rol = st.radio(
    "¿Quién está realizando la evaluación?",
    ("Padre / Tutor", "Maestro / Docente"),
    index=0
)

# --- PREGUNTAS ---
preguntas = [
    "¿Evita el contacto visual o tiene dificultad para mantenerlo?",
    "¿Muestra expresiones faciales limitadas o inapropiadas?",
    "¿Tiene dificultad para entender los sentimientos de los demás?",
    "¿Prefiere jugar solo en lugar de con otros niños?",
    "¿Tiene intereses intensos y muy específicos?",
    "¿Se molesta mucho por cambios pequeños en la rutina?",
    "¿Repite acciones o movimientos una y otra vez (aletear manos, balancearse)?",
    "¿Responde inusualmente a sonidos, texturas, olores o sabores?",
    "¿Tiene dificultad para adaptarse a cambios de ambiente?",
    "¿Tiene retrasos en el desarrollo del lenguaje?",
    "¿Usa lenguaje literal (dificultad para entender bromas o sarcasmo)?",
    "¿Repite palabras o frases (ecolalia)?",
    "¿Tiene dificultad para iniciar o mantener conversaciones?",
    "¿Parece no compartir disfrute o intereses con otros?",
    "¿Muestra apego inusual a objetos específicos?",
    "¿Tiene patrones de juego repetitivos o ritualistas?",
    "¿Tiene dificultad para hacer amigos de su misma edad?",
    "¿Parece no notar cuando otros hablan con él/ella?",
    "¿Tiene rabietas intensas o reacciones emocionales desproporcionadas?",
    "¿Tiene dificultad para comprender instrucciones múltiples?",
    "¿Muestra poca conciencia del peligro?",
    "¿Tiene patrones de sueño inusuales o problemas para dormir?",
    "¿Camina de puntillas o tiene patrones de movimiento inusuales?",
    "¿Se concentra intensamente en partes de objetos (ej: ruedas de coches)?",
    "¿Tiene dificultad para comprender gestos o lenguaje corporal?",
    "¿Muestra ansiedad en entornos sociales?",
    "¿Tiene memoria excepcional para detalles específicos?",
    "¿Muestra selectividad alimentaria extrema?",
    "¿Tiene dificultad para manejar la frustración?",
    "¿Muestra poca variedad en actividades espontáneas?"
]

# Inicializar respuestas
if 'respuestas' not in st.session_state:
    st.session_state.respuestas = []
    st.session_state.indice = 0
    st.session_state.puntaje = 0

# Mostrar progreso
def mostrar_progreso():
    progreso = st.session_state.indice / len(preguntas)
    st.progress(progreso)
    st.caption(f"Pregunta {st.session_state.indice + 1} de {len(preguntas)}")

# Mostrar pregunta actual
if st.session_state.indice < len(preguntas):
    mostrar_progreso()
    st.subheader(f"Pregunta {st.session_state.indice + 1}")
    st.write(preguntas[st.session_state.indice])

    col1, col2 = st.columns(2)
    with col1:
        si = st.button("✅ Sí", key=f"si_{st.session_state.indice}")
    with col2:
        no = st.button("❌ No", key=f"no_{st.session_state.indice}")

    if si:
        st.session_state.respuestas.append("SI")
        st.session_state.puntaje += 1
        st.session_state.indice += 1
        st.rerun()

    if no:
        st.session_state.respuestas.append("NO")
        st.session_state.indice += 1
        st.rerun()

# Mostrar resultados
else:
    st.balloons()
    st.header("📊 Resultados de la Evaluación")

    # Mostrar datos del niño
    st.markdown(f"**Nombre:** {nombre}")
    st.markdown(f"**Edad:** {edad} años")
    st.markdown(f"**Evaluado por:** {rol}")
    st.markdown("---")

    total = len(preguntas)
    porcentaje = (st.session_state.puntaje / total) * 100

    # Mostrar puntaje
    st.markdown(f"**Puntaje:** {st.session_state.puntaje}/{total} ({porcentaje:.1f}%)")

    # Nivel de riesgo
    if porcentaje <= 20:
        nivel = "Muy bajo riesgo"
        color = "green"
    elif porcentaje <= 40:
        nivel = "Bajo riesgo"
        color = "orange"
    elif porcentaje <= 60:
        nivel = "Riesgo moderado"
        color = "orange"
    elif porcentaje <= 80:
        nivel = "Alto riesgo"
        color = "red"
    else:
        nivel = "Muy alto riesgo"
        color = "red"

    st.markdown(f"**Nivel de riesgo:** <span style='color:{color}; font-weight:bold;'>{nivel}</span>", unsafe_allow_html=True)

    # Resultado para copiar
    resultado_texto = f"""
RESULTADO DE LA EVALUACIÓN
----------------------------
Nombre: {nombre}
Edad: {edad} años
Rol del evaluador: {rol}
Puntaje: {st.session_state.puntaje}/{total}
Porcentaje: {porcentaje:.1f}%
Nivel de riesgo: {nivel}

Recomendaciones:
"""

    if porcentaje <= 20:
        resultado_texto += """
- Muy pocos indicadores del espectro autista.
- Continúe observando con naturalidad.
- Fomente el juego compartido.
"""
    elif porcentaje <= 40:
        resultado_texto += """
- Algunos rasgos asociados al autismo.
- Registre comportamientos para seguimiento.
- Comparta sus observaciones con el pediatra.
"""
    elif porcentaje <= 60:
        resultado_texto += """
- Varios rasgos del espectro autista.
- Se recomienda evaluación profesional.
- Use rutinas visuales y pictogramas.
"""
    elif porcentaje <= 80:
        resultado_texto += """
- Patrón claro de rasgos del autismo.
- Busque evaluación especializada.
- Documente comportamientos para el especialista.
"""
    else:
        resultado_texto += """
- Muy alto riesgo de trastorno del espectro autista.
- Priorice una evaluación profesional inmediata.
- Proteja al niño/a de situaciones de exclusión.
"""

    resultado_texto += "\nGracias por usar esta herramienta. SynergixLabs 💙"

    # Mostrar resultado para copiar
    st.markdown("### 📄 Copia este resultado (para imprimir o guardar):")
    st.markdown(f"<div class='info-box'>{resultado_texto}</div>", unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align: center; margin: 20px 0; color: #7f8c8d; font-size: 14px;">
        Puedes seleccionar todo el texto, copiarlo (Ctrl+C) y pegarlo en un documento de Word o PDF.
    </div>
    """, unsafe_allow_html=True)

    # Botón para reiniciar
    if st.button("Realizar otra evaluación"):
        st.session_state.clear()
        st.rerun()
