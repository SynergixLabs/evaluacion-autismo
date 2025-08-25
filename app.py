import streamlit as st
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="Evaluación Autismo - SynergixLabs",
    page_icon="❤️",
    layout="centered"
)

# --- TÍTULO ---
st.markdown("<h1 style='text-align: center;'>❤️ Evaluación de Rasgos del Espectro Autista</h1>", unsafe_allow_html=True)

# --- ADVERTENCIA ---
st.markdown("""
<div style='text-align: center; margin-bottom: 20px; color: #7f8c8d; font-size: 14px;'>
    <em>Esta herramienta es orientativa y no sustituye un diagnóstico profesional.</em>
</div>
""", unsafe_allow_html=True)

# --- DATOS DEL NIÑO/A ---
st.subheader("📋 Datos del niño/a")
col1, col2 = st.columns(2)
nombre = col1.text_input("Nombre del niño/a", placeholder="Ej: Juan")
edad = col2.number_input("Edad", min_value=1, max_value=18, value=5)

rol = st.radio(
    "¿Quién está realizando la evaluación?",
    ("Padre / Tutor", "Maestro / Docente"),
    index=0,
    label_visibility="collapsed"
)

# --- PREGUNTAS ---
preguntas = [
    "¿Evita el contacto visual o tiene dificultad para mantenerlo?",
    "¿Muestra expresiones faciales limitadas o inapropiadas?",
    "¿Tiene dificultad para entender los sentimientos de los demás?",
    "¿Prefiere jugar solo en lugar de con otros niños?",
    "¿Tiene intereses intensos y muy específicos?",
    "¿Se molesta mucho por cambios pequeños en la rutina?",
    "¿Repite acciones o movimientos una y otra vez (aletear manos, balanceándose)?",
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
        si = st.button("✅ Sí", key=f"si_{st.session_state.indice}", type="primary")
    with col2:
        no = st.button("❌ No", key=f"no_{st.session_state.indice}")

    if si:
        st.session_state.respuestas.append("SI")
        st.session_state.puntaje += 1
        st.session_state.indice += 1
        st.experimental_rerun()

    if no:
        st.session_state.respuestas.append("NO")
        st.session_state.indice += 1
        st.experimental_rerun()

# Mostrar resultados
else:
    st.balloons()
    st.header("📊 Resultados de la Evaluación")

    # Datos del niño
    if nombre:
        st.markdown(f"**👤 Nombre:** {nombre}")
    else:
        st.markdown("**👤 Nombre:** No especificado")
    st.markdown(f"**🎂 Edad:** {edad} años")
    st.markdown(f"**🧑‍💼 Evaluado por:** {rol}")
    st.markdown("---")

    total = len(preguntas)
    porcentaje = (st.session_state.puntaje / total) * 100

    # Mostrar puntaje con color
    if porcentaje <= 20:
        st.success(f"✅ **Puntaje:** {st.session_state.puntaje}/{total} ({porcentaje:.1f}%)")
        st.info("🔹 **Muy bajo riesgo.** El niño/a muestra pocos rasgos asociados al autismo.")
        nivel = "Muy bajo riesgo"
    elif porcentaje <= 40:
        st.info(f"🟡 **Puntaje:** {st.session_state.puntaje}/{total} ({porcentaje:.1f}%)")
        st.warning("🔹 **Bajo riesgo.** Se recomienda observación continua.")
        nivel = "Bajo riesgo"
    elif porcentaje <= 60:
        st.warning(f"🟠 **Puntaje:** {st.session_state.puntaje}/{total} ({porcentaje:.1f}%)")
        st.error("🔹 **Riesgo moderado.** Se recomienda evaluación profesional.")
        nivel = "Riesgo moderado"
    elif porcentaje <= 80:
        st.error(f"🔴 **Puntaje:** {st.session_state.puntaje}/{total} ({porcentaje:.1f}%)")
        st.markdown("🔹 **Alto riesgo.** Se recomienda evaluación profesional lo antes posible.")
        nivel = "Alto riesgo"
    else:
        st.error(f"🚨 **Puntaje:** {st.session_state.puntaje}/{total} ({porcentaje:.1f}%)")
        st.markdown("🔹 **Muy alto riesgo.** Es altamente recomendable una evaluación completa.")
        nivel = "Muy alto riesgo"

    # --- RECOMENDACIONES ---
    if porcentaje <= 20:
        recomendaciones = """- Muy pocos indicadores del espectro autista.
- Continúe observando con naturalidad.
- Fomente el juego compartido y la comunicación.
- No hay urgencia de intervención especializada."""
    elif porcentaje <= 40:
        recomendaciones = """- Algunos rasgos asociados al autismo.
- Registre los comportamientos que le llaman la atención.
- Hable con el pediatra o maestro.
- Inicie rutinas visuales simples."""
    elif porcentaje <= 60:
        recomendaciones = """- Varios rasgos del espectro autista.
- Se recomienda atención especializada.
- Use pictogramas ARASAAC.
- Establezca una rutina visual diaria."""
    elif porcentaje <= 80:
        recomendaciones = """- Número significativo de rasgos del autismo.
- Es muy recomendable una evaluación profesional.
- Busque ayuda en centros de salud pública.
- Identifique intereses especiales y úselos."""
    else:
        recomendaciones = """- Patrón claro de características del autismo.
- Se recomienda una evaluación profesional inmediata.
- Priorice la comunicación: imágenes, gestos, apps.
- Proteja al niño/a de situaciones de exclusión."""

    # --- MOSTRAR RESULTADO FINAL ---
    st.markdown("### 📄 Resultado Final")

    st.markdown(f"""
**Nivel de riesgo:** {nivel}

**Recomendaciones:**
{recomendaciones}

---

💡 **¿Qué hacer ahora?**  
Puedes copiar este resultado y mostrarlo a un especialista (pediatra, neuropsicólogo, terapeuta).
    """)

    # --- BOTÓN REINICIAR ---
    if st.button("🔄 Realizar otra evaluación", key="reiniciar"):
        st.session_state.clear()
        st.experimental_rerun()
