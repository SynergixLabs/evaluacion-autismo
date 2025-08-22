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
        padding: 12px 28px;
        font-size: 16px;
        margin: 10px;
        width: 120px;
        font-weight: bold;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        transition: 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)

# --- LOGOS SUPERIORES: SynergixLabs (izquierda) y Corazón (centro) ---
col1, col2, col3 = st.columns([1, 2, 1])

# Logo de SynergixLabs (izquierda)
try:
    synergix_url = "https://raw.githubusercontent.com/synergixlabs/evaluacion-autismo/main/synergixlabs.png"
    response = requests.get(synergix_url, timeout=10)
    synergix_logo = Image.open(BytesIO(response.content))
    with col1:
        st.image(synergix_logo, width=140)
except Exception as e:
    with col1:
        st.write("")

# Corazón (centro)
try:
    corazon_url = "https://raw.githubusercontent.com/synergixlabs/evaluacion-autismo/main/corazon.png"
    response = requests.get(corazon_url, timeout=10)
    corazon_logo = Image.open(BytesIO(response.content))
    with col2:
        st.image(corazon_logo, width=160)
except Exception as e:
    with col2:
        st.write("")

# --- TÍTULO ---
st.markdown("<h1 style='text-align: center;'>❤️ Evaluación de Rasgos del Espectro Autista</h1>", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; margin-bottom: 20px;'>
    <em>Esta herramienta es orientativa y no sustituye un diagnóstico profesional.</em><br>
    <strong>Dirigida a padres, madres y maestros.</strong>
</div>
""", unsafe_allow_html=True)

# Selección de rol
rol = st.radio(
    "¿Quién está realizando la evaluación?",
    ("Padre / Tutor", "Maestro / Docente"),
    index=0,
    label_visibility="collapsed"
)

# Preguntas
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

# Inicializar variables
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
        si = st.button("✅ Sí", key=f"si_{st.session_state.indice}", type="primary")
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
    st.header("📊 Resultados")
    
    total = len(preguntas)
    porcentaje = (st.session_state.puntaje / total) * 100

    if porcentaje <= 20:
        st.success(f"Puntaje: {st.session_state.puntaje}/{total} ({porcentaje:.1f}%)")
        st.info("🔹 **Muy pocos indicadores**. El niño/a muestra pocos rasgos asociados al autismo.")
    elif porcentaje <= 40:
        st.info(f"Puntaje: {st.session_state.puntaje}/{total} ({porcentaje:.1f}%)")
        st.warning("🔹 **Algunos rasgos, bajo riesgo**. Se recomienda observación continua.")
    elif porcentaje <= 60:
        st.warning(f"Puntaje: {st.session_state.puntaje}/{total} ({porcentaje:.1f}%)")
        st.error("🔹 **Riesgo moderado**. Se recomienda evaluación profesional.")
    elif porcentaje <= 80:
        st.error(f"Puntaje: {st.session_state.puntaje}/{total} ({porcentaje:.1f}%)")
        st.markdown("🔹 **Alto riesgo**. Se recomienda evaluación profesional lo antes posible.")
    else:
        st.error(f"Puntaje: {st.session_state.puntaje}/{total} ({porcentaje:.1f}%)", icon="🚨")
        st.markdown("🔹 **Muy alto riesgo**. Es altamente recomendable una evaluación completa.")

    # Apoyo humano
    st.markdown("---")
    st.header("🌱 Apoyo para familias y educadores")

    if rol == "Padre / Tutor":
        st.markdown("""
        - 📌 Lleve un diario de comportamientos y fortalezas.
        - 📌 Use rutinas visuales en casa (levantarse, comer, dormir).
        - 📌 Busque ayuda en centros de salud pública u ONGs.
        - 📌 Únase a grupos de padres en Facebook o WhatsApp.
        - 💡 **Recurso gratuito**: pictogramas ARASAAC (busque en Google).
        """)
    else:
        st.markdown("""
        - 📌 Observe cómo sigue instrucciones y se relaciona con compañeros.
        - 📌 Use pictogramas o tarjetas de emociones en clase.
        - 📌 Asigne un compañero de apoyo amable.
        - 📌 Comuníquese con los padres con empatía y respeto.
        - 💡 **Recurso gratuito**: Canal 'Neuronilla' en YouTube.
        """)

    st.markdown("<div style='text-align: center; margin-top: 20px; font-size: 16px;'>Gracias por dedicar tiempo a entender mejor a este niño/a. ❤️</div>", unsafe_allow_html=True)

    # --- PIE DE PÁGINA: Apoyo de SynergixLabs ---
    st.markdown("---")
    st.markdown("<div style='text-align: center; font-size: 16px;'>Esta herramienta es un apoyo comunitario de:</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    try:
        synergix_url = "https://raw.githubusercontent.com/synergixlabs/evaluacion-autismo/main/synergixlabs.png"
        response = requests.get(synergix_url, timeout=10)
        synergix_logo = Image.open(BytesIO(response.content))
        with col2:
            st.image(synergix_logo, width=180)
    except Exception as e:
        st.markdown("<div style='text-align: center;'>SynergixLabs</div>", unsafe_allow_html=True)

    st.markdown("<div style='text-align: center; font-size: 14px; color: #7f8c8d;'>Juntos por una comunidad más inclusiva. 💙</div>", unsafe_allow_html=True)

    # Botón para reiniciar
    if st.button("Realizar otra evaluación"):
        st.session_state.clear()
        st.rerun()
