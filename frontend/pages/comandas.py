import streamlit as st
import requests
import pandas as pd

API_URL = "https://sistema-comanda.onrender.com"

# Verificação de segurança
if not st.session_state.get("logado"):
    st.warning("Faça login")
    st.stop()

# Headers globais
headers = {
    "Authorization": f"Bearer {st.session_state.get('token', '')}"
}

st.title("🍽️ Comandas")

# --- BLOCO DE LEITURA (GET) ---
try:
    resposta = requests.get(f"{API_URL}/comandas", headers=headers)

    if resposta.status_code == 200:
        comandas = resposta.json()

        if not comandas:
            st.info("Nenhuma comanda cadastrada")
        else:
            tabela = []
            for c in comandas:
                tabela.append({
                    "ID": c.get("id", "-"),
                    "Mesa": c.get("mesa", "-"),
                    "Status": c.get("status", "-"),
                    "Total": c.get("valor_total", 0)
                })

            df = pd.DataFrame(tabela)
            st.dataframe(df, use_container_width=True)

    else:
        st.error(f"Erro API: {resposta.status_code}")

except Exception as e:
    st.error(f"Erro na conexão: {str(e)}")

st.divider()

# --- BLOCO DE CRIAÇÃO (POST) ---
st.subheader("Nova comanda")

mesa = st.number_input("Mesa", min_value=1)

if st.button("Criar"):
    try:
        dados = {"mesa": mesa}
        resposta_post = requests.post(
            f"{API_URL}/comandas",
            json=dados,
            headers=headers
        )

        if resposta_post.status_code in [200, 201]:
            st.success("Comanda criada com sucesso")
            st.rerun()
        else:
            st.error(f"Erro ao criar comanda: {resposta_post.status_code}")

    except Exception as e:
        st.error(f"Falha na requisição: {str(e)}")