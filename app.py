import streamlit as st
from io import BytesIO
from PIL import Image
import time
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="Evaluación Autismo - SynergixLabs",
    page_icon="❤️",
    layout="centered"
)

# --- OCULTAR ICONO ↔ Y ESTILOS ---
st.markdown("""
<style>
    /* Ocultar el icono ↔ en títulos */
    h1::after, h2::after, h3::after, h4::after, h5::after, h6::after {
        content: none !important;
        display: none !important;
    }
    /* Ocultar el expander de Streamlit */
    .stExpander > div > div > span {
        display: none !important;
    }
    /* Estilos generales */
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
    .stProgress > div > div > div {
        background-color: #e74c3c;
    }
    .info-box {
        background-color: #f8f9fa;
        border-left: 6px solid #e74c3c;
        padding: 16px;
        margin: 20px 0;
        border-radius: 8px;
        font-family: 'Courier New', monospace;
        white-space: pre-wrap;
        font-size: 15px;
        color: #2c3e50;
    }
    .success-box {
        background-color: #dfffdf;
        border-left: 6px solid #27ae60;
        padding: 16px;
        margin: 20px 0;
        border-radius: 8px;
        font-family: 'Courier New', monospace;
        white-space: pre-wrap;
        font-size: 15px;
    }
    .warning-box {
        background-color: #fff9e6;
        border-left: 6px solid #f39c12;
        padding: 16px;
        margin: 20px 0;
        border-radius: 8px;
        font-family: 'Courier New', monospace;
        white-space: pre-wrap;
        font-size: 15px;
    }
    .danger-box {
        background-color: #ffe6e6;
        border-left: 6px solid #c0392b;
        padding: 16px;
        margin: 20px 0;
        border-radius: 8px;
        font-family: 'Courier New', monospace;
        white-space: pre-wrap;
        font-size: 15px;
        color: #c0392b;
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
        st.rerun()

    if no:
        st.session_state.respuestas.append("NO")
        st.session_state.indice += 1
        st.rerun()

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
        box_class = "success-box"
    elif porcentaje <= 40:
        st.info(f"🟡 **Puntaje:** {st.session_state.puntaje}/{total} ({porcentaje:.1f}%)")
        st.warning("🔹 **Bajo riesgo.** Se recomienda observación continua.")
        nivel = "Bajo riesgo"
        box_class = "warning-box"
    elif porcentaje <= 60:
        st.warning(f"🟠 **Puntaje:** {st.session_state.puntaje}/{total} ({porcentaje:.1f}%)")
        st.error("🔹 **Riesgo moderado.** Se recomienda evaluación profesional.")
        nivel = "Riesgo moderado"
        box_class = "warning-box"
    elif porcentaje <= 80:
        st.error(f"🔴 **Puntaje:** {st.session_state.puntaje}/{total} ({porcentaje:.1f}%)")
        st.markdown("🔹 **Alto riesgo.** Se recomienda evaluación profesional lo antes posible.")
        nivel = "Alto riesgo"
        box_class = "danger-box"
    else:
        st.error(f"🚨 **Puntaje:** {st.session_state.puntaje}/{total} ({porcentaje:.1f}%)")
        st.markdown("🔹 **Muy alto riesgo.** Es altamente recomendable una evaluación completa.")
        nivel = "Muy alto riesgo"
        box_class = "danger-box"

    # --- RESULTADO PARA COPIAR ---
    resultado_texto = f"""
RESULTADO DE LA EVALUACIÓN - SYNERGIXLABS
==========================================
Nombre: {nombre if nombre else 'No especificado'}
Edad: {edad} años
Evaluado por: {rol}
Puntaje: {st.session_state.puntaje}/{total}
Porcentaje: {porcentaje:.1f}%
Nivel de riesgo: {nivel}

Recomendaciones:
"""

    if porcentaje <= 20:
        resultado_texto += """
- Muy pocos indicadores del espectro autista.
- Continúe observando con naturalidad.
- Fomente el juego compartido y la comunicación.
- No hay urgencia de intervención especializada.
"""
    elif porcentaje <= 40:
        resultado_texto += """
- Algunos rasgos asociados al autismo.
- Registre los comportamientos que le llaman la atención.
- Hable con el pediatra o maestro.
- Inicie rutinas visuales simples.
"""
    elif porcentaje <= 60:
        resultado_texto += """
- Varios rasgos del espectro autista.
- Se recomienda atención especializada.
- Use pictogramas ARASAAC.
- Establezca una rutina visual diaria.
"""
    elif porcentaje <= 80:
        resultado_texto += """
- Número significativo de rasgos del autismo.
- Es muy recomendable una evaluación profesional.
- Busque ayuda en centros de salud pública.
- Identifique intereses especiales y úselos.
"""
    else:
        resultado_texto += """
- Patrón claro de características del autismo.
- Se recomienda una evaluación profesional inmediata.
- Priorice la comunicación: imágenes, gestos, apps.
- Proteja al niño/a de situaciones de exclusión.
"""

    resultado_texto += "\n\nGracias por usar esta herramienta.\nSynergixLabs 💙"

    # Mostrar resultado con color
    st.markdown("### 📄 Copia este resultado (para guardar o imprimir):")
    st.markdown(f"<div class='{box_class}'>{resultado_texto}</div>", unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align: center; margin: 20px 0; color: #7f8c8d; font-size: 14px;">
        🔽 Puedes seleccionar todo el texto, copiarlo (Ctrl+C) y pegarlo en un documento de Word o PDF.
    </div>
    """, unsafe_allow_html=True)

    # --- GENERAR FOLIO Y FECHA ---
    folio = int(time.time()) % 10000
    fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M")

    # --- INFORME PARA IMPRESIÓN (solo al imprimir) ---
    informe_html = f'''
    <div class="print-only">
        <div style="text-align: center; margin-bottom: 10px;">
            <img src="{logo_url}" alt="SynergixLabs" style="width: 160px; height: auto;">
            <h1 style="color: #8e44ad; margin: 10px 0;">❤️ Evaluación de Rasgos del Espectro Autista</h1>
            <p style="color: #7f8c8d; font-size: 13px; margin: 5px 0;">
                <em>Esta herramienta es orientativa y no sustituye un diagnóstico profesional.</em>
            </p>
        </div>

        <!-- FOLIO Y FECHA -->
        <div style="display: flex; justify-content: center; gap: 20px; font-size: 14px; color: #2c3e50; margin: 10px 0 15px 0; flex-wrap: wrap;">
            <div style="font-weight: bold;">📄 <strong>Folio:</strong> #{folio}</div>
            <div style="font-weight: bold;">📅 <strong>Fecha:</strong> {fecha_hora}</div>
        </div>

        <!-- LEYENDA DE ADVERTENCIA -->
        <div style="background-color: #fff3cd; color: #856404; padding: 10px 15px; border: 2px solid #ffeeba; border-radius: 8px; margin: 10px 0 15px 0; font-size: 13px; font-weight: bold; text-align: center; line-height: 1.4;">
            ⚠️ <strong>Advertencia:</strong> Esta evaluación es orientativa y no sustituye un diagnóstico profesional. El diagnóstico debe ser realizado por un especialista.
        </div>

        <hr style="border: 1px solid #e74c3c; margin: 15px 0;">

        <div style="font-size: 14px; line-height: 1.4;">
            <strong>📋 Datos del niño/a</strong>
            <p style="margin: 5px 0; padding: 0;"><strong>Nombre:</strong> {nombre if nombre else 'No especificado'}</p>
            <p style="margin: 5px 0; padding: 0;"><strong>Edad:</strong> {edad} años</p>
            <p style="margin: 5px 0; padding: 0;"><strong>Evaluado por:</strong> {rol}</p>

            <strong>📊 Resultados</strong>
            <p style="margin: 5px 0; padding: 0;"><strong>Puntaje:</strong> {st.session_state.puntaje}/{total} ({porcentaje:.1f}%)</p>
            <p style="margin: 5px 0; padding: 0;"><strong>Nivel de riesgo:</strong> <span style="color: {'#27ae60' if porcentaje <= 20 else '#f39c12' if porcentaje <= 60 else '#c0392b'}; font-weight: bold;">{nivel}</span></p>

            <strong>🌱 Recomendaciones</strong>
            <div style="background-color: #f8f9fa; padding: 12px; border-left: 5px solid #e74c3c; border-radius: 6px; font-family: Arial; font-size: 14px; line-height: 1.5; color: #2c3e50;">
{resultado_texto.strip()}
            </div>
        </div>

        <!-- CÓDIGO QR -->
        <div style="margin-top: 30px; text-align: center;">
            <div style="font-size: 14px; color: #2c3e50; font-weight: bold; margin-bottom: 8px;">Escanea para acceder a la herramienta</div>
            <img src="https://api.qrserver.com/v1/create-qr-code/?data=https%3A%2F%2Fsynergixlabs-evaluacion-autismo.streamlit.app&size=200x200&margin=10" alt="Código QR" style="width: 150px; height: 150px; border: 2px solid #e74c3c; border-radius: 8px;">
            <div style="font-size: 12px; color: #7f8c8d; margin-top: 6px;">synergixlabs-evaluacion-autismo.streamlit.app</div>
        </div>

        <!-- ESPACIO PARA FIRMA -->
        <div style="text-align: center; margin-top: 30px; font-size: 14px;">
            <p style="margin: 5px 0;"><strong>SynergixLabs 💙</strong></p>
            <div style="margin-top: 40px; font-size: 14px;">
                <div style="border-bottom: 1px solid #000; width: 300px; margin: 0 auto 8px; line-height: 0.8;">&nbsp;</div>
                <div style="color: #2c3e50; font-weight: bold;">Firma del evaluador</div>
                <div style="margin-top: 15px; display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; font-weight: bold;">
                    <div>Nombre: <span style="border-bottom: 1px solid #000; width: 250px; padding: 0 10px; display: inline-block;"></span></div>
                    <div>Fecha: <span style="border-bottom: 1px solid #000; width: 120px; padding: 0 10px; display: inline-block;"></span></div>
                </div>
            </div>
        </div>
    </div>
    '''

    # Renderizar el informe
    st.markdown(informe_html, unsafe_allow_html=True)

    # --- BOTÓN DE IMPRIMIR ---
    st.markdown("""
    <a href="javascript:window.print()" style="text-decoration: none;">
        <div style="
            text-align: center;
            background-color: #27ae60;
            color: white;
            padding: 14px 30px;
            font-size: 16px;
            font-weight: bold;
            border-radius: 12px;
            cursor: pointer;
            box-shadow: 0px 6px 12px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            display: inline-block;
            width: 80%;
            margin: 20px auto;
        "
        onmouseover="this.style.transform='scale(1.05)'; this.style.boxShadow='0px 8px 16px rgba(0,0,0,0.2)';"
        onmouseout="this.style.transform='scale(1)'; this.style.boxShadow='0px 6px 12px rgba(0,0,0,0.1)';"
        onclick="window.print(); return false;"
        >
        🖨 Imprimir resultado profesional
        </div>
    </a>
    """, unsafe_allow_html=True)

    # --- BOTÓN REINICIAR ---
    if st.button("🔄 Realizar otra evaluación", key="reiniciar"):
        st.session_state.clear()
        st.rerun()
