import streamlit as st
import os
import re

# Caminhos Base do Opensquad (Um nível acima da pasta app_python)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BD_ENTRADA = os.path.join(BASE_DIR, 'bd_entrada')
BD_SAIDA = os.path.join(BASE_DIR, 'bd_saida')
AGENTS_DIR = os.path.join(BASE_DIR, 'agents')

# Configuração da Página Web
st.set_page_config(
    page_title="Varejo Insight | AI Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização CSS Extra para Streamlit
st.markdown("""
    <style>
    .main { background-color: #0b0c10; color: #e0e0e0; }
    h1, h2, h3 { color: #66A6FF !important; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; background: linear-gradient(135deg, #66A6FF, #3B82F6); color: white; border: none;}
    .report-card { background: #1a1a24; padding: 20px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.05); margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# Menu Lateral (Sidebar) de Navegação
st.sidebar.title("🛒 Varejo Insight")
st.sidebar.caption("Squad AI de Alta Performance")
st.sidebar.markdown("---")
page = st.sidebar.radio("Comando da Squad", [
    "📥 1. Intake de Dados (Entradas)", 
    "🤖 2. Reunião de Equipe (Perfis)", 
    "📊 3. Mesa da Diretoria (Saídas)"
])
st.sidebar.markdown("---")
st.sidebar.button("▶ Run Pipeline (Opensquad)", help="Em breve: Acionamento via CLI Integrada")

# ----------------------------------------------------------------------------------
# TELA 1: INTAKE DE DADOS
# ----------------------------------------------------------------------------------
if page == "📥 1. Intake de Dados (Entradas)":
    st.header("📥 Gestão de Bases de Operação")
    st.write("Insira seus Arquivos CSV (usando separador `;` e codificação `UTF-8`) para alimentar a pasta `bd_entrada` da equipe.")
    
    # Upload File Drag and Drop nativo
    uploaded_files = st.file_uploader(
        "Arraste as planilhas do seu ERP: Estoque Filial, Vendas Históricas e Estoque CD (.csv)", 
        type="csv", 
        accept_multiple_files=True
    )
    
    if uploaded_files:
        if st.button("Salvar Bases na Pasta bd_entrada"):
            for f in uploaded_files:
                file_path = os.path.join(BD_ENTRADA, f.name)
                # O Python lê os bytes e escreve no disco local
                with open(file_path, "wb") as disk_file:
                    disk_file.write(f.getbuffer())
            st.success(f"Sucesso! {len(uploaded_files)} bases gravadas para o Agente Inicial!")
    
    st.subheader("📚 Arquivos Atuais na Doca (bd_entrada)")
    try:
        arquivos = [f for f in os.listdir(BD_ENTRADA) if f.endswith('.csv')]
        if not arquivos:
            st.info("A pasta bd_entrada está limpa. Nenhum fornecimento agendado.")
        else:
            for f in arquivos:
                st.markdown(f"- 📄 `{f}`")
    except Exception:
        st.error("Diretório bd_entrada não encontrado. Crie a pasta raiz.")


# ----------------------------------------------------------------------------------
# TELA 2: GESTÃO DE AGENTES (Edição de .agent.md)
# ----------------------------------------------------------------------------------
elif page == "🤖 2. Reunião de Equipe (Perfis)":
    st.header("🤖 Cérebro da Squad")
    st.write("Clique em um Analista Especialista para visualizar e reajustar suas diretrizes e parâmetros operacionais (DNA).")
    
    try:
        arquivos_agentes = [f for f in os.listdir(AGENTS_DIR) if f.endswith('.agent.md')]
        if not arquivos_agentes:
            st.warning("Nenhum agente localizado em `/agents`.")
        else:
            # Lista de seleção de abas igual ao Streamlit Tabs
            tabs = st.tabs([f.replace('.agent.md', '').replace('-', ' ').title() for f in arquivos_agentes])
            
            for index, agente_arquivo in enumerate(arquivos_agentes):
                path_agente = os.path.join(AGENTS_DIR, agente_arquivo)
                with open(path_agente, "r", encoding="utf-8") as f_aberto:
                    conteudo = f_aberto.read()
                
                # Extrai Name e Icon prático
                nome = re.search(r'name:\s*"(.*)"', conteudo)
                icone = re.search(r'icon:\s*"(.*)"', conteudo)
                titulo = re.search(r'title:\s*"(.*)"', conteudo)
                
                nome_formatado = f"{icone.group(1)} {nome.group(1)}" if icone and nome else agente_arquivo
                subtitulo = titulo.group(1) if titulo else "Analista Sistêmico"
                
                with tabs[index]:
                    st.subheader(nome_formatado)
                    st.caption(f"Cargo: {subtitulo}")
                    
                    st.markdown("---")
                    # Editor Interativo (Streamlit renderiza a textArea de altura variável)
                    st.markdown("**Regras de Prompt (Edição em Tempo Real do .agent.md):**")
                    novo_conteudo = st.text_area(
                        "Comportamento do Modelo:", 
                        value=conteudo, 
                        height=500, 
                        key=f"text_{agente_arquivo}"
                    )
                    
                    if st.button("💾 Salvar DNA do Agente", key=f"btn_{agente_arquivo}"):
                        with open(path_agente, "w", encoding="utf-8") as file_save:
                            file_save.write(novo_conteudo)
                        st.success(f"Comportamento de '{nome.group(1)}' salvo no disco físico com sucesso!")
    except Exception as e:
        st.error(f"Erro lendo agentes: {str(e)}")


# ----------------------------------------------------------------------------------
# TELA 3: SAÍDAS E RELATÓRIOS (Dashboards / CSV Masticados)
# ----------------------------------------------------------------------------------
elif page == "📊 3. Mesa da Diretoria (Saídas)":
    st.header("📊 Painel Consolidado de Diretoria")
    st.write("Acompanhe o Sumário Executivo aprovado da Squad e efetue o Download direto das bases pré-mastigadas para o seu ERP.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📝 Relatório Markdown Final (Aprovado)")
        try:
            arquivos_saida = [f for f in os.listdir(BD_SAIDA) if f.endswith('.md')]
            if arquivos_saida:
                ultimo_md = sorted(arquivos_saida)[-1]
                path_md = os.path.join(BD_SAIDA, ultimo_md)
                with open(path_md, "r", encoding="utf-8") as f_md:
                    st.markdown(f"<div class='report-card'>", unsafe_allow_html=True)
                    st.markdown(f"**Lendo Checkpoint:** `{ultimo_md}`")
                    st.write("---")
                    st.markdown(f_md.read())
                    st.markdown(f"</div>", unsafe_allow_html=True)
            else:
                st.info("Nenhum Resumo `.md` foi encontrado. O pipeline foi engatilhado hoje?")
        except Exception:
             st.info("O diretório `bd_saida` parece estar sem dados Markdown.")

    with col2:
        st.subheader("💾 Carga para o ERP (CSV)")
        st.write("Estes são os arquivos que o Agente Diego (ou a Automação Final) preparou com as matrizes aprovadas. Baixe aqui para injetar no sistema de suprimentos raiz.")
        
        try:
            arquivos_csv = [f for f in os.listdir(BD_SAIDA) if f.endswith('.csv')]
            if arquivos_csv:
                for f_csv in arquivos_csv:
                    st.markdown(f"### 📄 `{f_csv}`")
                    path_csv = os.path.join(BD_SAIDA, f_csv)
                    with open(path_csv, "rb") as file_to_dwl:
                        st.download_button(
                            label=f"⬇️ Fazer Download de {f_csv}",
                            data=file_to_dwl,
                            file_name=f_csv,
                            mime="text/csv",
                            key=f"dwl_{f_csv}"
                        )
                    st.markdown("---")
            else:
                st.warning("Nenhum Lote CSV (.csv) na Doca de Saída no momento.")
        except Exception:
            st.warning("Diretório `bd_saida` indisponível no momento.")
