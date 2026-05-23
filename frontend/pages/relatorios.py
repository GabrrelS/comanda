import streamlit as st
import requests
import pandas as pd

API_URL="https://sistema-comanda.onrender.com"

st.title("📋 Relatórios")

try:

    resposta = requests.get(
        f"{API_URL}/relatorios"
    )

    if resposta.status_code != 200:

        st.error(
            f"Erro API: {resposta.status_code}"
        )

        st.stop()

    dados = resposta.json()

    if not isinstance(
        dados,
        list
    ):

        st.error(
            "Formato inválido recebido da API"
        )

        st.write(
            dados
        )

        st.stop()

    if len(dados) > 0:

        df = pd.DataFrame(
            dados
        )

        st.dataframe(
            df,
            use_container_width=True
        )

        total=0

        # procura a coluna correta
        if "valor" in df.columns:

            total=df["valor"].fillna(
                0
            ).sum()

        elif "total" in df.columns:

            total=df["total"].fillna(
                0
            ).sum()

        st.metric(

            "Faturamento total",

            f"R$ {total:.2f}"
        )

        csv=df.to_csv(
            index=False
        )

        st.download_button(

            "📥 Baixar relatório CSV",

            csv,

            file_name="relatorio.csv",

            mime="text/csv"
        )

    else:

        st.warning(
            "Nenhuma comanda finalizada encontrada"
        )

except Exception as e:

    st.error(
        f"Erro ao gerar relatório: {str(e)}"
    )