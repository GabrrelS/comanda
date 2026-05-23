import streamlit as st
import requests

API_URL="https://sistema-comanda.onrender.com"

st.title("📦 Produtos")

# ==========================
# CADASTRAR
# ==========================

st.subheader(
    "Novo produto"
)

nome=st.text_input(
    "Nome"
)

preco=st.number_input(
    "Preço",
    min_value=0.0
)

estoque=st.number_input(
    "Estoque",
    min_value=0
)

if st.button(
    "Salvar"
):

    resposta=requests.post(

        f"{API_URL}/produtos",

        json={

            "nome":nome,

            "preco":preco,

            "estoque":estoque,

            "unidade":"UN"
        }
    )

    if resposta.status_code in [200,201]:

        st.success(
            "Produto salvo"
        )

        st.rerun()

    else:

        st.error(
            "Erro ao salvar"
        )


st.divider()

# ==========================
# LISTAR
# ==========================

st.subheader(
    "Produtos cadastrados"
)

try:

    resposta=requests.get(
        f"{API_URL}/produtos"
    )

    produtos=resposta.json()

    if not produtos:

        st.info(
            "Nenhum produto cadastrado"
        )

    else:

        for p in produtos:

            col1,col2=st.columns(
                [5,1]
            )

            with col1:

                st.write(

                    f"🍔 {p['nome']} | "
                    f"R$ {p['preco']} | "
                    f"Estoque: {p['estoque']}"
                )

            with col2:

                if st.button(
                    "🗑️",
                    key=f"delete_{p['id']}"
                ):

                    requests.delete(
                        f"{API_URL}/produtos/{p['id']}"
                    )

                    st.success(
                        "Produto removido"
                    )

                    st.rerun()

except Exception as e:

    st.error(
        f"Erro: {str(e)}"
    )