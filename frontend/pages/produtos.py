import streamlit as st
import requests

API_URL = "https://sistema-comanda.onrender.com"

# 1. Verificação de segurança
if not st.session_state.get("logado"):
    st.warning("Faça login")
    st.stop()

# 2. Header com Token
headers = {
    "Authorization": f"Bearer {st.session_state.get('token', '')}"
}

st.title("📦 Produtos")

# ==========================
# CADASTRAR (POST)
# ==========================
st.subheader("Novo produto")

nome = st.text_input("Nome")
preco = st.number_input("Preço", min_value=0.0)
estoque = st.number_input("Estoque", min_value=0)

if st.button("Salvar"):
    try:
        payload = {
            "nome": nome,
            "preco": preco,
            "estoque": estoque,
            "unidade": "UN"
        }

        res = requests.post(
            f"{API_URL}/produtos",
            json=payload,
            headers=headers
        )

        if res.status_code in [200, 201]:
            st.success("Produto salvo")
            st.rerun()
        else:
            st.error(f"Erro ao salvar: {res.status_code}")

    except Exception as e:
        st.error(f"Erro na conexão: {str(e)}")

st.divider()

# ==========================
# LISTAR E DELETAR (GET / DELETE)
# ==========================
st.subheader("Produtos cadastrados")

try:
    resposta = requests.get(f"{API_URL}/produtos", headers=headers)

    if resposta.status_code == 200:
        produtos = resposta.json()

        if not produtos:
            st.info("Nenhum produto cadastrado")
        else:
            for p in produtos:
                col1, col2 = st.columns(2)

                with col1:
                    st.write(
                        f"🍔 {p.get('nome')} | R$ {p.get('preco', 0):.2f} | Est: {p.get('estoque', 0)}"
                    )

                with col2:
                    if st.button("🗑️", key=f"del_{p.get('id')}"):
                        res_del = requests.delete(
                            f"{API_URL}/produtos/{p.get('id')}",
                            headers=headers
                        )

                        if res_del.status_code in [200, 204]:
                            st.success("Removido")
                            st.rerun()
                        else:
                            st.error(f"Erro ao deletar: {res_del.status_code}")
    else:
        st.error(f"Erro na API: {resposta.status_code}")

except Exception as e:
    st.error(f"Erro ao carregar lista: {str(e)}")