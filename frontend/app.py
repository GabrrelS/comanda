import streamlit as st
import requests
import os

API_URL = "https://sistemas-comandas-aps.onrender.com"

st.set_page_config(
    page_title="Sistema de Comandas",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ======================
# SESSION
# ======================

if "logado" not in st.session_state:
    st.session_state.logado = False

if "tipo" not in st.session_state:
    st.session_state.tipo = None


# ======================
# CAMINHO BASE
# ======================

BASE_DIR = os.path.dirname(__file__)


# ======================
# ESCONDER SIDEBAR
# ======================

if not st.session_state.logado:

    st.markdown("""
    <style>
        section[data-testid="stSidebar"]{
            display:none;
        }
    </style>
    """, unsafe_allow_html=True)


# ======================
# LOGIN
# ======================

if not st.session_state.logado:

    st.title("🔐 Login")

    email = st.text_input(
        "Email"
    )

    senha = st.text_input(
        "Senha",
        type="password"
    )

    if st.button("Entrar"):

        try:

            resposta = requests.post(
                f"{API_URL}/login",
                json={
                    "email": email,
                    "senha": senha
                },
                timeout=10
            )

            if resposta.status_code == 200:

                dados = resposta.json()

                st.session_state.logado = True
                st.session_state.tipo = dados["tipo"]

                st.rerun()

            else:

                st.error(
                    "Falha no login"
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "Não foi possível conectar ao backend"
            )

        except requests.exceptions.Timeout:

            st.error(
                "Servidor demorou para responder"
            )

        except Exception as e:

            st.error(
                f"Erro: {str(e)}"
            )


# ======================
# SISTEMA
# ======================

else:

    st.sidebar.title(
        "🍴 Sistema"
    )

    menu=[]

    # ADMIN
    if st.session_state.tipo=="admin":

        menu=[
            "Dashboard",
            "Produtos",
            "Comandas",
            "Relatórios"
        ]

    # GARÇOM / OPERADOR
    elif st.session_state.tipo=="operador":

        menu=[
            "Comandas"
        ]

    # CAIXA
    elif st.session_state.tipo=="caixa":

        menu=[
            "Comandas",
            "Relatórios"
        ]

    pagina=st.sidebar.radio(
        "Menu",
        menu
    )

    if st.sidebar.button(
        "Sair"
    ):

        st.session_state.logado=False
        st.session_state.tipo=None

        st.rerun()

    # ======================
    # CARREGAR TELAS
    # ======================

    if pagina == "Dashboard":

        exec(
            open(
                os.path.join(
                    BASE_DIR,
                    "telas",
                    "dashboard.py"
                ),
                encoding="utf8"
            ).read()
        )

    elif pagina == "Produtos":

        exec(
            open(
                os.path.join(
                    BASE_DIR,
                    "telas",
                    "produtos.py"
                ),
                encoding="utf8"
            ).read()
        )

    elif pagina == "Comandas":

        exec(
            open(
                os.path.join(
                    BASE_DIR,
                    "telas",
                    "comandas.py"
                ),
                encoding="utf8"
            ).read()
        )

    elif pagina == "Relatórios":

        exec(
            open(
                os.path.join(
                    BASE_DIR,
                    "telas",
                    "relatorios.py"
                ),
                encoding="utf8"
            ).read()
        )