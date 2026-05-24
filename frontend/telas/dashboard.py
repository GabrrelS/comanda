import streamlit as st
import requests
from streamlit_extras.metric_cards import style_metric_cards

API_URL="https://sistemas-comandas-aps.onrender.com"

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

    # garante que é uma lista
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

    abertas=0
    cozinha=0
    finalizadas=0
    faturamento=0

    for c in comandas:

        status=c.get(
            "status",
            ""
        )

        if status=="ABERTA":

            abertas+=1

        elif status=="NA_COZINHA":

            cozinha+=1

        elif status=="FINALIZADA":

            finalizadas+=1

            faturamento+=float(

                c.get(
                    "total",
                    0
                )
            )

    col1,col2,col3,col4=st.columns(4)

    with col1:

        st.metric(
            "Comandas abertas",
            abertas
        )

    with col2:

        st.metric(
            "Na cozinha",
            cozinha
        )

    with col3:

        st.metric(
            "Finalizadas",
            finalizadas
        )

    with col4:

        st.metric(
            "Faturamento",
            f"R$ {faturamento:.2f}"
        )

    st.markdown("""
    <style>

    [data-testid="stMetric"]{
    background-color: #1e1e1e;
    border: 1px solid #333333;
    padding: 15px;
    border-radius: 12px;
    }

    [data-testid="stMetricLabel"]{
    color:white;
    font-size:16px;
    }

    [data-testid="stMetricValue"]{
    color:#a855f7;
    font-size:30px;
    }

    </style>
    """, unsafe_allow_html=True)

except Exception as e:

    st.error(
        f"Erro ao carregar dashboard: {str(e)}"
    )