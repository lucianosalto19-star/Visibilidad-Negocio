import streamlit as st
import plotly.graph_objects as go
from fpdf import FPDF
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
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,400&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: #f8f7f4;
}

.titulo-principal {
    font-family: 'Sora', sans-serif;
    font-size: 2.3rem;
    font-weight: 800;
    color: #1a1a2e;
    line-height: 1.2;
    margin-bottom: 0.6rem;
    text-align: center;
}

.subtitulo {
    font-family: 'DM Sans', sans-serif;
    font-size: 1.05rem;
    color: #4a4a4a;
    line-height: 1.7;
    margin-bottom: 1.5rem;
    text-align: justify;
}

.pregunta-label {
    font-family: 'Sora', sans-serif;
    font-size: 1.05rem;
    font-weight: 600;
    color: #1a1a2e;
    margin-bottom: 0.3rem;
}

.titulo-resultados {
    font-family: 'Sora', sans-serif;
    font-size: 2.1rem;
    font-weight: 800;
    color: #1a1a2e;
    text-align: center;
    margin-bottom: 0.4rem;
}

.subtitulo-resultados {
    font-family: 'DM Sans', sans-serif;
    font-size: 1.05rem;
    color: #4a4a4a;
    text-align: center;
    line-height: 1.6;
    margin-bottom: 1.5rem;
}

.perfil-contenedor {
    background: #1a1a2e;
    border-radius: 16px;
    padding: 1.8rem 2rem;
    margin-bottom: 1.5rem;
    text-align: center;
}

.perfil-nivel {
    font-family: 'Sora', sans-serif;
    font-size: 0.85rem;
    font-weight: 600;
    color: #f0c040;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 0.3rem;
}

.perfil-nombre {
    font-family: 'Sora', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 0.2rem;
}

.perfil-puntaje {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.9rem;
    color: #aaaacc;
    margin-bottom: 1rem;
}

.perfil-descripcion {
    font-family: 'DM Sans', sans-serif;
    font-size: 1rem;
    color: #d0d0e8;
    line-height: 1.7;
    text-align: justify;
    border-top: 1px solid rgba(240,192,64,0.3);
    padding-top: 1rem;
    margin-top: 0.5rem;
}

.seccion-titulo {
    font-family: 'Sora', sans-serif;
    font-size: 1.2rem;
    font-weight: 700;
    color: #1a1a2e;
    text-align: center;
    margin: 1.8rem 0 0.4rem 0;
}

.seccion-descripcion {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.95rem;
    color: #666;
    text-align: center;
    margin-bottom: 1rem;
    line-height: 1.6;
}

.recomendacion-card {
    background: white;
    border-radius: 12px;
    padding: 1.1rem 1.3rem;
    margin-bottom: 0.9rem;
    border: 1px solid #e8e4dc;
    display: flex;
    align-items: flex-start;
    gap: 0.8rem;
}

.rec-dimension {
    font-family: 'Sora', sans-serif;
    font-size: 0.8rem;
    font-weight: 700;
    color: #888;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.2rem;
}

.rec-texto {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.97rem;
    color: #333;
    line-height: 1.6;
    text-align: justify;
}

.herramienta-tag {
    background: #f0f0f0;
    border-radius: 20px;
    padding: 0.35rem 0.9rem;
    font-size: 0.88rem;
    color: #333;
    display: inline-block;
    margin: 0.25rem;
    font-family: 'DM Sans', sans-serif;
    border: 1px solid #e0e0e0;
}

.beneficio-item {
    font-family: 'DM Sans', sans-serif;
    font-size: 1rem;
    color: #333;
    padding: 0.4rem 0;
    line-height: 1.5;
    border-bottom: 1px solid #f0ede8;
}

.oportunidad-box {
    background: #fffbef;
    border-left: 4px solid #f0c040;
    border-radius: 0 10px 10px 0;
    padding: 1rem 1.3rem;
    margin: 1rem 0 1.5rem 0;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.97rem;
    color: #333;
    line-height: 1.7;
    text-align: justify;
}

.divider {
    border: none;
    border-top: 1px solid #e8e4dc;
    margin: 1.5rem 0;
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
            ("Facturas, apuntes físicos / PDF sueltos / en la cabeza de alguien", 0),
            ("Excel / archivos digitales separados / QuickBooks o herramienta similar", 1),
            ("CRM / ERP / repositorio centralizado de información", 2),
        ]
    },
    {
        "id": "acceso",
        "dimension": "Acceso a información",
        "texto": "Cuando necesitas saber algo de tu negocio, ¿cómo lo obtienes?",
        "opciones": [
            ("Pregunto a alguien / busco entre correos, papeles o archivos sueltos", 0),
            ("Entro a una herramienta como Excel / QuickBooks y busco manualmente lo que necesito", 1),
            ("Tengo un dashboard / reporte automático que me lo muestra sin necesidad de buscarlo", 2),
        ]
    },
    {
        "id": "decisiones",
        "dimension": "Decisiones",
        "texto": "¿Con qué información tomas decisiones importantes en tu empresa?",
        "opciones": [
            ("Con mi experiencia e intuición, no con datos formales", 0),
            ("Con datos, pero generalmente tienen más de una semana de antigüedad", 1),
            ("Con datos actualizados de esta semana / de ayer", 2),
        ]
    },
    {
        "id": "comprension",
        "dimension": "Comprensión",
        "texto": "¿Puedes explicar hoy por qué subieron o bajaron tus ventas el mes pasado?",
        "opciones": [
            ("No, no tengo esa información disponible", 0),
            ("Sí, pero me tarda tiempo conseguirla y analizarla", 1),
            ("Sí, lo veo directamente en mis sistemas sin mayor esfuerzo", 2),
        ]
    },
    {
        "id": "automatizacion",
        "dimension": "Automatización",
        "texto": "¿Qué nivel de automatización tiene tu empresa hoy?",
        "opciones": [
            ("No automatizo nada, todo lo ejecuta alguien manualmente", 0),
            ("Automatizo algunas tareas operativas repetitivas", 1),
            ("Automatizo procesos y uso datos para predecir / planear decisiones futuras", 2),
        ]
    },
]

PERFILES = [
    {
        "nombre": "Sobreviviendo",
        "icono": "Nivel 1 / 5",
        "rango": (0, 1),
        "descripcion": "Tu negocio depende de la memoria de tu equipo. Si alguien falta, la información se pierde. No puedes crecer lo que no puedes medir, y hoy gran parte de tu operación es invisible para ti.",
        "oportunidad": "Antes de pensar en IA necesitas un lugar único donde viva tu información: clientes, ventas, inventario y gastos, todo en un solo lugar accesible para tu equipo. Este es el primer peldaño y es más sencillo de lo que parece.",
        "herramientas": ["HubSpot CRM (gratuito)", "Zoho CRM", "Clientify", "Google Workspace", "Aspel / Contpaqi"],
        "beneficios": [
            "Mayor control sobre tu operación diaria sin depender de personas clave",
            "Capacidad de medir lo que pasa en tu negocio en tiempo real",
            "Base sólida para crecer sin perder el hilo de tu información",
        ],
    },
    {
        "nombre": "Registrando",
        "icono": "Nivel 2 / 5",
        "rango": (2, 3),
        "descripcion": "Tienes sistemas pero no los estás aprovechando. Tu CRM / herramienta sabe más de tu negocio que tú. Estás pagando por infraestructura que aún no te genera valor real.",
        "oportunidad": "No necesitas más herramientas, necesitas aprender a leer las que ya tienes. Activa los reportes nativos de tu sistema y empieza a conectar esa información a tus decisiones del día a día. El valor ya está ahí, solo hay que desbloquearlo.",
        "herramientas": ["Reportes nativos de tu CRM / ERP", "Google Looker Studio (gratuito)", "Cursos Google Activate", "QuickBooks Reports avanzados"],
        "beneficios": [
            "Decisiones más informadas sin invertir en nuevo software",
            "Tiempo liberado de búsqueda manual de información",
            "Mayor confianza en tus números y en tu equipo",
        ],
    },
    {
        "nombre": "Intentando ver",
        "icono": "Nivel 3 / 5",
        "rango": (4, 5),
        "descripcion": "Tienes esfuerzo analítico pero depende de personas, no de sistemas. Alguien produce tus reportes manualmente y si esa persona falta o se equivoca, pierdes visibilidad de tu negocio.",
        "oportunidad": "Automatiza lo que ya haces manualmente. El proceso que alguien ejecuta cada semana es tu primer candidato. No se trata de tecnología compleja, sino de conectar lo que ya tienes.",
        "herramientas": ["Power BI", "Google Looker Studio", "Zapier / Make", "Notion", "Airtable"],
        "beneficios": [
            "Reportes que se generan solos sin depender de nadie",
            "Menos carga operativa en tu equipo clave",
            "Visibilidad consistente y confiable de tu negocio",
        ],
    },
    {
        "nombre": "Entendiendo",
        "icono": "Nivel 4 / 5",
        "rango": (6, 7),
        "descripcion": "Puedes explicar lo que pasa en tu negocio con datos. Eso ya te pone por encima de la mayoría. El siguiente paso es pasar de entender lo que ocurrió a anticipar lo que va a ocurrir.",
        "oportunidad": "Tienes la base para incorporar análisis predictivo. Empieza con algo concreto: una proyección de ventas basada en tu histórico o una alerta automática cuando un indicador clave se salga del rango esperado.",
        "herramientas": ["Modelos de forecasting en Python / Excel", "Claude / ChatGPT para análisis", "Databricks / BigQuery", "Automatización con reglas de negocio"],
        "beneficios": [
            "Capacidad de anticipar problemas antes de que ocurran",
            "Decisiones proactivas en lugar de reactivas",
            "Ventaja competitiva real y difícil de replicar",
        ],
    },
    {
        "nombre": "Anticipando",
        "icono": "Nivel 5 / 5",
        "rango": (8, 10),
        "descripcion": "Estás en el camino que pocos toman. Tu negocio tiene visibilidad completa y capacidad predictiva. El reto ahora es escalar lo que tienes y gobernarlo bien para que siga funcionando mientras tu empresa crece.",
        "oportunidad": "Explora agentes de IA especializados por área de negocio y automatización de extremo a extremo de procesos complejos. El objetivo es que tu operación escale sin que el headcount crezca proporcionalmente.",
        "herramientas": ["Agentes de IA por área de negocio", "Plataformas MLOps", "Data governance", "Automatización end-to-end"],
        "beneficios": [
            "Operación que escala sin crecer proporcionalmente en costos fijos",
            "Insights en tiempo real por área de negocio",
            "Posición competitiva que la competencia tardará años en alcanzar",
        ],
    },
]

NIVEL_IMPLICACION = {
    "datos": {
        0: "Tu información no está organizada. Cualquier decisión depende de que alguien la recuerde o la encuentre.",
        1: "Tienes información registrada pero dispersa. Acceder a ella toma tiempo y esfuerzo.",
        2: "Tu información está centralizada. Cualquiera en tu equipo puede acceder a ella cuando la necesita.",
    },
    "acceso": {
        0: "Obtener información de tu negocio depende de personas, no de sistemas. Es lento y propenso a errores.",
        1: "Tienes herramientas, pero la información no llega sola. Requiere que alguien vaya a buscarla.",
        2: "La información te encuentra a ti. Tienes visibilidad sin esfuerzo adicional.",
    },
    "decisiones": {
        0: "Tus decisiones se basan en experiencia, no en datos. Eso funciona hasta que el negocio crece.",
        1: "Tomas decisiones con datos, pero con retraso. En mercados dinámicos eso puede costarte caro.",
        2: "Tus decisiones están respaldadas por información reciente. Reduces el riesgo de equivocarte.",
    },
    "comprension": {
        0: "No puedes explicar lo que pasa en tu negocio con datos. Eso limita tu capacidad de mejorarlo.",
        1: "Puedes explicarlo, pero con esfuerzo. El conocimiento está atrapado en procesos manuales.",
        2: "Tienes claridad sobre tu negocio en todo momento. Eso es poder real de decisión.",
    },
    "automatizacion": {
        0: "Todo depende de que alguien lo ejecute. Tu operación es tan buena como tu equipo en su peor día.",
        1: "Has automatizado lo repetitivo. Eso libera tiempo para lo que realmente importa.",
        2: "Tu operación aprende y se anticipa. Eso separa a las empresas que compiten de las que sobreviven.",
    },
}

RECOMENDACIONES = {
    "datos": [
        {"nivel": 0, "texto": "Elige un CRM gratuito esta semana — HubSpot / Zoho en español. Migra tus contactos activos primero, el resto después. El objetivo es que tu información deje de vivir en la cabeza de alguien.", "impacto": "Alto"},
        {"nivel": 1, "texto": "Tu Excel ya es un CRM incompleto. El siguiente paso es migrar esa estructura a una herramienta que se actualice sola y que todo tu equipo pueda alimentar sin depender de ti.", "impacto": "Alto"},
    ],
    "acceso": [
        {"nivel": 0, "texto": "Identifica una sola pregunta que te haces cada semana sobre tu negocio y construye un lugar donde esa respuesta esté siempre visible. Empieza con una, no con diez.", "impacto": "Medio"},
        {"nivel": 1, "texto": "Ya consultas tu información, ahora hazla llegar sola. Activa alertas y dashboards automáticos en las herramientas que ya tienes — casi todas lo permiten sin costo adicional.", "impacto": "Medio"},
    ],
    "decisiones": [
        {"nivel": 0, "texto": "Define tres métricas que revisarás cada lunes: ventas de la semana, inventario crítico, cuentas por cobrar vencidas. Solo esas tres. Lo que se mide, se gestiona.", "impacto": "Alto"},
        {"nivel": 1, "texto": "Tienes datos pero están atrasados. Identifica dónde está el cuello de botella — generalmente es un reporte que alguien produce manualmente — y elimínalo.", "impacto": "Alto"},
    ],
    "comprension": [
        {"nivel": 0, "texto": "Empieza por una sola área: ¿por qué subieron / bajaron tus ventas este mes? Responde esa pregunta con datos aunque te tarde. La siguiente vez tardará menos.", "impacto": "Alto"},
        {"nivel": 1, "texto": "Ya puedes explicar tu negocio pero con esfuerzo. Documenta cómo llegas a esa respuesta y automatiza ese proceso para que ocurra solo cada semana.", "impacto": "Medio"},
    ],
    "automatizacion": [
        {"nivel": 0, "texto": "Elige el proceso más repetitivo de tu operación — cotizaciones, seguimiento a clientes, reportes de cierre. Ese es tu primer candidato a automatizar. No necesitas programar nada.", "impacto": "Alto"},
        {"nivel": 1, "texto": "Ya automatizas tareas. El siguiente paso es usar esos datos para predecir. Empieza simple: proyección de ventas del siguiente mes basada en tu histórico.", "impacto": "Medio"},
    ],
}

SEMAFORO = {"Alto": "🔴", "Medio": "🟡", "Bajo": "🟢"}

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
            prioridades.append({
                "dimension": pregunta["dimension"],
                "puntaje_actual": puntaje,
                "brecha": 2 - puntaje,
                "recomendacion": rec["texto"],
                "impacto": rec["impacto"],
            })
    prioridades.sort(key=lambda x: ({"Alto": 0, "Medio": 1, "Bajo": 2}[x["impacto"]], -x["brecha"]))
    return prioridades

def crear_telarana(respuestas, puntaje_total):
    dimensiones = [p["dimension"] for p in PREGUNTAS]
    valores_actuales = [respuestas.get(p["id"], 0) for p in PREGUNTAS]

    perfil_actual    = calcular_perfil(puntaje_total)
    indice_perfil    = PERFILES.index(perfil_actual)
    siguiente_perfil = PERFILES[min(indice_perfil + 1, len(PERFILES) - 1)]
    puntaje_sig      = siguiente_perfil["rango"][0]

    valores_siguiente = list(valores_actuales)
    pendiente = max(0, puntaje_sig - puntaje_total)
    for i in range(len(PREGUNTAS)):
        if pendiente > 0 and valores_siguiente[i] < 2:
            valores_siguiente[i] += 1
            pendiente -= 1

    tooltips_actual = []
    for pregunta in PREGUNTAS:
        v = respuestas.get(pregunta["id"], 0)
        impl = NIVEL_IMPLICACION[pregunta["id"]][v]
        tooltips_actual.append(f"<b>{pregunta['dimension']}</b> — Nivel {v}/2<br>{impl}")

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=valores_siguiente + [valores_siguiente[0]],
        theta=dimensiones + [dimensiones[0]],
        fill='toself',
        name=f'Siguiente nivel: {siguiente_perfil["nombre"]}',
        fillcolor='rgba(240,192,64,0.12)',
        line=dict(color='#f0c040', width=2, dash='dash'),
        hoverinfo='skip',
    ))

    fig.add_trace(go.Scatterpolar(
        r=valores_actuales + [valores_actuales[0]],
        theta=dimensiones + [dimensiones[0]],
        fill='toself',
        name=f'Tu nivel: {perfil_actual["nombre"]}',
        fillcolor='rgba(26,26,46,0.25)',
        line=dict(color='#1a1a2e', width=2.5),
        text=tooltips_actual + [tooltips_actual[0]],
        hovertemplate='%{text}<extra></extra>',
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 2],
                tickvals=[0, 1, 2],
                ticktext=["Inicial", "En proceso", "Logrado"],
                tickfont=dict(size=10, color="#888"),
                gridcolor="#e0ddd8",
                linecolor="#e0ddd8",
            ),
            angularaxis=dict(
                tickfont=dict(size=12, family="Sora", color="#1a1a2e"),
                linecolor="#e0ddd8",
                gridcolor="#e0ddd8",
            ),
            bgcolor="#f8f7f4",
        ),
        showlegend=True,
        legend=dict(
            font=dict(size=11, family="DM Sans"),
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor="#e8e4dc",
            borderwidth=1,
            orientation="h",
            yanchor="bottom",
            y=-0.18,
            xanchor="center",
            x=0.5,
        ),
        paper_bgcolor="#f8f7f4",
        margin=dict(l=60, r=60, t=30, b=70),
        height=430,
    )
    return fig

def generar_pdf(perfil, puntaje_total, prioridades):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Header
    pdf.set_fill_color(26, 26, 46)
    pdf.rect(0, 0, 210, 38, 'F')
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(240, 192, 64)
    pdf.set_y(9)
    pdf.cell(0, 9, "Diagnostico de Visibilidad del Negocio", ln=True, align="C")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(180, 180, 200)
    pdf.cell(0, 7, "De sobrevivir a competir: automatizacion e IA como diferenciador", ln=True, align="C")

    pdf.set_y(46)
    pdf.set_text_color(26, 26, 46)

    # Nivel actual
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "Tu nivel actual de visibilidad", ln=True)
    pdf.set_draw_color(240, 192, 64)
    pdf.set_line_width(0.8)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(4)

    pdf.set_fill_color(26, 26, 46)
    pdf.set_text_color(240, 192, 64)
    pdf.set_font("Helvetica", "B", 13)
    nivel_txt = f"Nivel: {perfil['nombre']}  |  Puntaje: {puntaje_total} / 10"
    pdf.cell(0, 11, nivel_txt, ln=True, fill=True, align="C")
    pdf.ln(3)

    pdf.set_text_color(60, 60, 60)
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 6, perfil["descripcion"])
    pdf.ln(3)

    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(26, 26, 46)
    pdf.cell(0, 7, "Siguiente paso clave:", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(60, 60, 60)
    pdf.multi_cell(0, 6, perfil["oportunidad"])
    pdf.ln(4)

    # Prioridades
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(26, 26, 46)
    pdf.cell(0, 8, "Tus prioridades para ganar visibilidad", ln=True)
    pdf.set_line_width(0.8)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(4)

    for i, p in enumerate(prioridades, 1):
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(26, 26, 46)
        pdf.cell(0, 7, f"{i}. {p['dimension']}  [Impacto {p['impacto']}]", ln=True)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(70, 70, 70)
        pdf.multi_cell(0, 5, p["recomendacion"])
        pdf.ln(2)

    # Herramientas
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(26, 26, 46)
    pdf.cell(0, 8, "Herramientas que pueden impulsarte al siguiente nivel", ln=True)
    pdf.set_line_width(0.8)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(4)

    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(60, 60, 60)
    for h in perfil["herramientas"]:
        pdf.cell(6, 6, "-", ln=False)
        pdf.cell(0, 6, h, ln=True)
    pdf.ln(3)

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
        pdf.cell(6, 6, "->", ln=False)
        pdf.multi_cell(0, 6, b)
    pdf.ln(4)

    # Footer
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(160, 160, 160)
    fecha = datetime.date.today().strftime("%d/%m/%Y")
    pdf.cell(0, 6, f"Generado el {fecha}  |  Universidad de la Libertad  |  Especialidad IA Aplicada a los Negocios", ln=True, align="C")

    return bytes(pdf.output())

# ─── ESTADO ───────────────────────────────────────────────────────────────────

if "pagina" not in st.session_state:
    st.session_state.pagina = "cuestionario"
if "respuestas" not in st.session_state:
    st.session_state.respuestas = {}
if "puntaje_total" not in st.session_state:
    st.session_state.puntaje_total = 0

# ══════════════════════════════════════════════════════════════════════════════
# PANTALLA 1
# ══════════════════════════════════════════════════════════════════════════════

if st.session_state.pagina == "cuestionario":

    st.markdown('<div class="titulo-principal">¿Qué tan visible es tu negocio para ti?</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="subtitulo">
    No hace falta saber de tecnología para responder esto.<br><br>
    Este cuestionario de 5 preguntas te ayudará a entender el nivel de
    <strong>visibilidad actual de tu empresa</strong>, identificar cuáles deberían ser
    tus prioridades y qué herramientas concretas pueden apoyarte a dar el siguiente paso
    hacia una operación más clara, más eficiente y más competitiva.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    respuestas_temp  = {}
    todas_respondidas = True

    for i, pregunta in enumerate(PREGUNTAS, 1):
        st.markdown(f'<div class="pregunta-label">{i}. {pregunta["texto"]}</div>', unsafe_allow_html=True)
        seleccion = st.radio(
            label=pregunta["texto"],
            options=[op[0] for op in pregunta["opciones"]],
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
        if st.button(
            "Ver mi diagnóstico →",
            use_container_width=True,
            disabled=not todas_respondidas,
            type="primary"
        ):
            puntaje = sum(respuestas_temp.values())
            st.session_state.respuestas   = respuestas_temp
            st.session_state.puntaje_total = puntaje
            st.session_state.pagina        = "resultados"
            st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PANTALLA 2
# ══════════════════════════════════════════════════════════════════════════════

elif st.session_state.pagina == "resultados":

    respuestas    = st.session_state.respuestas
    puntaje_total = st.session_state.puntaje_total
    perfil        = calcular_perfil(puntaje_total)
    prioridades   = calcular_prioridades(respuestas)
    indice_perfil = PERFILES.index(perfil)
    sig_perfil    = PERFILES[min(indice_perfil + 1, len(PERFILES) - 1)]

    # Título
    st.markdown('<div class="titulo-resultados">Tu siguiente paso empieza aquí.</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="subtitulo-resultados">
    Este es el estado actual de la visibilidad de tu negocio.<br>
    Abajo encontrarás las acciones concretas que te llevarán al siguiente nivel.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # Perfil
    st.markdown(f"""
    <div class="perfil-contenedor">
        <div class="perfil-nivel">Nivel actual de visibilidad &nbsp;·&nbsp; {perfil['icono']}</div>
        <div class="perfil-nombre">{perfil['nombre']}</div>
        <div class="perfil-puntaje">{puntaje_total} de 10 puntos</div>
        <div class="perfil-descripcion">{perfil['descripcion']}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="oportunidad-box"><strong>Tu siguiente paso clave:</strong><br>'
        + perfil["oportunidad"] + '</div>',
        unsafe_allow_html=True
    )

    # Telaraña
    st.markdown('<div class="seccion-titulo">Tu mapa de visibilidad</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="seccion-descripcion">
    La <strong>línea oscura</strong> muestra dónde estás hoy.<br>
    La <strong>línea dorada</strong> muestra a dónde puedes llegar: nivel <em>{sig_perfil['nombre']}</em>.<br>
    <span style="font-size:0.88rem; color:#999;">
    Pasa el cursor sobre cada vértice para ver qué implica tu nivel actual en esa dimensión.
    </span>
    </div>
    """, unsafe_allow_html=True)

    fig = crear_telarana(respuestas, puntaje_total)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # Prioridades
    if prioridades:
        st.markdown('<div class="seccion-titulo">Tus prioridades para ganar visibilidad</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="seccion-descripcion">
        Cada acción está diseñada para que <strong>entiendas mejor lo que pasa en tu negocio</strong>
        y puedas tomar mejores decisiones. Ordenadas por impacto.<br>
        <span style="font-size:0.88rem;">🔴 Alto &nbsp;·&nbsp; 🟡 Medio &nbsp;·&nbsp; 🟢 Bajo</span>
        </div>
        """, unsafe_allow_html=True)

        for i, p in enumerate(prioridades, 1):
            semaforo = SEMAFORO.get(p["impacto"], "⚪")
            st.markdown(f"""
            <div class="recomendacion-card">
                <div style="min-width:2rem; padding-top:0.1rem; font-size:1.3rem;">{semaforo}</div>
                <div>
                    <div class="rec-dimension">{i}. {p['dimension']}</div>
                    <div class="rec-texto">{p['recomendacion']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.success("Tu empresa ya tiene visibilidad completa. El siguiente paso es escalar y gobernar lo que tienes.")

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # Herramientas
    st.markdown('<div class="seccion-titulo">Herramientas que pueden impulsarte al siguiente nivel</div>', unsafe_allow_html=True)
    herr_html = "".join([f'<span class="herramienta-tag">{h}</span>' for h in perfil["herramientas"]])
    st.markdown(f'<div style="text-align:center; margin-bottom:1rem;">{herr_html}</div>', unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # Beneficios
    st.markdown('<div class="seccion-titulo">Al subir de nivel obtendrás</div>', unsafe_allow_html=True)
    for b in perfil["beneficios"]:
        st.markdown(f'<div class="beneficio-item">&#10003; &nbsp;{b}</div>', unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # Botones
    col_pdf, col_reiniciar = st.columns(2)

    with col_pdf:
        try:
            pdf_bytes = generar_pdf(perfil, puntaje_total, prioridades)
            st.download_button(
                label="Descargar mi diagnostico en PDF",
                data=pdf_bytes,
                file_name=f"diagnostico_{perfil['nombre'].lower().replace(' ', '_')}.pdf",
                mime="application/pdf",
                use_container_width=True,
                type="primary"
            )
        except Exception as e:
            st.error(f"Error al generar PDF: {e}")

    with col_reiniciar:
        if st.button("Volver a empezar", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    # Footer
    st.markdown("""
    <div style="text-align:center; margin-top:2.5rem; padding-top:1rem;
                border-top:1px solid #e8e4dc; font-size:0.82rem; color:#bbb;
                font-family:'DM Sans', sans-serif;">
        De sobrevivir a competir: automatización e IA como diferenciador para la empresa mexicana<br>
        <span style="color:#ddd;">Universidad de la Libertad &nbsp;·&nbsp; Especialidad en IA Aplicada a los Negocios</span>
    </div>
    """, unsafe_allow_html=True)
