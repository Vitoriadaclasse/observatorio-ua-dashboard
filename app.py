# Importações
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.express as px


# Configurações iniciais
st.set_page_config(page_title="Observatório Científico UA", layout="wide", page_icon="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS1ZOSQg8JAJfqgtVPpSreJArI1a8cFPIFT1Q&s")

# --- ESTILIZAÇÃO CSS ---
st.markdown("""
    <style>
    /* Cores do Sidebar */
    div[data-baseweb="slider"] > div > div > div {
        background-color: #007A53 !important;
    }

    /* TRACK PREENCHIDO */
    div[data-baseweb="slider"] [data-testid="stSlider"] div div div div {
        background-color: #007A53 !important;
    }

    /* Manípulo */
    div[role="slider"] {
        background-color: #007A53 !important;
        border-color: #007A53 !important;
        box-shadow: none !important;
    }

    /* Hover / foco */
    div[role="slider"]:hover,
    div[role="slider"]:active,
    div[role="slider"]:focus {
        box-shadow: 0 0 0 10px rgba(0, 122, 83, 0.2) !important;
    }

    div[data-baseweb="slider"] div {
        color: #007A53 !important;
    }
    /********************************/
            
    /* Container principal da métrica */
    div[data-testid="stMetric"] {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
    }

    /* Legenda (label) */
    div[data-testid="stMetric"] > label {
        width: 100%;
        justify-content: center;
        text-align: center;
    }

    /* Valor numérico */
    div[data-testid="stMetric"] > div {
        justify-content: center;
        text-align: center;
    }

    /* Delta (se existir) */
    div[data-testid="stMetricDelta"] {
        justify-content: center;
        text-align: center;
    }
    
    /* Caixa/pílula da métrica */
    div[data-testid="stMetric"] {
        background-color: rgba(0, 122, 83, 0.06);
        border: 1px solid rgba(0, 122, 83, 0.25);
        border-radius: 15px;
        padding: 10px 5px !important;
        text-align: center;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    /* Hover elegante */
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12);
    }

    /* Legenda */
    div[data-testid="stMetric"] > label {
        font-size: 1rem;
        font-weight: 400;
        color: #004b93;
        justify-content: center;
        margin-bottom: 6px;
    }

    /* Valor */
    div[data-testid="stMetric"] > div {
        font-size: 1.8rem;
        font-weight: 700;
        color: #004b93;
        justify-content: center;
    }

    /* Delta (se existir) */
    div[data-testid="stMetricDelta"] {
        justify-content: center;
        font-size: 0.8rem;
    }
            
    /******************************/
    /* 1. Centraliza a lista de abas */
    div[data-testid="stTabs"] [data-baseweb="tab-list"] {
        display: flex;
        justify-content: center;
        gap: 35px;
        background-color: transparent;
                
        /* Remove explicitamente qualquer borda padrão cinzenta */
        border: none !important; 
        
        /* Cria a linha horizontais superiror    */
        border-top: 2px solid #F0F2F6 !important; 
        
        /* Espaçamento interno para as pílulas ficarem no meio */
        padding: 15px 20px !important; 
        margin-top: 0px;
        margin-bottom: 0px;
    }

    /* 2. Estiliza cada aba como uma "pílula" individual */
    div[data-testid="stTabs"] [data-baseweb="tab"] {
        background-color: #F0F7FF; 
        border: 1px solid #D1E9FF !important;
        border-radius: 12px;
        padding: 20px 30px;
        transition: all 0.2s ease-in-out;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.03);
    }

    /* 3. Efeito de hover */
    div[data-testid="stTabs"] [data-baseweb="tab"]:hover {
        background-color: #E1F5FE;
        border-color: #004b93 !important;
    }

    /* 4. Estilo da aba ATIVA (Selecionada) */
    div[data-testid="stTabs"] [aria-selected="true"] {
        background-color: #004b93 !important; 
        border-color: #004b93 !important;
        transform: translateY(-1px);
        box-shadow: 0px 4px 10px rgba(0,75,147,0.2);
    }
    
    /* 5. Ajuste da cor e peso do texto */
    div[data-testid="stTabs"] [aria-selected="true"] p {
        color: white !important;
        font-weight: 700 !important;
    }
    
    div[data-testid="stTabs"] [aria-selected="false"] p {
        color: #4F5B63 !important;
        font-weight: 500 !important;
    }

    </style>
""", unsafe_allow_html=True)

# --- CARREGAMENTO DE DADOS  ---
@st.cache_data
def load_data():
    articles = pd.read_csv('Fact_Articles.csv', dtype={'Article_ID': str, 'Topic_ID': str})
    topics = pd.read_csv('Dim_Topics.csv', dtype={'Topic_ID': str})
    geo = pd.read_csv('Bridge_Geography.csv', dtype={'Article_ID': str})
    authors = pd.read_csv('Dim_Authors.csv', dtype={'Author_ID': str})
    bridge_authors = pd.read_csv('Bridge_Article_Authors.csv', dtype={'Article_ID': str, 'Author_ID': str})
    timeline = pd.read_csv('Agg_Timeline.csv')
    df_terms = pd.read_csv("top_terms_per_topic.csv", dtype={'Topic_ID': str})

    # NOVOS FICHEIROS GERADOS
    authors = pd.read_csv('Dim_Authors.csv', dtype={'Author_ID': str})
    bridge_authors = pd.read_csv('Bridge_Article_Authors.csv', dtype={'Article_ID': str, 'Author_ID': str})
    timeline = pd.read_csv('Agg_Timeline.csv')
    df_terms = pd.read_csv("top_terms_per_topic.csv", dtype={'Topic_ID': str})

    df_full = articles.merge(topics, on='Topic_ID', how='left')
    return df_full, topics, geo, authors, bridge_authors, timeline, df_terms

# Inicialização dos dados
try:
    df_full, df_topics, df_geo, df_authors, df_bridge_authors, df_timeline, df_terms, = load_data()
except Exception as e:
    st.error(f"Erro ao carregar arquivos CSV: {e}")
    st.stop()

# --- GESTÃO DE NAVEGAÇÃO ---
if 'page' not in st.session_state:
    st.session_state.page = 'cover'

def change_page(name):
    st.session_state.page = name

# CAPA INTRODUTÓRIA
if st.session_state.get("page", "cover") == "cover":

    # Textos
    # Textos formatados para o dicionário
    t = {
        "uni": "Universidade de Aveiro",
        "title": "Observatório da Comunidade Científica",
        "subtitle": "Plataforma de inteligência científica para monitorização de tendências e impacto da comunidade",
        "about_t": "Sobre o Projeto",
        "about_b": (
            "O presente projeto de Observatório tem como objetivo fornecer uma ferramenta de "
            "apoio à análise da produção científica da Universidade de Aveiro. A sua finalidade "
            "principal consiste em mapear a geração e a partilha de conhecimento entre os diferentes "
            "departamentos e áreas de investigação, recorrendo a uma análise bibliométrica baseada em "
            "dados provenientes da base Scopus."
            " A plataforma permite:"
            " acompanhar a evolução das publicações científicas ao longo do tempo;"
            " avaliar o impacto do trabalho dos investigadores através das citações;"
            " identificar os principais meios utilizados para a divulgação dos resultados;"
            " destacar as áreas e temas de maior relevância no contexto atual."
        ),
        "tech_t": "Parte técnica",
        "tech_b": (
            "A plataforma foi construída para analisar de forma detalhada a produção científica da UA, "
            "usando técnicas avançadas de NLP (Processamento de Linguagem Natural) e modelos de "
            "extração de tópicos, como a NMF (Fatorização de Matrizes Não Negativas). Com isto, "
            "conseguimos processar milhares de resumos e títulos para identificar agrupamentos temáticos "
            "que mostram a identidade científica da universidade."
            "Para tornar a análise ainda mais precisa, o sistema utiliza o modelo Llama via Ollama, "
            "que interpreta e rotula automaticamente os tópicos. A interface foi desenvolvida em Python "
            "com Streamlit, utilizando o Plotly para transformar dados bibliométricos complexos "
            "em insights visuais fáceis de entender."
        ),
        "team": "Equipa de Desenvolvimento",
        "btn": "Explorar Dashboard ➔"
    }     

    # CSS
      
    st.markdown("""                                
    <style>

    .header {
        text-align: center;
        margin-top: 0px;
        margin-bottom: 35px;
    }

    .ua-logo {
        max-width: 150px;
        margin-bottom: 10px;
    }

    .ua-name {
        font-size: 2.5rem;
        font-weight: 1200;
        letter-spacing: 4px;
        color: #007A53;
        margin-bottom: 2px;
        text-transform: uppercase;
    }

    .main-title {
        font-size: 3.2rem;
        font-weight: 900;
        margin-bottom: 2px;
        color: #004b93;
    }

    .subtitle {
        font-size: 1.15rem;
        opacity: 0.8;
        margin-bottom: 2px;
    }

    .info-card {
        background: rgba(255,255,255,0.04);
        border-radius: 18px;
        padding: 28px;
        height: 100%;
        box-shadow: inset 0 0 0 1px rgba(255,255,255,0.06);
        text-align: justify;
    }
    .info-card h3 {
        color: #004b93;
        margin-top: 0;
    }
    .team {
        text-align: center;
        margin-top: 0px;
    }
    .gh-container {
        display: flex;
        justify-content: center;
        gap: 30px;
        margin-top: 0px;
    }

    .gh-link {
        color: #004b93;
        font-weight: 400;
        text-decoration: none;
    }

    .gh-link:hover {
        color: #004b93;
        text-shadow: 0 0 8px rgba(79,172,254,0.9);
    }

   div.stButton > button {
        background-color: #004b93; 
        color: white;               
        font-weight: 800;
        border-radius: 30px;
        height: 50px;
        font-size: 1.6rem;
        border: none;
        box-shadow: 0 8px 20px rgba(0, 75, 147, 0.3); 
        transition: all 0.1s ease;
        margin-top: 25px
    }

    div.stButton > button:hover {
        background-color: #004b93; 
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 12px 25px rgba(0, 75, 147, 0.5);
    }
    
    div.stButton > button:active {
        transform: translateY(0px);
    }

    </style>
    """, unsafe_allow_html=True)
           
    # HEADER
    st.markdown(f"""
    <div class="header">
        <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS1ZOSQg8JAJfqgtVPpSreJArI1a8cFPIFT1Q&s" class="ua-logo">
        <div class="ua-name">{t['uni']}</div>
        <div class="main-title">{t['title']}</div>
        <div class="subtitle">{t['subtitle']}</div>
    </div>
    """, unsafe_allow_html=True)

   
    # CARDS
    
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div class="info-card">
            <h3> {t['about_t']}</h3>
            <p>{t['about_b']}</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="info-card">
            <h3> {t['tech_t']}</h3>
            <p>{t['tech_b']}</p>
        </div>
        """, unsafe_allow_html=True)

  
    # TEAM / GITHUB
    
    st.markdown(f"""
    <div class="team">
        <h4>{t['team']}</h4>
        <div class="gh-container">
            <a class="gh-link" href="https://github.com/AnnaPaulaBarros" target="_blank"> Anna Paula Barros da Silva - 129253 </a>
            <a class="gh-link" href="https://github.com/rebeca-gomes-de-freitas" target="_blank"> Rebeca Gomes de Freitas - 130542 </a>
            <a class="gh-link" href="https://github.com/Vitoriadaclasse" target="_blank"> Vitória da Conceição Rodrigues - 130557 </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    
    # BOTÃO
    _, col_btn, _ = st.columns([1, 1, 1])
    with col_btn:
        if st.button(t["btn"], use_container_width=True):
            st.session_state.page = "dashboard"
            st.rerun()

# DASHBOARD 
else:
# --- SIDEBAR INTERATIVO ---
    st.sidebar.image("data:image/png;base64,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", width=200)
    st.sidebar.markdown("<h1 style='color: #007A53;'>Painel de Controle</h1>", unsafe_allow_html=True)    
          
    # Filtro de Tópicos (Influencia o Nuvem e o Card)
    topicos_lista = ["Todos"] + sorted(df_topics['Topic_Label'].unique().tolist())
    topico_selecionado = st.sidebar.selectbox("Focar em um Tópico Específico:", topicos_lista)
    anos = sorted(df_full['Year'].unique())
    ano_range = st.sidebar.select_slider("Período:", options=anos, value=(min(anos), max(anos)))
    df_filtered = df_full[(df_full['Year'] >= ano_range[0]) & (df_full['Year'] <= ano_range[1])]
    if topico_selecionado != "Todos":
        df_filtered = df_filtered[df_filtered['Topic_Label'] == topico_selecionado]
    
    if st.sidebar.button("<-   Voltar para Capa"):
        change_page('cover')
        st.rerun()
    # --- CORPO DO DASHBOARD ---
    st.markdown("<h1 style='text-align: center; color: #007A53;'>Observatório da Comunidade Científica</h1>", unsafe_allow_html=True)    

    # Layout em abas conforme o roteiro
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "DESEMPENHO", "PANORAMA (NLP)", "TÓPICOS EM ALTA", "REDES E COLABORAÇÃO", "PESQUISAR"
    ])

# PAINEL 1: Monitorização de Desempenho (Bibliometria)
    with tab1:
        with st.container(border=True):
            st.markdown("<h2 style='text-align: center; color: #004b93;'>"
                "Painel 1: Métricas de Produtividade e Impacto"
                "</h2>", unsafe_allow_html=True)

        # Espaçamento vertical
        st.markdown("<br>", unsafe_allow_html=True)

        # Métricas com espaçamento refinado
        m1, m2, m3, m4 = st.columns(4, gap="large")

        for m, label, value in [
            (m1, "Publicações", len(df_filtered)),
            (m2, "Nº Citações", int(df_filtered['Cited by'].sum())),
            (m3, "Citação/Artigo", round(df_filtered['Cited by'].mean(), 2)),
            (m4, "Tópicos Ativos", df_filtered['Topic_ID'].nunique())]:
            with m:
                st.metric(label, value)

        st.markdown("<hr>", unsafe_allow_html=True)
        col_a, col_b = st.columns(2)

        with col_a:
            # Evolução Temporal
            evolucao = df_filtered.groupby('Year').size().reset_index(name='Artigos')
            fig_evol = px.bar(
                evolucao,
                x='Year',
                y='Artigos',
                color_discrete_sequence=["#0059B3"]
            )
            fig_evol.update_layout(
                title=dict(
                    text="Produção Anual de artigos",  
                    x=0.5,                              # centraliza título
                    xanchor='center',                  
                    font=dict(color="#717172")
                ),
                xaxis_title=None, 
                yaxis_title="Volume de Artigos",
                height=400,           # mesma altura para alinhamento
                margin=dict(t=50, l=20, r=20, b=20)  # título alinhado no topo
            )
            st.plotly_chart(fig_evol, use_container_width=True)

        with col_b:             
            # Top Journals
            top_journals = df_filtered['Source title'].value_counts().head(10).reset_index()
            top_journals_sorted = top_journals.sort_values(by='count', ascending=False)

            fig_jour = px.bar(
                top_journals_sorted,
                x='count',
                y='Source title',
                orientation='h',
                color_discrete_sequence=["#66C9F7"],
                category_orders={"Source title": top_journals_sorted['Source title'].tolist()}
            )
            fig_jour.update_layout(
                title=dict(
                    text="Principais Canais de Publicação",  
                    x=0.5,                              # centraliza título
                    xanchor='center',                  
                    font=dict(color='#717172')
                ),
                xaxis_title=None, 
                yaxis_title=None,
                height=400,           # mesma altura
                margin=dict(t=50, l=20, r=20, b=20)  # títulos alinhados
            )
            st.plotly_chart(fig_jour, use_container_width=True)

# --- PAINEL 2: PANORAMA (NLP) ---
    with tab2:
        with st.container(border=True):
            st.markdown(f"<h2 style='text-align: center; color: #004b93;'>Painel 2: Análise de Conteúdo</h2>", unsafe_allow_html=True)
                    
        # 2. GRÁFICO DE BARRAS GLOBAL (Ignora o filtro de tópico para possibilitar comparação)
        df_year_only = df_full[(df_full['Year'] >= ano_range[0]) & (df_full['Year'] <= ano_range[1])]
        
        # Calculamos as contagens globais para o gráfico de barras
        topic_counts_global = df_year_only['Topic_Label'].value_counts().reset_index()
        topic_counts_global.columns = ['Topic_Label', 'Quantidade']
        
        fig_bar = px.bar(
            topic_counts_global, 
            x='Quantidade', 
            y='Topic_Label', 
            orientation='h', 
            color='Quantidade', 
            color_continuous_scale='Blues',
            labels= {'Quantidade': 'Nº de artigos'}
        )
        fig_bar.update_layout(yaxis=None, xaxis=None, title=dict(
                    text="Artigos por Área Científica (Tópicos gerados)",  
                    x=0.5,                              
                    xanchor='center',                  
                    font=dict(color='#717172')), height=400)
        st.plotly_chart(fig_bar, use_container_width=True)

        st.divider()

        # 3. LÓGICA DE SELEÇÃO PARA DETALHAMENTO (Nuvem e Card)
        # Se 'Todos' estiver no sidebar, detalhamos o tópico com maior volume no período
        if topico_selecionado == "Todos":
            display_topic = topic_counts_global['Topic_Label'].iloc[0] 
        else:
            display_topic = topico_selecionado

        # Busca informações na tabela Dim_Topics para o tópico a ser exibido
        topic_info = df_topics[df_topics['Topic_Label'] == display_topic].iloc[0]

        # 4. COLUNAS: NUVEM (Esquerda) e CARD IA (Direita)
        col_left, col_right = st.columns([1.2, 1])

        with col_left:
            st.markdown(f"<p style='font-size: 1.2em; color: #717172; font-weight: bold; margin-bottom: 0;'>Identidade Semântica: {display_topic}</p>", unsafe_allow_html=True)
            
            # Recuperar ID do tópico e filtrar termos
            t_id = df_topics[df_topics['Topic_Label'] == display_topic]['Topic_ID'].values[0]
            t_terms = df_terms[df_terms['Topic_ID'] == t_id]
            
            if not t_terms.empty:
                from wordcloud import WordCloud
                import matplotlib.pyplot as plt

                weights_dict = dict(zip(t_terms['term'], t_terms['weight']))
                wordcloud = WordCloud(
                    width=1000, height=600, 
                    background_color='white',
                    colormap='Blues', 
                    max_words=50
                ).generate_from_frequencies(weights_dict)
                
                fig, ax = plt.subplots(figsize=(12, 7))
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.axis('off')
                plt.tight_layout(pad=0)
                st.pyplot(fig)
            else:
                st.warning("Não foram encontrados termos para este tópico.")

        with col_right:
            st.markdown(f"<p style='font-size: 1.2em; color: #717172; font-weight: bold; margin-bottom: 0;'> Resumo do Tópico</p>", unsafe_allow_html=True)
            st.markdown(f"""
                <div style="background-color: #F0F2F6; color: white; padding: 25px; border-radius: 15px; 
                            border-left: 8px solid #004b93; min-height: 380px; box-shadow: 5px 5px 15px rgba(0,0,0,0.3);">
                    <h2 style="color: #004b93; margin-top: 0; font-size: 1.6em;">{display_topic}</h2>
                    <p style="color: #004b93; font-weight: bold; font-size: 0.8em; letter-spacing: 1.2px; margin-bottom: 10px;">
                        INTERPRETAÇÃO OLLAMA / NMF
                    </p>
                    <hr style="border: 0.1px solid #333; margin: 15px 0;">
                    <p style="font-size: 1.05em; line-height: 1.6; color: #4F5B63; text-align: justify;">
                        {topic_info['Description']}
                    </p>
                    <div style="margin-top: 20px;">
                        <span style="background: #004b93; padding: 6px 12px; border-radius: 4px; font-size: 0.8em; font-weight: bold;">
                            TENDÊNCIA: {topic_info['Trend_Status']}
                        </span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        st.divider()

        # --- BLOCO: DISPERÇÃO REVISTAS x TÓPICOS ---
        st.markdown("<h4 style='color: #004b93;'>Relação Revistas x Tópicos (Top 10)</h4>", unsafe_allow_html=True)

        # --- Preparar os dados ---
        # Top 10 revistas
        top_10_journals = df_filtered['Source title'].value_counts().head(10).index.tolist()

        abreviacoes_revistas = {}
        for journal in top_10_journals:
            words = journal.split()
            # Abrevia para até 3 palavras principais
            if len(words) <= 3:
                abreviacoes_revistas[journal] = " ".join(words)
            else:
                abreviacoes_revistas[journal] = " ".join(words[:2]) + "…"
        df_top_journals = df_filtered[df_filtered['Source title'].isin(top_10_journals)]

        # Contagem de artigos por Revista x Tópico
        df_dist = df_top_journals.groupby(['Source title', 'Topic_Label']).size().reset_index(name='Artigos')

        # Top 10 tópicos
        top_10_topics = df_dist.groupby('Topic_Label')['Artigos'].sum().sort_values(ascending=False).head(10).index.tolist()
        df_dist_top = df_dist[df_dist['Topic_Label'].isin(top_10_topics)]

        # Abreviar nomes das revistas
        df_dist_top['Revista_Abrev'] = df_dist_top['Source title'].map(lambda x: abreviacoes_revistas.get(x, x))

        #Legendar Topicos
        top_10_topics = df_dist.groupby('Topic_Label')['Artigos'].sum().sort_values(ascending=False).head(10).index.tolist()
        legenda_topicos = {topic: f"T{i+1}" for i, topic in enumerate(top_10_topics)}

        # Criar coluna com legenda
        df_dist_top['Topico_Legenda'] = df_dist_top['Topic_Label'].map(legenda_topicos)

        # --- Criar gráfico de dispersão ---
        fig_scatter = px.scatter(
            df_dist_top,
            x='Topico_Legenda',
            y='Revista_Abrev',  
            size='Artigos',
            color_discrete_sequence=['#004b93'],  
            hover_data={                           
                'Topico_Legenda': False,
                'Revista_Abrev': False,
                'Artigos': False,
                'Source title': False,
                'Topic_Label': False
            },
            size_max=40
        )

        # Ajustes visuais
        fig_scatter.update_layout(
            xaxis_title=None,
            yaxis_title=None,
            plot_bgcolor='rgba(0,0,0,0)',
            height=700,
            margin=dict(l=80, r=50, t=50, b=150),
            font=dict(size=12)
        )
        fig_scatter.update_traces(
            hovertemplate=
            "REVISTA: %{customdata[0]}<br>" +
            "TÓPICO: %{customdata[1]}<br>" +
            "Nº ARTIGOS: %{customdata[2]}<extra></extra>",
            customdata=df_dist_top[['Source title', 'Topic_Label', 'Artigos']].values
        )

        # Inverter eixo Y para colocar a revista mais publicada no topo
        fig_scatter.update_yaxes(categoryorder='total ascending')

        # Mostrar no Streamlit
        st.plotly_chart(fig_scatter, use_container_width=True)

# --- PAINEL 3: TENDÊNCIAS E CICLO DE VIDA ---
    with tab3:
        with st.container(border=True):
            st.markdown(f"<h2 style='text-align: center; color: #007A53;'>Painel 3: Ciclo de Vida e Maturidade dos Tópicos</h2>", unsafe_allow_html=True)
            
            if df_filtered.empty:
                st.warning("Ajuste os filtros laterais para visualizar a evolução temporal.")
            else:
                # 1. Agregação de dados por Ano e Tópico
                trend_data = df_filtered.groupby(['Year', 'Topic_Label']).size().reset_index(name='Volume')
                
                # 2. Gráfico de Barras Horizontais Empilhadas (Stacked Bar Chart)
                # O eixo Y mostra os tópicos e o X a quantidade. A cor diferencia os anos.
                fig_trend = px.bar(
                    trend_data, 
                    x="Volume", 
                    y="Topic_Label", 
                    color="Year", 
                    orientation='h',
                    color_continuous_scale='Blues', # Tons de azul conforme solicitado
                    title="Distribuição Histórica da Produção por Tópico",
                    labels={'Volume': 'Quantidade de Artigos', 'Topic_Label': 'Área Científica', 'Year': 'Ano'}
                )

                # 3. Aplicação do Princípio de Pouca Tinta (Minimalismo Visual)
                fig_trend.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)', 
                    paper_bgcolor='rgba(0,0,0,0)',
                    xaxis=dict(
                        showgrid=True, 
                        gridcolor='#f0f0f0', 
                        title_font=dict(size=12, color='#4F5B63')
                    ),
                    yaxis=dict(
                        showgrid=False, 
                        categoryorder='total ascending', # Ordena do maior para o menor volume
                        title_font=dict(size=12, color='#4F5B63')
                    ),
                    height=600,
                    margin=dict(l=0, r=0, t=50, b=0),
                    coloraxis_colorbar=dict(
                        title="Ano", 
                        thickness=15,
                        len=0.5
                    )
                )

                st.plotly_chart(fig_trend, use_container_width=True)

            st.divider()

            # 9. Classificação de "Hot Topics" (Tabela com Indicadores)
            st.markdown("#### Classificação de Relevância Estratégica")
            
            # Colunas para organizar a lista de status
            c_hot, c_stable = st.columns(2)
            
            with c_hot:
                st.markdown("<p style='color: #004b93; font-weight: bold;'> ÁREAS EM ALTA (HOT)</p>", unsafe_allow_html=True)
                # Filtragem dos tópicos Hot na dimensão
                hot_list = df_topics[df_topics['Trend_Status'].str.contains('Hot', na=False)]['Topic_Label'].tolist()
                for t in hot_list:
                    st.markdown(f"- {t}")
            
            with c_stable:
                st.markdown("<p style='color: #4F5B63; font-weight: bold;'> ÁREAS CONSOLIDADAS (STABLE)</p>", unsafe_allow_html=True)
                # Filtragem dos tópicos Estáveis
                stable_list = df_topics[df_topics['Trend_Status'].str.contains('Stable', na=False)]['Topic_Label'].tolist()
                for t in stable_list:
                    st.markdown(f"- {t}")

            st.caption("Nota: A segmentação por cores no gráfico acima permite validar visualmente o status de tendência de cada área.")


# --- PAINEL 4: REDES E COLABORAÇÃO  ---
    with tab4:
        with st.container(border=True):
            st.markdown(f"<h2 style='text-align: center; color: #004b93;'>Painel 4: Dimensão Geográfica e Colaboração Internacional</h2>", unsafe_allow_html=True)

        if df_filtered.empty:
            st.warning(" Ajuste os filtros para carregar os dados.")
        else:
            # 1. PROCESSAMENTO DE PAÍSES
            article_ids = df_filtered['Article_ID'].unique()
            geo_filtered = df_geo[df_geo['Article_ID'].isin(article_ids)].copy()

            paises_validos = ['Brazil', 'Portugal', 'Spain', 'Germany', 'United States', 
                            'France', 'Italy', 'United Kingdom', 'China', 'Argentina', 
                            'Chile', 'Colombia', 'Mexico', 'Angola', 'Mozambique']

            map_fix = {'Brasil': 'Brazil', 'Espanha': 'Spain', 'Alemanha': 'Germany', 'Estados Unidos': 'United States'}
            geo_filtered['Country_Region'] = geo_filtered['Country_Region'].replace(map_fix)
            geo_filtered = geo_filtered[geo_filtered['Country_Region'].isin(paises_validos)]

            if geo_filtered.empty:
                st.info("ℹ️ Sem dados geográficos válidos para estes filtros.")
            else:
                geo_counts = geo_filtered['Country_Region'].value_counts().reset_index()
                geo_counts.columns = ['Local', 'Frequência']

                # Novo scatter_geo com cor fixa azul escuro
                fig_map = px.scatter_geo(
                    geo_counts,
                    locations="Local",
                    locationmode="country names",
                    size="Frequência",              # tamanho proporcional à frequência
                    hover_name="Local",
                    color_discrete_sequence=["#004b93"],  # cor fixa azul escuro
                    projection="natural earth",
                    size_max=30                      # opcional: tamanho máximo da bolinha
                )

                fig_map.update_layout(
                    margin=dict(l=0, r=0, t=30, b=0),
                    height=450
                )

                st.plotly_chart(fig_map, use_container_width=True)


        st.divider()

        # 2. RANKING E AUTORES
        col_g1, col_g2 = st.columns([2, 1])
        
        with col_g1:
            st.markdown(f"<h4 style='color: #717172;'>Ranking de Países</h4>", unsafe_allow_html=True)

            if not geo_filtered.empty:
                # Seleciona os 10 países com mais artigos
                top_paises = geo_counts.sort_values('Frequência', ascending=False).head(10)
                # Ordena para que a barra maior fique embaixo
                top_paises = top_paises.sort_values('Frequência', ascending=True)

                # Cria o gráfico de barras com cor fixa azul escuro
                fig_bar = px.bar(
                    top_paises,
                    x='Frequência',
                    y='Local',
                    orientation='h',
                    color_discrete_sequence=["#004b93"]  # azul escuro igual ao mapa
                )

                fig_bar.update_layout(
                    yaxis=None,
                    xaxis=None,
                    margin=dict(l=0, r=0, t=10, b=0)
                )

                st.plotly_chart(fig_bar, use_container_width=True)


        with col_g2:
            st.markdown(f"<h4 style='color: #717172;'>Principais Autores</h4>", unsafe_allow_html=True)
            st.write("")
            st.write("")  
            # Filtramos a ponte com os novos IDs oficiais
            bridge_ids = df_bridge_authors[df_bridge_authors['Article_ID'].isin(article_ids)]
            top_ids = bridge_ids['Author_ID'].value_counts().head(10).reset_index()
            top_ids.columns = ['Author_ID', 'count']
            
            # Unimos com os novos nomes completos vindos do Dim_Authors
            top_names = top_ids.merge(df_authors, on='Author_ID', how='left')
            top_names = top_names.sort_values('Author_Name')

            for _, row in top_names.iterrows():
                # Como o nome no novo CSV já está completo (ex: "Silva, Anna P."), basta exibir!
                st.write(f"👤 {row['Author_Name']}")
            
            st.caption("Dados extraídos diretamente da base ScopusUA.")

# --- PAINEL 5: Explorador de Dados ---
    with tab5:
        st.markdown(f"<h2 style='color: #004b93;'>Pesquisa Avançada de Artigos</h2>", unsafe_allow_html=True)
        st.write("Filtre e localize artigos específicos utilizando a pesquisa textual e os metadados bibliométricos.")
                
        query_text = st.text_input("🔍 Pesquisar por artigo ou autores(as)", "")

        # Para cada artigo, identificamos o primeiro autor na ponte (Author Principal)
        main_auth_df = df_bridge_authors.groupby('Article_ID').first().reset_index()
        main_auth_df = main_auth_df.merge(df_authors, on='Author_ID', how='left')
        
        # Cruzamento final para a tabela do explorador
        explorer_df = df_filtered.merge(main_auth_df[['Article_ID', 'Author_Name']], on='Article_ID', how='left')
        
        if query_text:
            explorer_df = explorer_df[explorer_df['Title'].str.contains(query_text, case=False, na=False)]
            
        # Definição das colunas conforme o roteiro
        display_map = {
            'Title': 'Título',
            'Year': 'Ano',
            'Source title': 'Revista',
            'Topic_Label': 'Tópico (IA)',
            'Author_Name': 'Autor Principal',
            'Cited by': 'Citações',
            'Link': 'Link DOI'
        }
        
        # Seleção e renomeação
        df_display = explorer_df[list(display_map.keys())].rename(columns=display_map)
        
        # Exibição da Tabela Interativa
        st.dataframe(
            df_display,
            column_config={
                "Link DOI": st.column_config.LinkColumn("Link DOI", help="Abrir registo oficial no Scopus/DOI")
            },
            use_container_width=True,
            hide_index=True
        )
        
        st.download_button(
            label="📥 Exportar Lista Filtrada (CSV)",
            data=df_display.to_csv(index=False).encode('utf-8'),
            file_name='explorador_ua_cientifica.csv',
            mime='text/csv'

        )

