import streamlit as st
import requests
import pandas as pd

API_URL="https://sistema-comanda.onrender.com"

st.title("🍽️ Comandas")

try:

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

            tabela=[]

            for c in comandas:

                tabela.append({

                    "ID": c.get(
                        "id",
                        "-"
                    ),

                    "Mesa": c.get(
                        "mesa",
                        "-"
                    ),

                    "Status": c.get(
                        "status",
                        "-"
                    ),

                    "Total": c.get(
                        "valor_total",
                        0
                    )

                })

            df = pd.DataFrame(
                tabela
            )

            st.dataframe(
                df,
                use_container_width=True
            )

    else:

        st.error(
            f"Erro API: {resposta.status_code}"
        )

except Exception as e:

    st.error(
        f"Erro: {str(e)}"
    )


st.divider()

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

    try:

        requests.post(

            f"{API_URL}/comandas",

            json={

                "mesa":mesa
            }
        )

        st.success(
            "Comanda criada"
        )

        st.rerun()

    except Exception as e:

        st.error(
            str(e)
        )