import streamlit as st
import requests

API_URL = "https://sistema-comanda.onrender.com"

# 1. Configuração inicial
st.set_page_config(page_title="Sistema de Comandas", layout="wide")

# 2. Inicialização do Session State
if "logado" not in st.session_state:
    st.session_state.logado = False
if "tipo" not in st.session_state:
    st.session_state.tipo = None
if "token" not in st.session_state:
    st.session_state.token = None

# --- FUNÇÃO DE LOGIN ---
def login_page():
    st.title("🔐 Login")
    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        try:
            resposta = requests.post(
                f"{API_URL}/login",
                json={"email": email, "senha": senha}
            )
            if resposta.status_code == 200:
                dados = resposta.json()
                st.session_state.logado = True
                st.session_state.tipo = dados["tipo"]
                st.session_state.token = dados["access_token"]
                st.rerun()
            else:
                st.error("Login inválido")
        except Exception as e:
            st.error(f"Erro ao conectar com o backend: {e}")

# --- FUNÇÃO DE LOGOUT ---
def logout():
    st.session_state.logado = False
    st.session_state.tipo = None
    st.session_state.token = None
    st.rerun()

# --- GERENCIAMENTO DE NAVEGAÇÃO ---

if not st.session_state.logado:
    # Se não está logado, a única página que existe no sistema é o Login
    pg = st.navigation([st.Page(login_page, title="Autenticação", icon="🔒")])
else:
    # Definimos os objetos de página (apontando para a nova pasta 'views')
    p_dashboard = st.Page("views/dashboard.py", title="Dashboard", icon="📊")
    p_produtos = st.Page("views/produtos.py", title="Produtos", icon="📦")
    p_comandas = st.Page("views/comandas.py", title="Comandas", icon="📝")
    p_relatorios = st.Page("views/relatorios.py", title="Relatórios", icon="📁")

    # Filtramos as páginas de acordo com o tipo de ator
    paginas_disponiveis = []
    
    if st.session_state.tipo == "Admin":
        paginas_disponiveis = [p_dashboard, p_produtos, p_comandas, p_relatorios]
    elif st.session_state.tipo == "Operador":
        paginas_disponiveis = [p_dashboard, p_comandas]
    elif st.session_state.tipo == "Sistema":
        paginas_disponiveis = [p_comandas, p_relatorios]

    # Criamos o menu lateral com as páginas permitidas
    pg = st.navigation({"Menu Principal": paginas_disponiveis})
    
    # Botão de sair na sidebar
    st.sidebar.button("Sair", on_click=logout)

# Executa a página selecionada
pg.run()