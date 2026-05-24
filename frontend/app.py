import streamlit as st
import requests

API_URL = "https://sistema-comanda.onrender.com"

# 1. Configuração da Página
st.set_page_config(page_title="Sistema de Comandas", layout="wide")

# 2. Inicialização do Estado
#if "logado" not in st.session_state:
 #   st.session_state.logado = False
#if "tipo" not in st.session_state:
 #   st.session_state.tipo = None
#if "token" not in st.session_state:
 #   st.session_state.token = None

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
                st.session_state.tipo = dados["tipo"]  # Aqui assume "Admin", "Operador", etc.
                st.session_state.token = dados["access_token"]
                st.rerun()
            else:
                st.error("Login inválido")
        except Exception as e:
            st.error(f"Erro ao conectar: {e}")

# --- FUNÇÃO DE LOGOUT ---
def logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# --- DEFINIÇÃO DA NAVEGAÇÃO (O BLOCO DE PERMISSÕES) ---

if not st.session_state.logado:
    # Enquanto não logar, esta é a ÚNICA página que o Streamlit reconhece
    pg = st.navigation([st.Page(login_page, title="Entrar", icon="🔒")])
else:
    # 1. Definimos todas as páginas possíveis (apontando para a pasta /views)
    p_dashboard = st.Page("views/dashboard.py", title="Dashboard", icon="📊")
    p_produtos = st.Page("views/produtos.py", title="Produtos", icon="📦")
    p_comandas = st.Page("views/comandas.py", title="Comandas", icon="📝")
    p_relatorios = st.Page("views/relatorios.py", title="Relatórios", icon="📁")
    p_usuarios = st.Page("views/usuarios.py", title="Gerir Usuários", icon="👥")

    # 2. Criamos a lógica de quem vê o quê (O BLOCO DE ADMIN/OPERADOR)
    paginas_visiveis = []

    if st.session_state.tipo == "Admin":
        # Admin vê tudo, incluindo a gestão de utilizadores
        paginas_visiveis = [p_dashboard, p_produtos, p_comandas, p_relatorios, p_usuarios]
    
    elif st.session_state.tipo == "Operador":
        # Operador tem acesso reduzido
        paginas_visiveis = [p_dashboard, p_comandas]
    
    elif st.session_state.tipo == "Sistema":
        # Outro perfil que tinhas no código original
        paginas_visiveis = [p_comandas, p_relatorios]

    # 3. Criamos o menu com as páginas filtradas
    pg = st.navigation(paginas_visiveis)
    
    # Botão de sair na barra lateral
    st.sidebar.button("Sair", on_click=logout)

# Executa a aplicação
pg.run()