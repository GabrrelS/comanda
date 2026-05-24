import streamlit as st
import requests
import pandas as pd

API_URL = "https://sistema-comanda.onrender.com"

# 1. Verificação de segurança
if not st.session_state.get("logado"):
    st.warning("Faça login")
    st.stop()

# 2. Header com Token
headers = {
    "Authorization": f"Bearer {st.session_state.token}"
}

st.title("📋 Relatórios")

try:
    # Requisição com autenticação
    resposta = requests.get(
        f"{API_URL}/relatorios",
        headers=headers
    )

    if resposta.status_code != 200:
        st.error(f"Erro API: {resposta.status_code}")
        st.stop()

    dados = resposta.json()

    # Verifica se os dados são uma lista
    if not isinstance(dados, list):
        st.error("Formato inválido recebido da API")
        st.write(dados)
        st.stop()

    if len(dados) > 0:
        df = pd.DataFrame(dados)

        # Exibe a tabela
        st.dataframe(df, use_container_width=True)

        # Cálculo do faturamento total
        total = 0.0
        if "valor" in df.columns:
            total = df["valor"].fillna(0).sum()
        elif "total" in df.columns:
            total = df["total"].fillna(0).sum()
        elif "valor_total" in df.columns:
            total = df["valor_total"].fillna(0).sum()

        st.metric("Faturamento total", f"R$ {total:.2f}")

        # Preparação do download
        csv = df.to_csv(index=False).encode('utf-8')

        st.download_button(
            label="📥 Baixar relatório CSV",
            data=csv,
            file_name="relatorio.csv",
            mime="text/csv"
        )
    else:
        st.warning("Nenhuma comanda finalizada encontrada")

except Exception as e:
    st.error(f"Erro ao gerar relatório: {str(e)}")