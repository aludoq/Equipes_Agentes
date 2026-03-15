import streamlit as st
import os
import re
import pandas as pd

# Caminhos Base do Equipes_agentes (Um nível acima da pasta app_python)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BD_ENTRADA = os.path.join(BASE_DIR, 'bd_entrada')
BD_SAIDA = os.path.join(BASE_DIR, 'bd_saida')

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
    h1, h2, h3 { color: #89b4fa !important; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; background: linear-gradient(135deg, #89b4fa, #3B82F6); color: white; border: none;}
    .report-card { background: #1a1a24; padding: 20px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.05); margin-bottom: 20px; }
    .metric-card { background: #11111b; padding: 15px; border-radius: 8px; border-left: 5px solid #89b4fa; }
    </style>
""", unsafe_allow_html=True)

# Menu Lateral (Sidebar) de Navegação
st.sidebar.title("🛒 Varejo Insight")
st.sidebar.caption("Squad AI de Alta Performance")
st.sidebar.markdown("---")
page = st.sidebar.radio("Comando da Squad", [
    "📥 1. Intake de Dados (Entradas)", 
    "📊 2. Mesa da Diretoria (Resultados)"
])
st.sidebar.markdown("---")

# ----------------------------------------------------------------------------------
# TELA 1: INTAKE DE DADOS
# ----------------------------------------------------------------------------------
if page == "📥 1. Intake de Dados (Entradas)":
    st.header("📥 Gestão de Bases de Operação")
    st.write("Insira seus Arquivos CSV (separador `;` e codificação `UTF-8`) para alimentar a pasta `bd_entrada` da equipe.")
    
    uploaded_files = st.file_uploader(
        "Arraste as planilhas do seu ERP: Estoque Filial, Vendas Históricas e Estoque CD (.csv)", 
        type="csv", 
        accept_multiple_files=True
    )
    
    if uploaded_files:
        if st.button("Salvar Bases na Pasta bd_entrada"):
            for f in uploaded_files:
                file_path = os.path.join(BD_ENTRADA, f.name)
                with open(file_path, "wb") as disk_file:
                    disk_file.write(f.getbuffer())
            st.success(f"Sucesso! {len(uploaded_files)} bases gravadas com sucesso!")
    
    st.subheader("📚 Arquivos Atuais na Doca (bd_entrada)")
    try:
        if not os.path.exists(BD_ENTRADA):
            os.makedirs(BD_ENTRADA)
            
        arquivos = [f for f in os.listdir(BD_ENTRADA) if f.endswith('.csv')]
        if not arquivos:
            st.info("A pasta bd_entrada está limpa. Nenhum fornecimento agendado.")
        else:
            for f in arquivos:
                st.markdown(f"- 📄 `{f}`")
    except Exception as e:
        st.error(f"Erro ao acessar bd_entrada: {e}")


# ----------------------------------------------------------------------------------
# TELA 2: MESA DA DIRETORIA (Resultados)
# ----------------------------------------------------------------------------------
elif page == "📊 2. Mesa da Diretoria (Resultados)":
    st.header("📊 Mesa da Diretoria - Apuração de Resultados")
    st.write("Acompanhe o Sumário Executivo aprovado da Squad e baixe as bases processadas para o seu ERP.")
    
    # --- SEÇÃO DE INDICADORES (APURAR RESULTADOS) ---
    st.subheader("📈 Indicadores Operacionais")
    try:
        csv_files = [f for f in os.listdir(BD_SAIDA) if f.endswith('.csv')]
        if csv_files:
            cols = st.columns(len(csv_files) if len(csv_files) <= 3 else 3)
            for idx, f_csv in enumerate(csv_files):
                path_csv = os.path.join(BD_SAIDA, f_csv)
                df = pd.read_csv(path_csv, sep=';', encoding='utf-8')
                
                with cols[idx % 3]:
                    st.markdown(f"<div class='metric-card'>", unsafe_allow_html=True)
                    st.markdown(f"**Arquivo:** `{f_csv}`")
                    st.markdown(f"**Itens Sugeridos:** {len(df)}")
                    if 'Sugestão' in df.columns:
                        st.markdown(f"**Volume Total:** {int(df['Sugestão'].sum())}")
                    elif 'Sugestão (Caixas)' in df.columns:
                        st.markdown(f"**Cx Totais:** {int(df['Sugestão (Caixas)'].sum())}")
                    st.markdown("</div>", unsafe_allow_html=True)
                    st.write("")
        else:
            st.info("Aguardando processamento de dados para gerar indicadores.")
    except Exception as e:
        st.warning(f"Não foi possível apurar resultados detalhados: {e}")

    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📝 Relatório Estratégico (Markdown)")
        try:
            if not os.path.exists(BD_SAIDA):
                os.makedirs(BD_SAIDA)
                
            arquivos_saida = [f for f in os.listdir(BD_SAIDA) if f.endswith('.md')]
            if arquivos_saida:
                # Pega o mais recente por nome/data se houver prefixo numérico
                ultimo_md = sorted(arquivos_saida)[-1]
                path_md = os.path.join(BD_SAIDA, ultimo_md)
                with open(path_md, "r", encoding="utf-8") as f_md:
                    st.markdown(f"<div class='report-card'>", unsafe_allow_html=True)
                    st.markdown(f"**Checkpoint Atual:** `{ultimo_md}`")
                    st.write("---")
                    st.markdown(f_md.read())
                    st.markdown(f"</div>", unsafe_allow_html=True)
            else:
                st.info("Nenhum Resumo `.md` encontrado. O pipeline foi executado?")
        except Exception as e:
             st.error(f"Erro ao ler relatórios: {e}")

    with col2:
        st.subheader("💾 Carga para o ERP (Download)")
        st.write("Baixe os arquivos CSV preparados para injeção no sistema raiz.")
        
        try:
            arquivos_csv = [f for f in os.listdir(BD_SAIDA) if f.endswith('.csv')]
            if arquivos_csv:
                for f_csv in arquivos_csv:
                    st.markdown(f"### 📄 `{f_csv}`")
                    path_csv = os.path.join(BD_SAIDA, f_csv)
                    with open(path_csv, "rb") as file_to_dwl:
                        st.download_button(
                            label=f"⬇️ Baixar {f_csv}",
                            data=file_to_dwl,
                            file_name=f_csv,
                            mime="text/csv",
                            key=f"dwl_{f_csv}"
                        )
                    st.markdown("---")
            else:
                st.warning("Nenhum Lote CSV na Doca de Saída.")
        except Exception as e:
            st.error(f"Erro ao carregar lista de downloads: {e}")
