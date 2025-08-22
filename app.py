import streamlit as st
import requests
from io import BytesIO
from PIL import Image
from fpdf import FPDF

# Configuración de la página
st.set_page_config(
    page_title="Evaluación Autismo - SynergixLabs",
    page_icon="❤️",
    layout="centered"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    body {
        background-color: #fffaf0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
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
</style>
""", unsafe_allow_html=True)

# --- TÍTULO CON CORAZÓN ---
st.markdown("<h1 style='text-align: center; color: #8e44ad;'>❤️ Evaluación de Rasgos del Espectro Autista</h1>", unsafe_allow_html=True)

# --- LOGO DE SYNERGIXLABS CON ENLACE ---
logo_url = "https://raw.githubusercontent.com/synergixlabs/evaluacion-autismo/main/synergixlabs.png"
link_url = "https://github.com/synergixlabs"

st.markdown(f"""
<div style="text-align: center; margin: 20px 0;">
    <a href="{link_url}" target="_blank" style="text-decoration: none;">
        <img src="{logo_url}" alt="SynergixLabs" width="160" 
             style="border-radius: 12px; 
                    box-shadow: 0px 4px 8px rgba(0,0,0,0.1); 
                    transition: transform 0.3s ease; 
                    border: 2px solid #e74c3c;">
    </a>
</div>
<script>
    const img = document.querySelector('img[alt="SynergixLabs"]');
    if (img) {{
        img.addEventListener('mouseover', () => {{
            img.style.transform = 'scale(1.08)';
        }});
        img.addEventListener('mouseout', () => {{
            img.style.transform = 'scale(1)';
        }});
    }}
</script>
""", unsafe_allow_html=True)

# --- ADVERTENCIA ---
st.markdown("""
<div style='text-align: center; margin-bottom: 20px; font-size: 14px; color: #7f8c8d;'>
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
        nivel = "Muy pocos indicadores"
        recomendaciones = """- El niño/a muestra pocos rasgos asociados al autismo.
- Continúe observando su desarrollo con naturalidad.
- Fomente el juego compartido y la comunicación.
- No hay urgencia de intervención especializada por ahora."""
    elif porcentaje <= 40:
        st.info(f"Puntaje: {st.session_state.puntaje}/{total} ({porcentaje:.1f}%)")
        st.warning("🔹 **Algunos rasgos, bajo riesgo**. Se recomienda observación continua.")
        nivel = "Algunos rasgos, bajo riesgo"
        recomendaciones = """- Se observan ciertos comportamientos que podrían relacionarse con el autismo.
- Registre los comportamientos que le llaman la atención.
- Hable con el pediatra o maestro para comparar observaciones.
- Inicie rutinas visuales simples si hay dificultad con cambios."""
    elif porcentaje <= 60:
        st.warning(f"Puntaje: {st.session_state.puntaje}/{total} ({porcentaje:.1f}%)")
        st.error("🔹 **Riesgo moderado**. Se recomienda evaluación profesional.")
        nivel = "Riesgo moderado"
        recomendaciones = """- El niño/a presenta varios rasgos asociados al espectro autista.
- Se recomienda atención especializada para una evaluación más profunda.
- Use pictogramas ARASAAC para mejorar la comprensión del lenguaje.
- Establezca una rutina visual diaria."""
    elif porcentaje <= 80:
        st.error(f"Puntaje: {st.session_state.puntaje}/{total} ({porcentaje:.1f}%)")
        st.markdown("🔹 **Alto riesgo**. Se recomienda evaluación profesional lo antes posible.")
        nivel = "Alto riesgo"
        recomendaciones = """- Se observa un número significativo de rasgos del espectro autista.
- Es muy recomendable una evaluación profesional lo antes posible.
- Busque ayuda en centros de salud pública o programas de discapacidad.
- Identifique intereses especiales y úselos como herramienta de aprendizaje."""
    else:
        st.error(f"Puntaje: {st.session_state.puntaje}/{total} ({porcentaje:.1f}%)", icon="🚨")
        st.markdown("🔹 **Muy alto riesgo**. Es altamente recomendable una evaluación completa.")
        nivel = "Muy alto riesgo"
        recomendaciones = """- Se observa un patrón significativo de características del autismo.
- Se recomienda una evaluación profesional inmediata.
- Priorice la comunicación: use imágenes, gestos o aplicaciones simples.
- Proteja al niño/a de situaciones de burla o exclusión."""

    # --- APoyo HUMANO ---
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

    st.markdown(f"""
    <div style="text-align: center; margin: 15px 0;">
        <a href="{link_url}" target="_blank" style="text-decoration: none;">
            <img src="{logo_url}" alt="SynergixLabs" width="180" 
                 style="border-radius: 12px; 
                        box-shadow: 0px 4px 8px rgba(0,0,0,0.1); 
                        transition: transform 0.3s ease; 
                        border: 2px solid #e74c3c;">
        </a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='text-align: center; font-size: 14px; color: #7f8c8d;'>Juntos por una comunidad más inclusiva. 💙</div>", unsafe_allow_html=True)

    # --- GENERAR PDF CON LOGO ---
    def generar_pdf():
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)

        # Insertar logo desde URL
        try:
            response = requests.get(logo_url, timeout=10)
            response.raise_for_status()
            img = Image.open(BytesIO(response.content))
            img_byte_arr = BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)
            pdf.image(img_byte_arr, x=10, y=10, w=60)
        except Exception as e:
            pass  # No detener si falla el logo

        # Título
        pdf.set_font("Arial", "B", 16)
        pdf.set_text_color(142, 68, 173)
        pdf.cell(0, 10, "Evaluación de Rasgos del Espectro Autista", ln=True, align="C")
        pdf.ln(20)

        # Información
        pdf.set_font("Arial", "", 12)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 8, f"Rol: {rol}", ln=True)
        pdf.cell(0, 8, f"Puntaje: {st.session_state.puntaje}/{total}", ln=True)
        pdf.cell(0, 8, f"Porcentaje: {porcentaje:.1f}%", ln=True)
        pdf.cell(0, 8, f"Nivel: {nivel}", ln=True)
        pdf.ln(10)

        # Recomendaciones
        pdf.set_font("Arial", "B", 12)
        pdf.set_text_color(231, 76, 60)
        pdf.cell(0, 8, "Recomendaciones:", ln=True)
        pdf.set_font("Arial", "", 11)
        pdf.set_text_color(0, 0, 0)

        for line in recomendaciones.split("\n"):
            if line.strip():
                pdf.cell(0, 7, line.strip(), ln=True)

        pdf.ln(10)

        # Apoyo
        pdf.set_font("Arial", "I", 10)
        pdf.set_text_color(127, 140, 141)
        pdf.multi_cell(0, 6, "Esta evaluación es orientativa. El diagnóstico debe ser realizado por un profesional de la salud.")

        pdf.ln(5)
        pdf.set_text_color(44, 62, 80)
        pdf.set_font("Arial", "I", 10)
        pdf.cell(0, 6, "Apoyo comunitario de: SynergixLabs", ln=True)

        return pdf.output(dest="S").encode("latin1")

    # --- BOTÓN DESCARGAR PDF ---
    pdf_data = generar_pdf()
    st.download_button(
        label="📄 Descargar resultados en PDF",
        data=pdf_data,
        file_name="resultados_evaluacion_autismo.pdf",
        mime="application/pdf"
    )

    # --- BOTÓN REINICIAR ---
    if st.button("Realizar otra evaluación"):
        st.session_state.clear()
        st.rerun()
