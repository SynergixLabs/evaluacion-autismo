import streamlit as st
import time

# Configuración de la página
st.set_page_config(
    page_title="🧠 Evaluación Autismo",
    page_icon="🧠",
    layout="centered"
)

# Título principal
st.title("🧠 Evaluación de Rasgos del Espectro Autista")
st.markdown("""
Esta herramienta es **orientativa** y no sustituye un diagnóstico profesional.  
Dirigida a padres, madres y maestros.
""")

# Selección de rol
rol = st.radio(
    "¿Quién está realizando la evaluación?",
    ("Padre / Tutor", "Maestro / Docente")
)

# Preguntas (sin caracteres problemáticos, en UTF-8)
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

# Inicializar variables en session_state
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
    st.header("📊 Resultados")
    
    total = len(preguntas)
    porcentaje = (st.session_state.puntaje / total) * 100

    # Mostrar puntaje con color
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

    # Mensaje de apoyo humano
    st.markdown("---")
    st.header("🌱 Apoyo para familias y educadores")

    if rol == "Padre / Tutor":
        st.markdown("""
        - 📌 Lleve un diario de comportamientos y fortalezas.
        - 📌 Use rutinas visuales en casa (levantarse, comer, dormir).
        - 📌 Busque ayuda en centros de salud pública o ONGs.
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

    st.markdown("Gracias por dedicar tiempo a entender mejor a este niño/a. 💙")

    # Botón para reiniciar
    if st.button("Realizar otra evaluación"):
        st.session_state.clear()
        st.rerun()