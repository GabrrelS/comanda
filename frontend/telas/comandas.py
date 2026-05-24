import streamlit as st
import requests
import pandas as pd

API_URL = "https://sistemas-comandas-aps.onrender.com"

st.title("🍽️ Comandas")

# ==========================
# CARREGAR COMANDAS
# ==========================

try:

    r = requests.get(
        f"{API_URL}/comandas",
        timeout=10
    )

    comandas=[]

    if r.status_code==200:
        comandas=r.json()

except:

    comandas=[]


# ==========================
# LISTAR COMANDAS
# ==========================

st.subheader(
    "Comandas"
)

if len(comandas)>0:

    tabela=[]

    for c in comandas:

        tabela.append({

            "ID":c["id"],
            "Mesa":c["mesa"],
            "Status":c["status"],
            "Total":f'R$ {c["total"]:.2f}'

        })

    st.dataframe(
        pd.DataFrame(tabela),
        use_container_width=True
    )

    st.divider()

    st.subheader(
        "Gerenciar comandas"
    )

    for c in comandas:

        with st.container():

            st.write(
                f"""
Mesa: {c["mesa"]}

Status: {c["status"]}

Total: R$ {c["total"]:.2f}
"""
            )

            if c["status"] != "FINALIZADA":

                if st.button(
                    f"Fechar mesa {c['mesa']}",
                    key=f"fechar_{c['id']}"
                ):

                    resposta=requests.put(
                        f"{API_URL}/comandas/{c['id']}/fechar"
                    )

                    if resposta.status_code==200:

                        st.success(
                            "Comanda fechada"
                        )

                        st.rerun()

                    else:

                        st.error(
                            resposta.text
                        )

            else:

                st.success(
                    "✅ Comanda finalizada"
                )

            st.divider()

else:

    st.info(
        "Nenhuma comanda cadastrada"
    )


# ==========================
# NOVA COMANDA
# ==========================

st.subheader(
    "Nova comanda"
)

mesa=st.number_input(
    "Mesa",
    min_value=1
)

if st.button(
    "Criar"
):

    resposta=requests.post(
        f"{API_URL}/comandas",
        json={
            "mesa":mesa
        }
    )

    if resposta.status_code==200:

        st.success(
            "Comanda criada"
        )

        st.rerun()

    else:

        st.error(
            "Erro ao criar"
        )


st.divider()


# ==========================
# ADICIONAR PRODUTOS
# ==========================

st.subheader(
    "Adicionar produto na comanda"
)

try:

    r=requests.get(
        f"{API_URL}/produtos"
    )

    produtos=[]

    if r.status_code==200:
        produtos=r.json()

except:

    produtos=[]


if len(comandas)>0 and len(produtos)>0:

    lista_comandas={

        f"Mesa {c['mesa']}":
        c["id"]

        for c in comandas

        if c["status"]!="FINALIZADA"

    }

    lista_produtos={

        p["nome"]:
        p["id"]

        for p in produtos

    }

    if len(lista_comandas)>0:

        comanda=st.selectbox(
            "Escolha a comanda",
            list(lista_comandas.keys())
        )

        produto=st.selectbox(
            "Produto",
            list(lista_produtos.keys())
        )

        quantidade=st.number_input(
            "Quantidade",
            min_value=1,
            value=1
        )

        if st.button(
            "Adicionar"
        ):

            resposta=requests.post(
                f"{API_URL}/itens",
                json={

                    "comanda_id":
                    lista_comandas[comanda],

                    "produto_id":
                    lista_produtos[produto],

                    "quantidade":
                    quantidade
                }
            )

            if resposta.status_code==200:

                st.success(
                    "Produto adicionado"
                )

                st.rerun()

            else:

                st.error(
                    f"Erro: {resposta.text}"
                )

    else:

        st.warning(
            "Não existem comandas abertas"
        )

else:

    st.warning(
        "Cadastre produtos e comandas primeiro"
    )