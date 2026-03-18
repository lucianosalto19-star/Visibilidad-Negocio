import streamlit as st
import plotly.graph_objects as go
from fpdf import FPDF
import io
import datetime

# ─── CONFIG ───────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Visibilidad de tu negocio",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ─── ESTILOS ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

h1, h2, h3 {
    font-family: 'Sora', sans-serif;
}

.stApp {
    background: #f8f7f4;
}

.titulo-principal {
    font-family: 'Sora', sans-serif;
    font-size: 2.2rem;
    font-weight: 700;
    color: #1a1a2e;
    line-height: 1.2;
    margin-bottom: 0.5rem;
}

.subtitulo {
    font-family: 'DM Sans', sans-serif;
    font-size: 1.05rem;
    color: #555;
    line-height: 1.6;
    margin-bottom: 2rem;
}

.pregunta-label {
    font-family: 'Sora', sans-serif;
    font-size: 1rem;
    font-weight: 600;
    color: #1a1a2e;
}

.perfil-badge {
    background: #1a1a2e;
    color: #f0c040;
    font-family: 'Sora', sans-serif;
    font-weight: 700;
    font-size: 1.4rem;
    padding: 1rem 2rem;
    border-radius: 12px;
    display: inline-block;
    margin-bottom: 1rem;
}

.implicacion-box {
    background: white;
    border-left: 4px solid #f0c040;
    padding: 1rem 1.2rem;
    border-radius: 0 8px 8px 0;
    margin-bottom: 1rem;
    font-size: 0.95rem;
    color: #333;
    line-height: 1.6;
}

.prioridad-card {
    background: white;
    border: 1px solid #e8e4dc;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.8rem;
}

.prioridad-numero {
    font-family: 'Sora', sans-serif;
    font-weight: 700;
    color: #f0c040;
    font-size: 1.3rem;
}

.herramienta-tag {
    background: #f0f0f0;
    border-radius: 20px;
    padding: 0.3rem 0.8rem;
    font-size: 0.85rem;
    color: #444;
    display: inline-block;
    margin: 0.2rem;
}

.beneficio-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 0;
    font-size: 0.95rem;
    color: #333;
}

.divider {
    border: none;
    border-top: 1px solid #e8e4dc;
    margin: 1.5rem 0;
}

.stRadio > div {
    gap: 0.5rem;
}

.stRadio label {
    font-size: 0.95rem !important;
    color: #333 !important;
}

</style>
""", unsafe_allow_html=True)

# ─── DATOS ────────────────────────────────────────────────────────────────────

PREGUNTAS = [
    {
        "id": "datos",
        "dimension": "Datos",
        "texto": "¿Dónde vive la información de tu negocio?",
        "opciones": [
            ("Facturas, apuntes o en la cabeza de alguien", 0),
            ("Archivos de Excel o carpetas separadas", 1),
            ("Un CRM, ERP o sistema centralizado", 2),
        ]
    },
    {
        "id": "acceso",
        "dimension": "Acceso a información",
        "texto": "Cuando necesitas saber algo de tu negocio, ¿cómo lo obtienes?",
        "opciones": [
            ("Busco entre archivos o le pregunto a alguien", 0),
            ("Entro a una herramienta y lo consulto manualmente", 1),
            ("La información llega sola o la obtengo en minutos con una consulta", 2),
        ]
    },
    {
        "id": "decisiones",
        "dimension": "Decisiones",
        "texto": "¿Con qué información tomas decisiones importantes en tu empresa?",
        "opciones": [
            ("Con mi experiencia e intuición", 0),
            ("Con datos, pero generalmente tienen más de una semana", 1),
            ("Con datos actualizados de esta semana o de ayer", 2),
        ]
    },
    {
        "id": "comprension",
        "dimension": "Comprensión",
        "texto": "¿Puedes explicar hoy por qué subieron o bajaron tus ventas el mes pasado?",
        "opciones": [
            ("No, no tengo esa información disponible", 0),
            ("Sí, pero me tarda tiempo conseguirla", 1),
            ("Sí, lo veo directamente en mis sistemas", 2),
        ]
    },
    {
        "id": "automatizacion",
        "dimension": "Automatización",
        "texto": "¿Qué nivel de automatización tiene tu empresa hoy?",
        "opciones": [
            ("No automatizo nada, todo lo hace alguien manualmente", 0),
            ("Automatizo algunas tareas operativas repetitivas", 1),
            ("Automatizo procesos y uso datos para predecir o planear", 2),
        ]
    },
]

PERFILES = [
    {
        "nombre": "Sobreviviendo",
        "rango": (0, 1),
        "emoji": "🌱",
        "descripcion": "Tu negocio depende de la memoria de tu equipo. Si alguien falta, la información se pierde. No puedes crecer lo que no puedes medir.",
        "oportunidad": "Antes de pensar en IA necesitas un lugar único donde viva tu información: clientes, ventas, inventario y gastos. Todo en un solo lugar accesible para tu equipo.",
        "herramientas": ["HubSpot CRM (gratis)", "Zoho CRM", "Clientify", "Google Workspace", "Aspel / Contpaqi"],
        "beneficios": ["Mayor control sobre tu operación diaria", "Menos dependencia de personas clave", "Base sólida para crecer"],
    },
    {
        "nombre": "Registrando",
        "rango": (2, 3),
        "emoji": "📋",
        "descripcion": "Tienes sistemas pero no los aprovechas. Tu CRM o herramienta sabe más de tu negocio que tú. Estás pagando por algo que aún no te genera valor real.",
        "oportunidad": "No necesitas más herramientas, necesitas aprender a leer las que ya tienes. Activa los reportes nativos de tu sistema y conecta esa información a tus decisiones del día a día.",
        "herramientas": ["Reportes nativos de tu CRM", "Google Looker Studio (gratis)", "Cursos Google Activate", "QuickBooks Reports"],
        "beneficios": ["Decisiones más informadas sin nuevo software", "Tiempo liberado de búsqueda de información", "Mayor confianza en tus números"],
    },
    {
        "nombre": "Intentando ver",
        "rango": (4, 5),
        "emoji": "🔍",
        "descripcion": "Tienes esfuerzo analítico pero depende de personas, no de sistemas. Alguien produce tus reportes manualmente y si esa persona falta, pierdes visibilidad.",
        "oportunidad": "Automatiza lo que ya haces manualmente. El proceso que alguien ejecuta cada semana es tu primer candidato.",
        "herramientas": ["Power BI", "Looker Studio", "Zapier / Make", "Notion", "Airtable"],
        "beneficios": ["Reportes que se generan solos", "Menos carga operativa en tu equipo", "Visibilidad consistente sin depender de nadie"],
    },
    {
        "nombre": "Entendiendo",
        "rango": (6, 7),
        "emoji": "📈",
        "descripcion": "Puedes explicar tu negocio con datos. El siguiente paso es anticiparlo antes de que ocurra.",
        "oportunidad": "Tienes la base para incorporar análisis predictivo. Empieza con una proyección simple de ventas basada en tu histórico.",
        "herramientas": ["Modelos de forecasting en Excel/Python", "ChatGPT / Claude para análisis", "Databricks / BigQuery", "Automatización con reglas de negocio"],
        "beneficios": ["Anticipar problemas antes de que ocurran", "Decisiones proactivas en lugar de reactivas", "Ventaja competitiva real sobre tu mercado"],
    },
    {
        "nombre": "Anticipando",
        "rango": (8, 10),
        "emoji": "🚀",
        "descripcion": "Estás en el camino que pocos toman. Tu negocio tiene visibilidad completa y capacidad predictiva. El reto ahora es escalar y gobernar bien lo que tienes.",
        "oportunidad": "Explora agentes de IA especializados por área de negocio y automatización end-to-end de procesos complejos.",
        "herramientas": ["Agentes de IA por área", "Plataformas MLOps", "Data governance", "Automatización end-to-end"],
        "beneficios": ["Operación que escala sin crecer proporcionalmente en headcount", "Insights en tiempo real por área", "Posición competitiva difícil de replicar"],
    },
]

RECOMENDACIONES = {
    "datos": [
        {
            "nivel": 0,
            "texto": "Elige un CRM gratuito esta semana. HubSpot o Zoho en español. Migra tus contactos activos primero, todo lo demás después.",
            "impacto": "Alto"
        },
        {
            "nivel": 1,
            "texto": "Tu Excel ya es un CRM incompleto. El siguiente paso es migrar esa estructura a una herramienta que se actualice sola y que todo tu equipo pueda alimentar.",
            "impacto": "Alto"
        },
    ],
    "acceso": [
        {
            "nivel": 0,
            "texto": "Identifica una sola pregunta que te haces cada semana sobre tu negocio y construye un lugar donde esa respuesta esté siempre visible.",
            "impacto": "Medio"
        },
        {
            "nivel": 1,
            "texto": "Ya consultas tu información, ahora hazla llegar sola. Activa alertas y dashboards automáticos en las herramientas que ya tienes.",
            "impacto": "Medio"
        },
    ],
    "decisiones": [
        {
            "nivel": 0,
            "texto": "Define tres métricas que vas a revisar cada lunes: ventas de la semana, inventario crítico, cuentas por cobrar vencidas. Solo esas tres.",
            "impacto": "Alto"
        },
        {
            "nivel": 1,
            "texto": "Tienes datos pero están atrasados. Identifica dónde está el cuello de botella, generalmente es un reporte que alguien produce manualmente, y reemplázalo.",
            "impacto": "Alto"
        },
    ],
    "comprension": [
        {
            "nivel": 0,
            "texto": "Empieza por una sola área. ¿Por qué subieron o bajaron tus ventas este mes? Responde esa pregunta con datos aunque te tarde. La siguiente vez tardará menos.",
            "impacto": "Alto"
        },
        {
            "nivel": 1,
            "texto": "Ya puedes explicar tu negocio pero con esfuerzo. Documenta cómo llegas a esa respuesta y automatiza ese proceso.",
            "impacto": "Medio"
        },
    ],
    "automatizacion": [
        {
            "nivel": 0,
            "texto": "Elige el proceso más repetitivo de tu operación: cotizaciones, seguimiento a clientes, reportes de cierre. Ese es tu primer candidato a automatizar.",
            "impacto": "Alto"
        },
        {
            "nivel": 1,
            "texto": "Ya automatizas tareas. El siguiente paso es usar esos datos para predecir. Empieza con algo simple: proyección de ventas del siguiente mes basada en histórico.",
            "impacto": "Medio"
        },
    ],
}

# ─── FUNCIONES ────────────────────────────────────────────────────────────────

def calcular_perfil(puntaje_total):
    for perfil in PERFILES:
        if perfil["rango"][0] <= puntaje_total <= perfil["rango"][1]:
            return perfil
    return PERFILES[-1]

def calcular_prioridades(respuestas):
    prioridades = []
    for pregunta in PREGUNTAS:
        puntaje = respuestas.get(pregunta["id"], 0)
        if puntaje < 2:
            rec = RECOMENDACIONES[pregunta["id"]][puntaje]
            brecha = 2 - puntaje
            prioridades.append({
                "dimension": pregunta["dimension"],
                "puntaje_actual": puntaje,
                "brecha": brecha,
                "recomendacion": rec["texto"],
                "impacto": rec["impacto"],
            })
    prioridades.sort(key=lambda x: x["brecha"], reverse=True)
    return prioridades

def crear_telarana(respuestas, puntaje_total):
    dimensiones = [p["dimension"] for p in PREGUNTAS]
    valores_actuales = [respuestas.get(p["id"], 0) for p in PREGUNTAS]
    
    perfil_actual = calcular_perfil(puntaje_total)
    indice_perfil = PERFILES.index(perfil_actual)
    siguiente_perfil = PERFILES[min(indice_perfil + 1, len(PERFILES) - 1)]
    puntaje_siguiente = siguiente_perfil["rango"][0]
    
    valores_siguiente = []
    for i, pregunta in enumerate(PREGUNTAS):
        v_actual = valores_actuales[i]
        diferencia = puntaje_siguiente - puntaje_total
        if diferencia > 0 and v_actual < 2:
            valores_siguiente.append(min(2, v_actual + 1))
        else:
            valores_siguiente.append(v_actual)

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=valores_siguiente + [valores_siguiente[0]],
        theta=dimensiones + [dimensiones[0]],
        fill='toself',
        name=f'Siguiente nivel: {siguiente_perfil["nombre"]}',
        fillcolor='rgba(240, 192, 64, 0.15)',
        line=dict(color='#f0c040', width=2, dash='dash'),
    ))

    fig.add_trace(go.Scatterpolar(
        r=valores_actuales + [valores_actuales[0]],
        theta=dimensiones + [dimensiones[0]],
        fill='toself',
        name=f'Tu nivel actual: {perfil_actual["nombre"]}',
        fillcolor='rgba(26, 26, 46, 0.3)',
        line=dict(color='#1a1a2e', width=2.5),
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 2],
                tickvals=[0, 1, 2],
                ticktext=["Inicial", "En proceso", "Logrado"],
                tickfont=dict(size=10, color="#666"),
                gridcolor="#e8e4dc",
                linecolor="#e8e4dc",
            ),
            angularaxis=dict(
                tickfont=dict(size=12, family="Sora", color="#1a1a2e"),
                linecolor="#e8e4dc",
                gridcolor="#e8e4dc",
            ),
            bgcolor="#f8f7f4",
        ),
        showlegend=True,
        legend=dict(
            font=dict(size=11, family="DM Sans"),
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="#e8e4dc",
            borderwidth=1,
        ),
        paper_bgcolor="#f8f7f4",
        margin=dict(l=60, r=60, t=40, b=40),
        height=420,
    )

    return fig

def generar_pdf(perfil, puntaje_total, respuestas, prioridades):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Header
    pdf.set_fill_color(26, 26, 46)
    pdf.rect(0, 0, 210, 35, 'F')
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(240, 192, 64)
    pdf.set_y(10)
    pdf.cell(0, 10, "Diagnostico de Visibilidad del Negocio", ln=True, align="C")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(200, 200, 200)
    pdf.cell(0, 8, f"De sobrevivir a competir: automatizacion e IA como diferenciador", ln=True, align="C")

    pdf.set_y(45)
    pdf.set_text_color(26, 26, 46)

    # Perfil
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "Tu nivel actual de visibilidad", ln=True)
    pdf.set_draw_color(240, 192, 64)
    pdf.set_line_width(0.8)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)

    pdf.set_fill_color(26, 26, 46)
    pdf.set_text_color(240, 192, 64)
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 12, f"{perfil['emoji']}  {perfil['nombre']}  ({puntaje_total}/10 puntos)", ln=True, fill=True, align="C")
    pdf.ln(3)

    pdf.set_text_color(60, 60, 60)
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 6, perfil["descripcion"])
    pdf.ln(4)

    # Oportunidad
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(26, 26, 46)
    pdf.cell(0, 8, "Tu siguiente paso clave:", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(60, 60, 60)
    pdf.multi_cell(0, 6, perfil["oportunidad"])
    pdf.ln(4)

    # Prioridades
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(26, 26, 46)
    pdf.cell(0, 8, "Tus prioridades para subir de nivel", ln=True)
    pdf.set_line_width(0.8)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(4)

    for i, p in enumerate(prioridades[:3], 1):
        pdf.set_fill_color(248, 247, 244)
        pdf.set_draw_color(232, 228, 220)
        pdf.set_line_width(0.3)
        y_inicio = pdf.get_y()
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(26, 26, 46)
        pdf.cell(0, 7, f"{i}. {p['dimension']}  [Impacto: {p['impacto']}]", ln=True)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(80, 80, 80)
        pdf.multi_cell(0, 5, p["recomendacion"])
        pdf.ln(3)

    # Herramientas
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(26, 26, 46)
    pdf.cell(0, 8, "Herramientas recomendadas para tu nivel", ln=True)
    pdf.set_line_width(0.8)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(4)

    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(60, 60, 60)
    for h in perfil["herramientas"]:
        pdf.cell(5, 6, "-", ln=False)
        pdf.cell(0, 6, h, ln=True)
    pdf.ln(4)

    # Beneficios
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(26, 26, 46)
    pdf.cell(0, 8, "Al subir de nivel obtendras:", ln=True)
    pdf.set_line_width(0.8)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(4)

    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(60, 60, 60)
    for b in perfil["beneficios"]:
        pdf.cell(5, 6, "->", ln=False)
        pdf.cell(0, 6, b, ln=True)
    pdf.ln(6)

    # Footer
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(150, 150, 150)
    fecha = datetime.date.today().strftime("%d/%m/%Y")
    pdf.cell(0, 6, f"Generado el {fecha}  |  De sobrevivir a competir: automatizacion e IA como diferenciador para la empresa mexicana", ln=True, align="C")

    return pdf.output(dest='S').encode('latin-1')

# ─── APP ──────────────────────────────────────────────────────────────────────

if "pagina" not in st.session_state:
    st.session_state.pagina = "cuestionario"
if "respuestas" not in st.session_state:
    st.session_state.respuestas = {}
if "puntaje_total" not in st.session_state:
    st.session_state.puntaje_total = 0

# ══════════════════════════════════════════════════════════════════════════════
# PANTALLA 1 — CUESTIONARIO
# ══════════════════════════════════════════════════════════════════════════════

if st.session_state.pagina == "cuestionario":

    st.markdown('<div class="titulo-principal">¿Qué tan visible es tu negocio para ti?</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="subtitulo">
    No hace falta saber de tecnología para responder esto.<br>
    Este cuestionario de 5 preguntas te ayudará a entender el nivel de <strong>visibilidad actual de tu empresa</strong>,
    identificar cuáles deberían ser tus prioridades y qué herramientas concretas pueden apoyarte a dar el siguiente paso.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    respuestas_temp = {}
    todas_respondidas = True

    for i, pregunta in enumerate(PREGUNTAS, 1):
        st.markdown(f'<div class="pregunta-label">{i}. {pregunta["texto"]}</div>', unsafe_allow_html=True)
        opciones_texto = [op[0] for op in pregunta["opciones"]]
        seleccion = st.radio(
            label=pregunta["texto"],
            options=opciones_texto,
            index=None,
            key=f"q_{pregunta['id']}",
            label_visibility="collapsed"
        )
        if seleccion is None:
            todas_respondidas = False
        else:
            for texto, valor in pregunta["opciones"]:
                if texto == seleccion:
                    respuestas_temp[pregunta["id"]] = valor
        st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if not todas_respondidas:
            st.info("Responde todas las preguntas para ver tu diagnóstico.")
        boton = st.button(
            "Ver mi diagnóstico →",
            use_container_width=True,
            disabled=not todas_respondidas,
            type="primary"
        )

    if boton and todas_respondidas:
        puntaje = sum(respuestas_temp.values())
        st.session_state.respuestas = respuestas_temp
        st.session_state.puntaje_total = puntaje
        st.session_state.pagina = "resultados"
        st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PANTALLA 2 — RESULTADOS
# ══════════════════════════════════════════════════════════════════════════════

elif st.session_state.pagina == "resultados":

    respuestas = st.session_state.respuestas
    puntaje_total = st.session_state.puntaje_total
    perfil = calcular_perfil(puntaje_total)
    prioridades = calcular_prioridades(respuestas)

    st.markdown('<div class="titulo-principal">¿Y ahora qué?</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="subtitulo">
    Este es el estado actual de la visibilidad de tu negocio y cómo puedes llevarlo al siguiente nivel.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # Perfil actual
    st.markdown(f"""
    <div style="text-align:center; margin-bottom: 1rem;">
        <div class="perfil-badge">{perfil['emoji']} Nivel actual: {perfil['nombre']}</div>
        <div style="color:#888; font-size:0.9rem; margin-top:0.3rem;">{puntaje_total} de 10 puntos</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<div class="implicacion-box">{perfil["descripcion"]}</div>', unsafe_allow_html=True)

    # Telaraña
    st.markdown("#### Tu visibilidad actual vs el siguiente nivel")
    st.caption("La línea oscura es donde estás hoy. La línea amarilla es a donde puedes llegar con las acciones correctas.")
    fig = crear_telarana(respuestas, puntaje_total)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # Prioridades
    if prioridades:
        st.markdown("#### Tus prioridades para subir de nivel")
        st.caption("Ordenadas por impacto. Empieza por la primera.")

        for i, p in enumerate(prioridades, 1):
            with st.container():
                col_num, col_content = st.columns([0.08, 0.92])
                with col_num:
                    st.markdown(f'<div class="prioridad-numero">{i}</div>', unsafe_allow_html=True)
                with col_content:
                    st.markdown(f"""
                    <div class="prioridad-card">
                        <strong>{p['dimension']}</strong>
                        <span style="float:right; font-size:0.8rem; color:#888;">Impacto: {p['impacto']}</span><br>
                        <span style="font-size:0.92rem; color:#444;">{p['recomendacion']}</span>
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.success("🎯 Tu empresa ya tiene visibilidad completa. El siguiente paso es escalar y gobernar lo que tienes.")

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # Herramientas
    st.markdown("#### Herramientas recomendadas para tu nivel")
    herr_cols = st.columns(3)
    for i, h in enumerate(perfil["herramientas"]):
        with herr_cols[i % 3]:
            st.markdown(f'<span class="herramienta-tag">🔧 {h}</span>', unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # Beneficios
    st.markdown("#### Al subir de nivel obtendrás:")
    for b in perfil["beneficios"]:
        st.markdown(f"✅ {b}")

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # Botones
    col_pdf, col_reiniciar = st.columns(2)

    with col_pdf:
        pdf_bytes = generar_pdf(perfil, puntaje_total, respuestas, prioridades)
        st.download_button(
            label="📄 Descargar mi diagnóstico en PDF",
            data=pdf_bytes,
            file_name=f"diagnostico_visibilidad_{perfil['nombre'].lower()}.pdf",
            mime="application/pdf",
            use_container_width=True,
            type="primary"
        )

    with col_reiniciar:
        if st.button("↩ Volver a empezar", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    st.markdown("""
    <div style="text-align:center; margin-top:2rem; font-size:0.85rem; color:#aaa;">
        De sobrevivir a competir: automatización e IA como diferenciador para la empresa mexicana
    </div>
    """, unsafe_allow_html=True)
