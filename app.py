import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# =====================================================
# CONFIGURACIÓN
# =====================================================

st.set_page_config(
    page_title="Índice de Riesgo de Crisis",
    page_icon="📊",
    layout="wide"
)

# =====================================================
# ESTILOS
# =====================================================

st.markdown("""
<style>

.block-container{
    padding-top:1rem;
}

[data-testid="stMetricValue"]{
    font-size:2rem;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# FUNCIONES
# =====================================================

def determinar_criticidad(irc):

    if irc < 40:
        return "ESTABLE"

    elif irc < 70:
        return "RIESGO CRECIENTE"

    else:
        return "CRÍTICO"


def obtener_escenario_dominante(
        estable,
        creciente,
        critico
):

    escenarios = {
        "Estable": estable,
        "Riesgo creciente": creciente,
        "Crítico": critico
    }

    return max(
        escenarios,
        key=escenarios.get
    )


def generar_resumen(
        irc,
        iaam,
        escenario
):

    if escenario == "Estable":

        return f"""
El sistema evidencia condiciones de estabilidad funcional.

El Índice de Riesgo de Crisis (IRC) se ubica en {irc:.0f}% y el Índice de Activación de Asistencia Militar (IAAM) alcanza {iaam:.0f}%.

Los indicadores evaluados permanecen dentro de parámetros compatibles con un escenario estable y no se identifican factores con capacidad suficiente para generar una alteración significativa del orden público en el corto plazo.
"""

    elif escenario == "Riesgo creciente":

        return f"""
El sistema evidencia una fase de riesgo creciente.

El IRC alcanza {irc:.0f}% y el IAAM {iaam:.0f}%

La convergencia de factores asociados a movilización social y amplificación narrativa incrementa la probabilidad de afectaciones localizadas y exige fortalecimiento de capacidades de monitoreo y coordinación.
"""

    else:

        return f"""
El sistema evidencia convergencia de factores críticos.

El IRC alcanza {irc*100:.0f}% y el IAAM {iaam*100:.0f}%

La simultaneidad de múltiples factores de riesgo incrementa significativamente la probabilidad de evolución hacia escenarios de crisis y exige fortalecimiento de capacidades institucionales y mecanismos de coordinación.
"""


def generar_alerta(irc):

    if irc >= 70:

        return (
            "ALERTA CRÍTICA",
            "Convergencia de factores críticos con capacidad de escalamiento."
        )

    elif irc >= 40:

        return (
            "ALERTA PREVENTIVA",
            "Incremento de indicadores de conflictividad y movilización."
        )

    else:

        return (
            "ALERTA INFORMATIVA",
            "Condiciones compatibles con estabilidad funcional."
        )


def generar_alistamiento(iaam):

    if iaam <= 30:

        return {
            "nivel": "Baja probabilidad",
            "intencion": "Prevenir y anticipar",
            "ordenes": [
                "Mantener monitoreo permanente del IRC/IAAM y reporte diario consolidado.",
                "Coordinación continua con autoridades civiles y Policía para intercambio de información.",
                "Verificar planes de contingencia y protocolos de apoyo subsidiario.",
                "Reforzar capacitación en DD.HH., uso diferenciado de la fuerza y reglas de empleo aplicables al apoyo a la autoridad civil."
            ]
        }

    elif iaam <= 60:

        return {
            "nivel": "Probable",
            "intencion": "Preparar y articular",
            "ordenes": [
                "Activar instancias de coordinación interinstitucional (PMU u homólogos) con gobernadores y alcaldes.",
                "Revisión jurídica para eventuales solicitudes de asistencia militar.",
                "Alistamiento logístico general y disponibilidad de capacidades de apoyo.",
                "Consolidar un plan de comunicaciones institucionales para escenarios de escalamiento."
            ]
        }

    elif iaam <= 80:

        return {
            "nivel": "Alta probabilidad",
            "intencion": "Apoyar de forma subsidiaria",
            "ordenes": [
                "Disponer capacidades para apoyo a la autoridad civil, sujeto a solicitud formal.",
                "Coordinar con la Policía la delimitación de roles, manteniendo liderazgo policial.",
                "Priorizar la protección de infraestructura crítica conforme a la ley.",
                "Fortalecer mecanismos de control, registro y supervisión."
            ]
        }

    else:

        return {
            "nivel": "Intervención inminente",
            "intencion": "Contener y estabilizar bajo control civil",
            "ordenes": [
                "Ejecutar la asistencia militar conforme a la solicitud de la autoridad civil competente.",
                "Coordinación centralizada con Gobierno, Policía y autoridades territoriales.",
                "Priorizar la continuidad de servicios esenciales y protección de infraestructura estratégica.",
                "Garantizar comunicación pública transparente y mecanismos reforzados de supervisión."
            ]
        }


# =====================================================
# HISTORIAL
# =====================================================

if "historial" not in st.session_state:
    st.session_state.historial = []


# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("Gestión de Evaluación")

archivo = st.sidebar.file_uploader(
    "Cargar matriz diligenciada",
    type=["xlsx"]
)

procesar = st.sidebar.button(
    "Procesar evaluación"
)

if st.sidebar.button("Nueva evaluación"):

    st.session_state.clear()
    st.rerun()


# ==========================================
# HEADER EJECUTIVO
# ==========================================

fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")

st.markdown("""
<style>

.header-card{
    background:#ffffff;
    border:1px solid #e5e7eb;
    border-radius:20px;
    padding:30px;
    margin-bottom:25px;
    box-shadow:0 4px 12px rgba(0,0,0,0.05);
}

.header-top{
    color:#64748b;
    font-size:13px;
    font-weight:700;
    letter-spacing:1px;
    text-transform:uppercase;
}

.header-title{
    font-size:36px;
    font-weight:800;
    color:#0f172a;
    margin-top:10px;
    margin-bottom:10px;
}

.header-subtitle{
    color:#475569;
    font-size:16px;
}

.header-footer{
    color:#64748b;
    font-size:13px;
    margin-top:15px;
}

</style>
""", unsafe_allow_html=True)

st.markdown(
    f"""
<div class="header-card">

<div class="header-top">
CENTRO DE MONITOREO ESTRATÉGICO
</div>

<div class="header-title">
Índice de Riesgo de Crisis ante Manifestaciones Sociales Violentas
</div>

<div class="header-subtitle">
Sistema Integrado de Evaluación Prospectiva, Alerta Temprana y Apoyo a la Decisión
</div>

<hr>

<div class="header-footer">
Plataforma de monitoreo estratégico | {fecha_actual}
</div>

</div>
""",
unsafe_allow_html=True
)
st.markdown("""
<style>

.metric-card{
    background:white;
    border:1px solid #e5e7eb;
    border-radius:16px;
    padding:18px;
    text-align:center;
    box-shadow:0 2px 8px rgba(0,0,0,0.04);
    min-height:120px;
}

.metric-title{
    font-size:12px;
    font-weight:700;
    color:#64748b;
    text-transform:uppercase;
    letter-spacing:0.5px;
    margin-bottom:10px;
}

.metric-value{
    font-size:32px;
    font-weight:800;
    color:#0f172a;
}

.metric-green{
    color:#15803d;
}

.metric-yellow{
    color:#b45309;
}

.metric-red{
    color:#b91c1c;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# PROCESAMIENTO
# =====================================================

if archivo and procesar:

    try:

        hoja = pd.read_excel(
            archivo,
            sheet_name="Matriz integrada",
            header=None
        )

        fila = 66

        escenario_estable = float(hoja.iloc[fila, 4])
        escenario_creciente = float(hoja.iloc[fila, 6])
        escenario_critico = float(hoja.iloc[fila, 8])

        irc = float(hoja.iloc[fila, 10]) * 100
        iaam = float(hoja.iloc[fila, 12]) * 100

        # ==========================================
        # INDICADORES CRÍTICOS
        # ==========================================

        indicadores_criticos = 0

        for i in range(2, 66):

            valor = str(
                hoja.iloc[i, 8]
            ).strip().upper()

            if valor in ["X", "1", "CRITICO", "CRÍTICO"]:
                indicadores_criticos += 1

        # ==========================================
        # CATEGORÍAS
        # ==========================================

        categorias = {
            "Legitimidad electoral": range(0, 8),
            "Movilización social": range(8, 16),
            "Dinámica digital y mediática": range(16, 24),
            "Disrupción logística": range(24, 28),
            "Violencia y orden público": range(28, 34),
            "Relación civil-militar": range(34, 39),
            "Actores armados ilegales": range(39, 44),
            "Violencia organizada": range(44, 50),
            "Estabilidad institucional": range(50, 56),
            "Variables económicas": range(56, 64)
        }

        categorias_afectadas = 0

        for categoria, filas in categorias.items():

            tiene_critico = False

            for fila_cat in filas:

                fila_excel = fila_cat + 1

                valor = str(
                    hoja.iloc[fila_excel, 8]
                ).strip().upper()

                if valor in ["SI", "SÍ", "X", "1"]:
                    tiene_critico = True

            if tiene_critico:
                categorias_afectadas += 1
            
            # FIN DEL FOR DE CATEGORÍAS
            
        escenario = obtener_escenario_dominante(
            escenario_estable * 100,
            escenario_creciente * 100,
            escenario_critico * 100
        )

        criticidad = determinar_criticidad(irc)

        # =====================================
        # MÉTRICAS PRINCIPALES
        # =====================================

        c1, c2, c3, c4, c5, c6 = st.columns(6)

        with c1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">IRC</div>
                <div class="metric-value">{irc:.0f}%</div>
            </div>
            """, unsafe_allow_html=True)

        with c2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">IAAM</div>
                <div class="metric-value">{iaam:.0f}%</div>
            </div>
            """, unsafe_allow_html=True)

        with c3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Escenario</div>
                <div class="metric-value metric-green">{escenario}</div>
            </div>
            """, unsafe_allow_html=True)

        with c4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Criticidad</div>
                <div class="metric-value">{criticidad}</div>
            </div>
            """, unsafe_allow_html=True)

        with c5:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Indicadores críticos</div>
                <div class="metric-value">{indicadores_criticos}</div>
            </div>
            """, unsafe_allow_html=True)

        with c6:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Categorías afectadas</div>
                <div class="metric-value">{categorias_afectadas}</div>
            </div>
            """, unsafe_allow_html=True)

        # =====================================================
        # RESUMEN EJECUTIVO
        # =====================================================

        resumen = generar_resumen(
            irc,
            iaam,
            escenario
        )

        # =====================================
        # RESUMEN EJECUTIVO
        # =====================================

        st.markdown("""
        <div style="
            background:#ffffff;
            border:1px solid #e5e7eb;
            border-radius:16px;
            padding:22px;
            margin-top:20px;
            margin-bottom:20px;
            box-shadow:0 2px 8px rgba(0,0,0,0.04);
        ">
            <h3 style="
                margin-top:0;
                color:#0f172a;
                font-size:22px;
                font-weight:700;
            ">
                Resumen Ejecutivo Automatizado
            </h3>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="
            background:#f8fafc;
            border-left:5px solid #2563eb;
            border-radius:12px;
            padding:20px;
            color:#334155;
            line-height:1.7;
            margin-bottom:25px;
        ">
            {resumen.replace(chr(10), '<br><br>')}
        </div>
        """, unsafe_allow_html=True)

        # =====================================================
        # ALERTAS
        # =====================================================

        st.markdown(
            """
            <h3 style="
                color:#0f172a;
                font-size:22px;
                font-weight:700;
                margin-top:10px;
                margin-bottom:15px;
            ">
                Alertas Tempranas
            </h3>
            """,
            unsafe_allow_html=True
        )

        if irc >= 70:

            st.error(
                "🔴 ALERTA CRÍTICA\n\nConvergencia de factores críticos con capacidad de escalamiento."
            )

        elif irc >= 40:

            st.warning(
                "🟡 ALERTA PREVENTIVA\n\nIncremento sostenido de indicadores de riesgo."
            )

        else:

            st.success(
                "🟢 ALERTA INFORMATIVA\n\nCondiciones compatibles con estabilidad funcional."
            )

        # =====================================================
        # VISUALIZACIÓN ESTRATÉGICA
        # =====================================================
        
        st.markdown("""
        <h2 style="
            color:#0f172a;
            font-size:32px;
            font-weight:800;
            margin-top:25px;
            margin-bottom:20px;
        ">
        Visualización Estratégica
        </h2>
        """, unsafe_allow_html=True)
        
        graf1, graf2 = st.columns(2)
        
        # =====================================================
        # PROBABILIDAD DE ESCENARIOS
        # =====================================================
        
        with graf1:
        
            st.markdown("""
            <div style="
                background:white;
                border:1px solid #e5e7eb;
                border-radius:20px;
                padding:20px;
                box-shadow:0 6px 18px rgba(0,0,0,0.08);
            ">
                <h3 style="
                    margin:0;
                    color:#0f172a;
                    font-size:24px;
                    font-weight:800;
                ">
                    Probabilidad de Escenarios
                </h3>
            </div>
            """, unsafe_allow_html=True)
        
            dominante_valor = max(
                escenario_estable * 100,
                escenario_creciente * 100,
                escenario_critico * 100
            )
        
            fig_donut = go.Figure(
                data=[
                    go.Pie(
                        labels=[
                            "Estable",
                            "Riesgo creciente",
                            "Crítico"
                        ],
                        values=[
                            escenario_estable * 100,
                            escenario_creciente * 100,
                            escenario_critico * 100
                        ],
                        hole=0.68,
                        sort=False,
                        textinfo="percent",
                        textfont=dict(
                            color="white",
                            size=18
                        ),
                        marker=dict(
                            colors=[
                                "#16a34a",
                                "#d97706",
                                "#dc2626"
                            ],
                            line=dict(
                                color="white",
                                width=4
                            )
                        )
                    )
                ]
            )
        
            fig_donut.update_layout(
                height=500,
                paper_bgcolor="white",
                margin=dict(t=20, b=20, l=20, r=20),
        
                annotations=[
                    dict(
                        text=f"<b>{dominante_valor:.1f}%</b>",
                        x=0.5,
                        y=0.55,
                        showarrow=False,
                        font=dict(
                            size=40,
                            color="#0f172a"
                        )
                    ),
                    dict(
                        text=escenario,
                        x=0.5,
                        y=0.42,
                        showarrow=False,
                        font=dict(
                            size=20,
                            color="#64748b"
                        )
                    )
                ],
        
                legend=dict(
                    orientation="h",
                    y=-0.05,
                    x=0.15
                )
            )
        
            st.plotly_chart(
                fig_donut,
                use_container_width=True
            )
        
        # =====================================================
        # IAAM EJECUTIVO
        # =====================================================
        
        with graf2:
        
            if iaam <= 30:
                color_iaam = "#16a34a"
                nivel_iaam = "BAJA PROBABILIDAD"
        
            elif iaam <= 60:
                color_iaam = "#ca8a04"
                nivel_iaam = "PROBABLE"
        
            elif iaam <= 80:
                color_iaam = "#ea580c"
                nivel_iaam = "ALTA PROBABILIDAD"
        
            else:
                color_iaam = "#dc2626"
                nivel_iaam = "INTERVENCIÓN INMINENTE"
        
            st.markdown("""
            <div style="
                background:white;
                border:1px solid #e5e7eb;
                border-radius:20px;
                padding:20px;
                box-shadow:0 6px 18px rgba(0,0,0,0.08);
            ">
                <h3 style="
                    margin:0;
                    color:#0f172a;
                    font-size:24px;
                    font-weight:800;
                ">
                    Índice de Activación de Asistencia Militar
                </h3>
            </div>
            """, unsafe_allow_html=True)
        
            fig_iaam = go.Figure()
        
            fig_iaam.add_trace(
                go.Indicator(
                    mode="gauge+number",
                    value=iaam,
        
                    number={
                        "suffix":"%",
                        "font":{
                            "size":72,
                            "color":"#0f172a"
                        }
                    },
        
                    gauge={
        
                        "shape":"angular",
        
                        "axis":{
                            "range":[0,100]
                        },
        
                        "bar":{
                            "color":color_iaam,
                            "thickness":0.60
                        },
        
                        "borderwidth":5,
                        "bordercolor":"#cbd5e1",
        
                        "steps":[
                            {"range":[0,30],"color":"#dcfce7"},
                            {"range":[30,60],"color":"#fef3c7"},
                            {"range":[60,80],"color":"#fed7aa"},
                            {"range":[80,100],"color":"#fee2e2"}
                        ],
        
                        "threshold":{
                            "line":{
                                "color":"#111827",
                                "width":10
                            },
                            "value":iaam
                        }
                    }
                )
            )
        
            fig_iaam.update_layout(
                height=500,
                paper_bgcolor="white",
                margin=dict(t=20, b=20, l=20, r=20)
            )
        
            st.plotly_chart(
                fig_iaam,
                use_container_width=True
            )
        
            st.markdown(
                f"""
                <div style="
                    text-align:center;
                    margin-top:-15px;
                    padding:12px;
                ">
                    <span style="
                        color:{color_iaam};
                        font-size:22px;
                        font-weight:800;
                    ">
                        {nivel_iaam}
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )        
        # =====================================================
        # RIESGO POR CATEGORÍA
        # =====================================================

        st.subheader("Riesgo por Categoría")

        radar = go.Figure()

        riesgo_categorias = []

        for categoria, filas in categorias.items():

            estable = 0
            creciente = 0
            critico = 0

            for fila_cat in filas:

                fila_excel = fila_cat + 1

                valor_estable = str(
                    hoja.iloc[fila_excel, 4]
                ).strip().upper()

                valor_creciente = str(
                    hoja.iloc[fila_excel, 6]
                ).strip().upper()

                valor_critico = str(
                    hoja.iloc[fila_excel, 8]
                ).strip().upper()

                if "✓" in valor_estable or valor_estable in ["SI", "SÍ", "X", "1"]:
                    estable += 1

                if "✓" in valor_creciente or valor_creciente in ["SI", "SÍ", "X", "1"]:
                    creciente += 1

                if "✓" in valor_critico or valor_critico in ["SI", "SÍ", "X", "1"]:
                    critico += 1

            total = estable + creciente + critico

            if total == 0:

                riesgo = 0

            else:

                puntaje = (
                    estable * 1
                    + creciente * 2
                    + critico * 3
                )

                promedio = puntaje / total

                riesgo = (promedio / 3) * 100

            riesgo_categorias.append(riesgo)

        radar.add_trace(
            go.Scatterpolar(
                r=riesgo_categorias,
                theta=list(categorias.keys()),
                fill="toself",
                name="Nivel de riesgo"
            )
        )

        radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            height=650
        )

        st.plotly_chart(
            radar,
            use_container_width=True
        )

        # =====================================================
        # ALISTAMIENTO ESTRATÉGICO
        # =====================================================

        alistamiento = generar_alistamiento(
            iaam
        )

        st.subheader(
            "Alistamiento Estratégico"
        )

        st.metric(
            "Nivel IAAM",
            alistamiento["nivel"]
        )

        st.info(
            f"Intención del Comandante: {alistamiento['intencion']}"
        )

        for orden in alistamiento["ordenes"]:
            st.success(orden)

        # ==================================================
        # HISTORIAL
        # ==================================================

        st.subheader("Historial de Evaluaciones")

        st.dataframe(
            pd.DataFrame(
                st.session_state.historial
            ),
            use_container_width=True
        )

    except Exception as e:

        st.error(
            f"Error procesando matriz: {e}"
        )

else:

    st.info(
        "Cargue una matriz diligenciada y pulse 'Procesar evaluación'."
    )
