import streamlit as st
import requests

API_URL = "https://sistema-comanda.onrender.com"

st.title("🔐 Login")

email = st.text_input(
    "Email"
)

senha = st.text_input(
    "Senha",
    type="password"
)

if st.button("Entrar"):

    dados = {
        "email": email.strip(),
        "senha": senha
    }

    try:

        r = requests.post(
            f"{API_URL}/login",
            json=dados
        )

        if r.status_code == 200:

            usuario = r.json()

            # salva sessão
            st.session_state.logado = True
            st.session_state.tipo = usuario["tipo"]

            st.success(
                f"Bem-vindo {usuario['nome']}"
            )

            st.rerun()

        else:

            st.error(
                f"Erro {r.status_code}"
            )       

            st.write(
                r.text
            )

    except Exception as e:

        st.error(
            f"Erro conexão: {str(e)}"
        )