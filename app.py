import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configurações iniciais
st.set_page_config(page_title="Observatório Científico UA", layout="wide", page_icon="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS1ZOSQg8JAJfqgtVPpSreJArI1a8cFPIFT1Q&s")
# --- ESTILIZAÇÃO CSS (Centralização de Tabs) ---
st.markdown("""
    <style>
    /* Centraliza o contentor das tabs */
    div[data-testid="stTabs"] [data-baseweb="tab-list"] {
        display: flex;
        justify-content: center;
        gap: 20px;
    }

    /* Melhora o aspeto do texto das tabs */
    div[data-testid="stTabs"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1.1em;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# --- CARREGAMENTO DE DADOS ---
@st.cache_data
def load_data():
    articles = pd.read_csv('Fact_Articles.csv')
    topics = pd.read_csv('Dim_Topics.csv')
    geo = pd.read_csv('Bridge_Geography.csv')
    authors = pd.read_csv('Dim_Authors.csv')
    bridge_authors = pd.read_csv('Bridge_Article_Authors.csv')
    timeline = pd.read_csv('Agg_Timeline.csv')
    
    # Merge para facilitar análises de tópicos
    df_full = articles.merge(topics, on='Topic_ID', how='left')
    return df_full, topics, geo, authors, bridge_authors, timeline

# Inicialização dos dados
try:
    df_full, df_topics, df_geo, df_authors, df_bridge_authors, df_timeline = load_data()
except Exception as e:
    st.error(f"Erro ao carregar arquivos CSV: {e}")
    st.stop()

# --- GESTÃO DE NAVEGAÇÃO ---
if 'page' not in st.session_state:
    st.session_state.page = 'cover'

def change_page(name):
    st.session_state.page = name

# ==========================================
# CAPA INTRODUTÓRIA
# ==========================================
if st.session_state.page == 'cover':
    st.markdown("<h1 style='text-align: center; color: #004b93;'>Observatório da Comunidade Científica</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #4F5B63;'>Universidade de Aveiro</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("data:image/png;base64,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", use_container_width=True)
        
        st.markdown("### Sobre o Projeto")
        st.write("""
        Este observatório é o resultado de uma análise bibliométrica e de conteúdo exaustiva realizada ao longo do semestre. 
        O processo envolveu a extração de dados da base Scopus, seguida por uma etapa rigorosa de limpeza e normalização em Python. 
        
        **Destaque Técnico:** Implementamos técnicas de **Processamento de Linguagem Natural (NLP)** para a extração de tópicos latentes, 
        transformando resumos (abstracts) em clusters temáticos compreensíveis. Através de modelos estatísticos e análise de redes, 
        pretendemos mostrar a dinâmica da produção acadêmica, o impacto das publicações e a amplitude geográfica da rede de colaboração 
        da nossa comunidade científica.
        """)
        
        st.info("**Autores:**Vitoria Rodrigues (130557)")
        
        if st.button("Aceder ao Dashboard"):
            change_page('dashboard')
            st.rerun()

# ==========================================
# DASHBOARD PRINCIPAL
# ==========================================
else:
    # --- SIDEBAR INTERATIVO ---
    st.sidebar.image("data:image/png;base64,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", width=200)
    st.sidebar.title("Painel de Controle")
    
    if st.sidebar.button("🔙 Voltar para Capa"):
        change_page('cover')
        st.rerun()
    
    st.sidebar.divider()
    
    # Filtro de Tópicos (Influencia o Nuvem e o Card)
    topicos_lista = ["Todos"] + sorted(df_topics['Topic_Label'].unique().tolist())
    topico_selecionado = st.sidebar.selectbox("Focar em um Tópico Específico:", topicos_lista)
    
    anos = sorted(df_full['Year'].unique())
    ano_range = st.sidebar.select_slider("Período", options=anos, value=(min(anos), max(anos)))
    
    # Aplicação dos Filtros
    df_filtered = df_full[(df_full['Year'] >= ano_range[0]) & (df_full['Year'] <= ano_range[1])]
    if topico_selecionado != "Todos":
        df_filtered = df_filtered[df_filtered['Topic_Label'] == topico_selecionado]
    
    # --- CORPO DO DASHBOARD ---
    st.markdown("<h2 style='text-align: center; color: #004b93;'>Observatório da Comunidade Científica</h2>", unsafe_allow_html=True)
    # st.markdown("color: #004b93; >'Análise da Comunidade Científica'<")    
    st.markdown("---")

    # Layout em abas conforme o roteiro
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "DESEMPENHO", "PANORAMA (NLP)", "TÓPICOS EM ALTA", "REDES E COLABORAÇÃO", "PESQUISAR"
    ])

    # PAINEL 1: Monitorização de Desempenho (Bibliometria)
    with tab1:
        with st.container(border=True):
            st.subheader("Painel 1: Métricas de Produtividade e Impacto")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Total Publicações", len(df_filtered))
            m2.metric("Total Citações", int(df_filtered['Cited by'].sum()))
            m3.metric("Média Citação/Artigo", round(df_filtered['Cited by'].mean(), 2))
            m4.metric("Tópicos Ativos", df_filtered['Topic_ID'].nunique())
    
            col_a, col_b = st.columns(2)
            with col_a:
                # Evolução Temporal
                evolucao = df_filtered.groupby('Year').size().reset_index(name='Artigos')
                fig_evol = px.bar(evolucao, x='Year', y='Artigos', title="Produção Anual de artigos", color_discrete_sequence=['#004b93'])
                st.plotly_chart(fig_evol, use_container_width=True)
            with col_b:
                # Top Journals
                top_journals = df_filtered['Source title'].value_counts().head(10).reset_index()
                fig_jour = px.bar(top_journals, x='count', y='Source title', orientation='h', title="Top 10 Canais de Publicação")
                st.plotly_chart(fig_jour, use_container_width=True)

# --- PAINEL 2: PANORAMA (NLP) ---
    with tab2:
        st.subheader("Painel 2: Inteligência de Conteúdo")
        
        # 1. VERIFICAÇÃO DE SEGURANÇA (Evita o erro de índice)
        if df_filtered.empty:
            st.warning("Nenhum dado encontrado para os filtros selecionados. Por favor, ajuste o período ou os filtros no menu lateral.")
        else:
            st.write("Análise temática baseada em Processamento de Linguagem Natural (NLP) sobre os abstracts.")

            # 2. GRÁFICO DE BARRAS (Melhor prática Tableau para comparação)
            # Em vez de Treemap, usamos barras horizontais ordenadas
            topic_counts = df_filtered['Topic_Label'].value_counts().reset_index()
            topic_counts.columns = ['Topic_Label', 'Quantidade']
            
            fig_bar = px.bar(
                topic_counts, 
                x='Quantidade', 
                y='Topic_Label', 
                orientation='h', 
                title="Volume de Artigos por Área Científica",
                color='Quantidade', 
                color_continuous_scale='Blues',
                labels={'Quantidade': 'Nº de Artigos', 'Topic_Label': 'Tópico'}
            )
            fig_bar.update_layout(yaxis={'categoryorder':'total ascending'}, height=400)
            st.plotly_chart(fig_bar, use_container_width=True)

            st.divider()

            # 3. LÓGICA DE SELEÇÃO PARA O CARD E NUVEM
            # Se 'Todos' estiver no sidebar, detalhamos o tópico com maior volume atual
            if topico_selecionado == "Todos":
                display_topic = topic_counts['Topic_Label'].iloc[0] 
            else:
                display_topic = topico_selecionado

            # Busca informações na tabela Dim_Topics
            topic_info = df_topics[df_topics['Topic_Label'] == display_topic].iloc[0]

            # 4. COLUNAS: NUVEM (Esquerda) e CARD IA (Direita)
            col_left, col_right = st.columns([1.2, 1])

            with col_left:
                st.markdown(f"#### Nuvem Semântica: {display_topic}")
                # Extração de termos da coluna Top_Terms
                terms = [t.strip() for t in str(topic_info['Top_Terms']).split(',')]
                
                # Plotly Scatter para simular Nuvem de Palavras estável
                import random
                random.seed(42) # Mantém a nuvem na mesma posição
                x_pos = [random.uniform(0, 10) for _ in terms]
                y_pos = [random.uniform(0, 10) for _ in terms]
                sizes = [max(12, 45 - (i * 2.8)) for i in range(len(terms))] 
                
                fig_wc = go.Figure()
                fig_wc.add_trace(go.Scatter(
                    x=x_pos, y=y_pos, text=terms, mode='text',
                    textfont={'size': sizes, 'color': '#004b93', 'family': 'Arial Black'}
                ))
                fig_wc.update_layout(
                    xaxis={'visible': False}, yaxis={'visible': False},
                    height=380, margin=dict(l=0, r=0, t=0, b=0),
                    plot_bgcolor='rgba(240,242,246,0.5)'
                )
                st.plotly_chart(fig_wc, use_container_width=True)

            with col_right:
                st.markdown("#### Topic Card (Resumo da IA)")
                # Estilização Card "Netflix"
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
                
    # --- PAINEL 3: TENDÊNCIAS E CICLO DE VIDA ---
# --- PAINEL 3: TENDÊNCIAS E CICLO DE VIDA ---
    with tab3:
        st.subheader("🔥 Ciclo de Vida e Maturidade dos Tópicos")
        
        st.write("""
        Este gráfico de barras horizontais relaciona a produção total com o tempo, seguindo o princípio de **Pouca Tinta**. 
        **Como ler:** O comprimento total da barra indica a produtividade acumulada. As cores segmentam os anos 
        (Azul claro = Passado | Azul escuro = Presente). 
        """)

        if df_filtered.empty:
            st.warning("⚠️ Ajuste os filtros laterais para visualizar a evolução temporal.")
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
        st.markdown("#### 🏆 Classificação de Relevância Estratégica")
        
        # Colunas para organizar a lista de status
        c_hot, c_stable = st.columns(2)
        
        with c_hot:
            st.markdown("<p style='color: #004b93; font-weight: bold;'>🔥 ÁREAS EM ACELERAÇÃO (HOT)</p>", unsafe_allow_html=True)
            # Filtragem dos tópicos Hot na dimensão
            hot_list = df_topics[df_topics['Trend_Status'].str.contains('Hot', na=False)]['Topic_Label'].tolist()
            for t in hot_list:
                st.markdown(f"- {t}")
        
        with c_stable:
            st.markdown("<p style='color: #4F5B63; font-weight: bold;'>➡️ ÁREAS CONSOLIDADAS (STABLE)</p>", unsafe_allow_html=True)
            # Filtragem dos tópicos Estáveis
            stable_list = df_topics[df_topics['Trend_Status'].str.contains('Stable', na=False)]['Topic_Label'].tolist()
            for t in stable_list:
                st.markdown(f"- {t}")

        st.caption("Nota: A segmentação por cores no gráfico acima permite validar visualmente o status de tendência de cada área.")


# --- PAINEL 4: REDES E COLABORAÇÃO ---
    with tab4:
        st.subheader("🌍 Dimensão Geográfica e Colaboração Internacional")
        
        st.write("""
        Esta visualização mapeia a presença global da UA. As bolhas indicam os países mencionados ou 
        afiliados nos artigos analisados, revelando a amplitude das redes de colaboração e os focos geográficos de estudo.
        """)

        # 10. Mapa de Colaboração Global (Mapa Mundi)
        if df_filtered.empty:
            st.warning(" Ajuste os filtros laterais para visualizar o mapa de colaboração.")
        else:
            # Filtragem da ponte de geografia com base nos artigos atualmente filtrados
            article_ids = df_filtered['Article_ID'].unique()
            geo_filtered = df_geo[df_geo['Article_ID'].isin(article_ids)].copy()

            if geo_filtered.empty:
                st.info("ℹ️ Não foram encontradas localizações para os filtros selecionados.")
            else:
                # Agregação por País/Região
                geo_counts = geo_filtered['Country_Region'].value_counts().reset_index()
                geo_counts.columns = ['Local', 'Frequência']
                
                # Criar o Mapa de Bolhas (Scatter Geo)
                # Plotly reconhece automaticamente nomes de países em inglês/português padrão
                fig_map = px.scatter_geo(
                    geo_counts,
                    locations="Local",
                    locationmode="country names",
                    size="Frequência",
                    hover_name="Local",
                    color="Frequência",
                    color_continuous_scale="Blues",
                    title="Intensidade de Colaboração e Estudo por Região",
                    projection="natural earth", # Projeção moderna e equilibrada
                    labels={'Frequência': 'Menções/Artigos'}
                )

                # Aplicação de Design Minimalista
                fig_map.update_geos(
                    showcountries=True, 
                    countrycolor="#d1d1d1",
                    showcoastlines=True, 
                    coastlinecolor="#d1d1d1",
                    showland=True, 
                    landcolor="#f9f9f9",
                    showocean=True, 
                    oceancolor="#ffffff" # Fundo limpo para pouca tinta
                )

                fig_map.update_layout(
                    margin=dict(l=0, r=0, t=50, b=0),
                    height=600,
                    coloraxis_colorbar=dict(title="Volume", thickness=15)
                )

                st.plotly_chart(fig_map, use_container_width=True)
                
                st.info("💡 **Insight:** O tamanho das bolhas reflete a centralidade da região na produção científica da UA.")

        st.divider()

        # 11. Detalhes de Colaboração (Top 10 Países)
        st.markdown("#### Top 10 Países Parceiros")
        
        if not df_filtered.empty and not geo_filtered.empty:
            col_g1, col_g2 = st.columns([2, 1])
            
            with col_g1:
                # Ranking de Países
                top_geo = geo_counts.head(10)
                fig_geo_bar = px.bar(
                    top_geo, 
                    x='Frequência', 
                    y='Local', 
                    orientation='h',
                    color='Frequência',
                    color_continuous_scale='Blues',
                    labels={'Local': '', 'Frequência': 'Nº de Artigos'}
                )
                fig_geo_bar.update_layout(
                    yaxis={'categoryorder':'total ascending'},
                    plot_bgcolor='rgba(0,0,0,0)',
                    showlegend=False,
                    coloraxis_showscale=False
                )
                st.plotly_chart(fig_geo_bar, use_container_width=True)

            with col_g2:
                # Lista de Autores Hub (Identificados no roteiro)
                st.markdown("**Centralidade de Autoria**")
                # Pegamos a ponte de autores para os artigos filtrados
                bridge_filt = df_bridge_authors[df_bridge_authors['Article_ID'].isin(article_ids)]
                top_auth_ids = bridge_filt['Author_ID'].value_counts().head(5).reset_index()
                top_auth_names = top_auth_ids.merge(df_authors, on='Author_ID')
                
                for _, row in top_auth_names.iterrows():
                    st.write(f"👤 **{row['Author_Name']}** ({row['count']} art.)")
                
                st.caption("Autores com maior rede de conexão interna na amostra.")

    # PAINEL 5: Explorador de Dados
    with tab5:
        st.subheader("Pesquisa Avançada de Artigos")
        st.write("Filtre e localize artigos específicos utilizando a pesquisa textual e os metadados bibliométricos.")
        
        # Slicer de pesquisa local (por texto no título)
        query_text = st.text_input("🔍 Pesquisar por palavras-chave no título do artigo", "")
        
        # Preparação dos dados: Autor Principal
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
