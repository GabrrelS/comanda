import streamlit as st
import requests

API_URL="https://sistemas-comandas-aps.onrender.com"

st.title("📦 Produtos")

# ==========================
# CADASTRAR
# ==========================

st.subheader(
    "Novo produto"
)

nome = st.text_input(
    "Nome"
)

preco = st.number_input(
    "Preço",
    min_value=0.0
)

estoque = st.number_input(
    "Estoque",
    min_value=0
)

if st.button(
    "Salvar"
):

    resposta = requests.post(

        f"{API_URL}/produtos",

        json={

            "nome": nome,
            "preco": preco,
            "estoque": estoque,
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
            f"Erro: {resposta.text}"
        )


st.divider()

# ==========================
# LISTAR
# ==========================

st.subheader(
    "Produtos cadastrados"
)

try:

    resposta = requests.get(
        f"{API_URL}/produtos"
    )

    produtos = resposta.json()

    if len(produtos)==0:

        st.info(
            "Nenhum produto cadastrado"
        )

    else:

        for p in produtos:

            col1,col2,col3 = st.columns(
                [7,1,1]
            )

            with col1:

                st.write(

                    f"🍔 {p['nome']} | "
                    f"R$ {p['preco']:.2f} | "
                    f"Estoque: {p['estoque']}"
                )

            # ==================
            # EDITAR
            # ==================

            with col2:

                if st.button(
                    "✏️",
                    key=f"editar_{p['id']}"
                ):

                    st.session_state[
                        "editar"
                    ]=p["id"]


            # ==================
            # EXCLUIR
            # ==================

            with col3:

                if st.button(
                    "🗑️",
                    key=f"delete_{p['id']}"
                ):

                    resposta=requests.delete(
                        f"{API_URL}/produtos/{p['id']}"
                    )

                    if resposta.status_code==200:

                        st.success(
                            "Produto removido"
                        )

                        st.rerun()

                    else:

                        erro=resposta.json()

                        st.error(
                            erro["detail"]
                        )


            # ==================
            # FORM EDITAR
            # ==================

            if (

                "editar" in st.session_state

                and

                st.session_state[
                    "editar"
                ]==p["id"]

            ):

                st.write(
                    "Editar produto"
                )

                novo_nome=st.text_input(
                    "Nome",
                    value=p["nome"],
                    key=f"nome_{p['id']}"
                )

                novo_preco=st.number_input(
                    "Preço",
                    value=float(
                        p["preco"]
                    ),
                    key=f"preco_{p['id']}"
                )

                novo_estoque=st.number_input(
                    "Estoque",
                    value=int(
                        p["estoque"]
                    ),
                    key=f"estoque_{p['id']}"
                )

                if st.button(
                    "Salvar alterações",
                    key=f"salvar_{p['id']}"
                ):

                    resposta=requests.put(
                        f"{API_URL}/produtos/{p['id']}",

                        json={

                            "nome":novo_nome,

                            "preco":novo_preco,

                            "estoque":novo_estoque,

                            "unidade":"UN"
                        }
                    )

                    if resposta.status_code==200:

                        st.success(
                            "Produto atualizado"
                        )

                        del st.session_state[
                            "editar"
                        ]

                        st.rerun()

                    else:

                        st.error(
                            resposta.text
                        )

            st.divider()

except Exception as e:

    st.error(
        f"Erro: {str(e)}"
    )