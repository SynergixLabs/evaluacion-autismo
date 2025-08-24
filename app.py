import streamlit as st
import requests
from io import BytesIO
from PIL import Image
import time
from datetime import datetime
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.graphics.barcode import qr

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
        nivel = "Muy bajo"
        box_class = "success-box"
    elif porcentaje <= 40:
        st.info(f"🟡 **Puntaje:** {st.session_state.puntaje}/{total} ({porcentaje:.1f}%)")
        st.warning("🔹 **Bajo riesgo.** Se recomienda observación continua.")
        nivel = "Bajo"
        box_class = "warning-box"
    elif porcentaje <= 60:
        st.warning(f"🟠 **Puntaje:** {st.session_state.puntaje}/{total} ({porcentaje:.1f}%)")
        st.error("🔹 **Riesgo moderado.** Se recomienda evaluación profesional.")
        nivel = "Moderado"
        box_class = "warning-box"
    elif porcentaje <= 80:
        st.error(f"🔴 **Puntaje:** {st.session_state.puntaje}/{total} ({porcentaje:.1f}%)")
        st.markdown("🔹 **Alto riesgo.** Se recomienda evaluación profesional lo antes posible.")
        nivel = "Alto"
        box_class = "danger-box"
    else:
        st.error(f"🚨 **Puntaje:** {st.session_state.puntaje}/{total} ({porcentaje:.1f}%)")
        st.markdown("🔹 **Muy alto riesgo.** Es altamente recomendable una evaluación completa.")
        nivel = "Muy alto"
        box_class = "danger-box"

    # --- RECOMENDACIONES (para el PDF) ---
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
{recomendaciones}

Gracias por usar esta herramienta.
SynergixLabs 💙
"""

    st.markdown("### 📄 Copia este resultado (para guardar o imprimir):")
    st.markdown(f"<div class='{box_class}'>{resultado_texto}</div>", unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align: center; margin: 20px 0; color: #7f8c8d; font-size: 14px;">
        🔽 Puedes seleccionar todo el texto, copiarlo (Ctrl+C) y pegarlo en un documento de Word o PDF.
    </div>
    """, unsafe_allow_html=True)

    # --- GENERAR FOLIO ---
    folio = int(time.time()) % 10000
    fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M")

    # --- GENERAR PDF INTERACTIVO ---
    def generar_pdf():
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        # --- Encabezado ---
        c.setFillColor(colors.HexColor("#8e44ad"))
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(width / 2, height - 80, "❤️ Evaluación de Rasgos del Espectro Autista")
        c.setFont("Helvetica", 10)
        c.setFillColor(colors.grey)
        c.drawCentredString(width / 2, height - 100, "Orientativa – No sustituye diagnóstico profesional")
        c.setFillColor(colors.black)

        # --- Información del niño ---
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, height - 140, f"📄 Folio: #{folio}")
        c.drawString(250, height - 140, f"📅 Fecha: {fecha_hora}")
        c.drawString(50, height - 160, f"👤 Nombre: {nombre if nombre else 'No especificado'}")
        c.drawString(250, height - 160, f"🎂 Edad: {edad} años")
        c.drawString(450, height - 160, f"🧑‍ Evaluado por: {rol}")

        # --- Resultados ---
        c.setStrokeColor(colors.HexColor("#e74c3c"))
        c.setLineWidth(1)
        c.rect(45, height - 320, width - 90, 140, fill=0)

        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(colors.HexColor("#2980B9"))
        c.drawString(60, height - 300, "📊 Resultados")
        c.setFont("Helvetica", 11)
        c.setFillColor(colors.black)
        c.drawString(80, height - 320, f"Puntaje: {st.session_state.puntaje}/{total} ({porcentaje:.1f}%)")
        c.setFillColor(colors.red if nivel in ["Alto", "Muy alto"] else 
                       colors.orange if nivel == "Moderado" else colors.green)
        c.drawString(80, height - 340, f"Nivel de riesgo: {nivel}")

        # --- Recomendaciones ---
        c.setFillColor(colors.HexColor("#27AE60"))
        c.setFont("Helvetica-Bold", 12)
        c.drawString(60, height - 370, "🌱 Recomendaciones")
        text = c.beginText(80, height - 390)
        text.setFont("Helvetica", 10)
        for line in recomendaciones.split("\n"):
            if line.strip():
                text.textLine(line.strip())
        c.drawText(text)

        # --- QR ---
        web_link = "https://synergixlabs-evaluacion-autismo.streamlit.app"
        qr_code = qr.QrCodeWidget(web_link)
        bounds = qr_code.getBounds()
        size = 100
        width_qr = bounds[2] - bounds[0]
        height_qr = bounds[3] - bounds[1]
        d = qr_code.draw()
        d.scale(size / width_qr, size / height_qr)
        d.drawOn(c, width - 150, 80)

        # --- Enlace clickeable ---
        c.setFont("Helvetica", 9)
        c.setFillColor(colors.HexColor("#2980B9"))
        c.drawString(50, 70, web_link)
        c.linkURL(web_link, (50, 65, 300, 80), relative=1)

        # --- Firma ---
        c.setFillColor(colors.black)
        c.drawString(50, 40, "_________________________")
        c.drawString(70, 25, "Firma del evaluador")

        # --- Guardar PDF ---
        c.save()
        buffer.seek(0)
        return buffer

    # --- BOTÓN DESCARGAR PDF ---
    pdf_buffer = generar_pdf()

    st.download_button(
        label="📥 Descargar PDF profesional (QR + enlace)",
        data=pdf_buffer,
        file_name=f"evaluacion_autismo_{folio}.pdf",
        mime="application/pdf"
    )

    # --- BOTÓN REINICIAR ---
    if st.button("🔄 Realizar otra evaluación", key="reiniciar"):
        st.session_state.clear()
        st.rerun()
