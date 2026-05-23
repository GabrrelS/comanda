import streamlit as st
import requests

API_URL="https://sistema-comanda.onrender.com"

st.title("🍴 Comandas")

tab1, tab2 = st.tabs([
    "Nova Comanda",
    "Gerenciar"
])

# ==========================
# CRIAR COMANDA
# ==========================

with tab1:

    mesa = st.number_input(
        "Número da mesa",
        min_value=1
    )

    if st.button(
        "Criar Comanda"
    ):

        resposta = requests.post(
            f"{API_URL}/comandas",
            json={
                "mesa": mesa
            }
        )

        if resposta.status_code in [200, 201]:

            st.success(
                "Comanda criada"
            )

            st.rerun()

        else:

            st.error(
                "Erro ao criar"
            )


# ==========================
# GERENCIAR
# ==========================

with tab2:

    resposta = requests.get(
        f"{API_URL}/comandas"
    )

    if resposta.status_code == 200:

        comandas = resposta.json()

        if not comandas:

            st.info(
                "Nenhuma comanda cadastrada"
            )

        else:

            produtos = requests.get(
                f"{API_URL}/produtos"
            ).json()

            lista_produtos = {

                p["nome"]: p["id"]
                for p in produtos
            }

            for c in comandas:

                # esconder finalizadas
                if c.get(
                    "status"
                ) == "FINALIZADA":

                    continue

                st.subheader(
                    f"Comanda {c['id']}"
                )

                st.write(
                    f"Mesa: {c.get('mesa')}"
                )

                st.write(
                    f"Status: {c.get('status')}"
                )

                st.write(
                    f"Total: R$ {c.get('total',0)}"
                )

                produto = st.selectbox(
                    "Produto",
                    lista_produtos.keys(),
                    key=f"produto_{c['id']}"
                )

                quantidade = st.number_input(
                    "Quantidade",
                    min_value=1,
                    key=f"qtd_{c['id']}"
                )

                col1, col2, col3, col4 = st.columns(4)

                with col1:

                    if st.button(
                        "Adicionar item",
                        key=f"add_{c['id']}"
                    ):

                        requests.post(
                            f"{API_URL}/comandas/{c['id']}/itens",
                            json={
                                "produto_id":
                                lista_produtos[
                                    produto
                                ],

                                "quantidade":
                                quantidade
                            }
                        )

                        st.rerun()

                with col2:

                    if st.button(
                        "Enviar cozinha",
                        key=f"cozinha_{c['id']}"
                    ):

                        requests.put(
                            f"{API_URL}/comandas/{c['id']}",
                            json={
                                "status":
                                "NA_COZINHA"
                            }
                        )

                        st.rerun()

                with col3:

                    if st.button(
                        "Fechar",
                        key=f"fechar_{c['id']}"
                    ):

                        requests.put(
                            f"{API_URL}/comandas/{c['id']}/fechar"
                        )

                        st.rerun()

                with col4:

                    if st.button(
                        "Excluir",
                        key=f"delete_{c['id']}"
                    ):

                        requests.delete(
                            f"{API_URL}/comandas/{c['id']}"
                        )

                        st.success(
                            "Comanda excluída"
                        )

                        st.rerun()

                st.divider()