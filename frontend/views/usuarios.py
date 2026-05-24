import streamlit as st
import requests

# URL do seu backend
API_URL = "https://sistema-comanda.onrender.com"

def render_usuarios():
    st.title("👥 Gestão de Usuários")
    st.markdown("---")

    # Criamos abas para organizar: uma para listar e outra para cadastrar
    aba_listar, aba_cadastrar = st.tabs(["Lista de Usuários", "Cadastrar Novo"])

    with aba_cadastrar:
        st.subheader("Criar novo acesso")
        
        with st.form("form_cadastro"):
            nome = st.text_input("Nome Completo")
            email = st.text_input("E-mail (será usado para login)")
            senha = st.text_input("Senha", type="password")
            tipo = st.selectbox("Nível de Acesso", ["Admin", "Operador", "Sistema"])
            
            btn_salvar = st.form_submit_button("Finalizar Cadastro")

            if btn_salvar:
                if not nome or not email or not senha:
                    st.warning("Por favor, preencha todos os campos.")
                else:
                    # Monta o corpo da requisição
                    payload = {
                        "nome": nome,
                        "email": email,
                        "senha": senha,
                        "tipo": tipo
                    }
                    
                    # Se você já tiver o token no session_state, envie no header
                    headers = {}
                    if "token" in st.session_state:
                        headers["Authorization"] = f"Bearer {st.session_state.token}"
                    
                    try:
                        # Faz a chamada para o seu backend (ajuste a rota se for /users ou /usuarios)
                        response = requests.post(f"{API_URL}/users", json=payload, headers=headers)
                        
                        if response.status_code == 200 or response.status_code == 201:
                            st.success(f"Usuário {nome} cadastrado com sucesso!")
                        else:
                            st.error(f"Erro ao cadastrar: {response.text}")
                    except Exception as e:
                        st.error(f"Não foi possível conectar ao servidor: {e}")

    with aba_listar:
        st.subheader("Usuários Ativos")
        # Aqui você pode fazer um GET para listar quem já existe
        if st.button("Atualizar Lista"):
            headers = {"Authorization": f"Bearer {st.session_state.get('token')}"}
            res = requests.get(f"{API_URL}/users", headers=headers)
            if res.status_code == 200:
                st.table(res.json())
            else:
                st.error("Erro ao carregar lista.")

# Chamamos a função para renderizar o conteúdo
render_usuarios()