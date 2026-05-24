import streamlit as st
import requests

API_URL = "https://sistemas-comandas-aps.onrender.com"

st.title("📊 Dashboard")

try:

    resposta = requests.get(
        f"{API_URL}/comandas"
    )

    if resposta.status_code != 200:

        st.error(
            f"Erro na API: {resposta.status_code}"
        )

        st.stop()

    comandas = resposta.json()

    if not isinstance(
        comandas,
        list
    ):

        st.error(
            "Resposta inválida da API"
        )

        st.write(
            comandas
        )

        st.stop()

    abertas = 0
    finalizadas = 0
    faturamento = 0

    for c in comandas:

        status = c.get(
            "status",
            ""
        )

        if status == "ABERTA":

            abertas += 1

        elif status == "FINALIZADA":

            finalizadas += 1

            faturamento += float(
                c.get(
                    "total",
                    0
                )
            )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            label="Comandas abertas",
            value=abertas
        )

    with col2:

        st.metric(
            label="Finalizadas",
            value=finalizadas
        )

    with col3:

        st.metric(
            label="Faturamento",
            value=f"R$ {faturamento:.2f}"
        )


    st.markdown("""

    <style>

    /* CARD */

    div[data-testid="stMetric"]{

        background:#161b22;
        border:1px solid #30363d;
        padding:20px;
        border-radius:15px;
        text-align:center;

    }

    /* TÍTULO */

    div[data-testid="stMetricLabel"]{

        color:white !important;
        font-size:16px !important;
        font-weight:bold;

    }

    /* VALOR */

    div[data-testid="stMetricValue"]{

        color:#a855f7 !important;
        font-size:35px !important;
        font-weight:bold;

    }

    </style>

    """, unsafe_allow_html=True)

except Exception as e:

    st.error(
        f"Erro ao carregar dashboard: {str(e)}"
    )