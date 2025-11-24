import pandas as pd
import streamlit as st
from app.numerologia_personalidade import calcula_personalidade, calcula_alma, calcula_fator_oculto, calcula_energia_ano
from app.depara import get_arcano_by_number
from app.numerologia_nome import calcula_energia_nome
from app.gera_insight_gpt import generate_analysis
from datetime import date
import io

st.title("PROJETO CARTAS KATYA") 
tab_dados, tab_pers, tab_ano, tab_nome, tab_gpt = st.tabs(["Dados","Personalidade/Alma/Fator Oculto", "Energia do Ano", "Energia do Nome","Considerações do GPT"])

with tab_dados:
    st.header("Dados do Usuário 👤")
    nome = st.text_input("Nome Completo do(a) Consulente:")
    data_nascimento = st.date_input("Digite sua data de nascimento:",format="DD/MM/YYYY", min_value=date(1925, 1, 1), max_value=date.today(), value=None)
    contexto_pessoa = st.text_area("Descreva brevemente o contexto atual da vida da pessoa:")
    if st.button("Enviar Dados"):
        st.success(f"Dados recebidos")
        
    st.session_state['nome'] = nome
    st.session_state['data_nascimento'] = data_nascimento
    st.session_state['contexto_pessoa'] = contexto_pessoa
    
with tab_pers:
    st.header("Personalidade, Alma e Fator Oculto 🃏")
    if st.button("Gerar Análise de Personalidade/Alma/Fator Oculto"):
        if 'data_nascimento' not in st.session_state or not st.session_state['data_nascimento']:
            st.error("Por favor, insira sua data de nascimento na aba 'Dados' antes de gerar a análise.")
        else:
            data_nascimento = st.session_state['data_nascimento']
            raw_pers, red_pers = calcula_personalidade(data_nascimento)
            raw_alma, red_alma, final_alma = calcula_alma(data_nascimento)
            raw_fator, red_fator = calcula_fator_oculto(data_nascimento)

            st.subheader("Número da Personalidade 🎭")
            st.write(f"Soma bruta (dia + mês + ano): {raw_pers}")
            st.write(f"Número reduzido da Personalidade: {red_pers}")
            arc_pers = get_arcano_by_number(red_pers)
            if arc_pers:
                st.write(f"Arcano: **{arc_pers.get('arcano','-')}** {arc_pers.get('numero_romano','')}")
            st.divider()
            
            st.subheader("Número da Alma ✨")
            st.write(f"Soma bruta (dia + mês + ano): {raw_alma}")
            st.write(f"Número reduzido da Alma: {red_alma}")
            st.write(f"Número final da Alma (dígito único): {final_alma}")
            arc_alma = get_arcano_by_number(final_alma)
            if arc_alma:
                st.write(f"Arcano: **{arc_alma.get('arcano','-')}** {arc_alma.get('numero_romano','')}")
            st.divider()
            
            st.subheader("Fator Oculto 👁️")
            st.write(f"Soma bruta dos dígitos da data: {raw_fator}")
            st.write(f"Número reduzido do Fator Oculto: {red_fator}")
            arc_fator = get_arcano_by_number(red_fator)
            if arc_fator:
                st.write(f"Arcano: **{arc_fator.get('arcano','-')}** {arc_fator.get('numero_romano','')}")
        
            st.success("Análise gerada com sucesso!")
            
            st.session_state['arc_pers'] = arc_pers
            st.session_state['arc_alma'] = arc_alma
            st.session_state['arc_fator'] = arc_fator
    else:
        st.info("Clique no botão acima para gerar a análise de Personalidade, Alma e Fator Oculto.")
    
with tab_ano:
    st.header("Energia do Ano 🔮")

    ano = st.number_input("Insira o Ano (YYYY)", value=None, placeholder="Insira o Ano que deseja consultar a Energia", step=1)
    if st.button("Gerar Análise da Energia do Ano"):
        if 'data_nascimento' not in st.session_state or not st.session_state['data_nascimento']:
            st.error("Por favor, insira sua data de nascimento na aba 'Dados' antes de gerar a análise.")
        else:
            data_nascimento = st.session_state['data_nascimento']
            ano = int(ano)
            raw_energia, red_energia = calcula_energia_ano(data_nascimento.day, data_nascimento.month, ano)
            
            st.subheader(f"Energia do Ano de {ano} 🔮")
            st.write(f"Soma bruta dos dígitos (ddmmaaaa): {raw_energia}")
            st.write(f"Número reduzido da Energia do Ano: {red_energia}")
            arc_energia_ano = get_arcano_by_number(red_energia)
            if arc_energia_ano:
                st.write(f"Arcano: **{arc_energia_ano.get('arcano','-')}** {arc_energia_ano.get('numero_romano','')}")
                
            st.success("Análise da Energia do Ano gerada com sucesso!")
            st.session_state['arc_energia_ano'] = arc_energia_ano
    else:
        st.info("Clique no botão acima para gerar a análise da Energia do Ano.")
    
    
with tab_nome:
    st.header("Energia do Nome 📝")
    if st.button("Gerar Análise da Energia do Nome"):
        if 'nome' not in st.session_state or not st.session_state['nome']:
            st.error("Por favor, insira sua o nome na aba 'Dados' antes de gerar a análise.")
        else:
            raw_nome, red_nome = calcula_energia_nome(nome)
            
            st.write(f"Soma bruta das letras do nome: {raw_nome}")
            st.write(f"Número reduzido da Energia do Nome: {red_nome}")
            arc_energia_nome = get_arcano_by_number(red_nome)
            if arc_energia_nome:
                st.write(f"Arcano: **{arc_energia_nome.get('arcano','-')}** {arc_energia_nome.get('numero_romano','')}")
            st.success("Análise da Energia do Nome gerada com sucesso!")
            st.session_state['arc_energia_nome'] = arc_energia_nome
    else:
        st.info("Clique no botão acima para gerar a análise da Energia do Nome.")

# ...existing code...
with tab_gpt:
    st.header("Considerações do GPT 🤖 (via Groq LLaMA)")

    # ------------------------------------------------------------------
    # Métricas
    # ------------------------------------------------------------------
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Requisições API",
            st.session_state.get("api_request_count", 0),
            help="Quantidade de requisições feitas à API Groq"
        )

    with col2:
        st.metric(
            "Análises em Cache",
            len(st.session_state.get("analysis_cache", {})),
            help="Resultados reaproveitados sem nova requisição"
        )

    # ------------------------------------------------------------------
    # Entrada da API Key Groq
    # ------------------------------------------------------------------
    with st.expander("🔑 Configurar Chave Groq"):
        groq_api_key = st.text_input(
            "Cole sua chave Groq (começa com 'gsk_'):",
            type="password",
            key="groq_key_input",
            placeholder="Digite sua chave Groq aqui"
        )

    # ------------------------------------------------------------------
    # Controle de estado
    # ------------------------------------------------------------------
    st.session_state.setdefault("gpt_request_made", False)

    # ------------------------------------------------------------------
    # Funções auxiliares
    # ------------------------------------------------------------------
    def campos_ok():
        if not st.session_state.get("nome"):
            st.error("❌ Informe o nome na aba 'Dados'.")
            return False
        if not st.session_state.get("data_nascimento"):
            st.error("❌ Informe a data de nascimento na aba 'Dados'.")
            return False
        if not groq_api_key:
            st.error("❌ Cole sua chave Groq para continuar.")
            return False
        return True

    def montar_arcanos():
        return {
            "personalidade": st.session_state.get("arc_pers", {}),
            "alma": st.session_state.get("arc_alma", {}),
            "fator_oculto": st.session_state.get("arc_fator", {}),
            "energia_ano": st.session_state.get("arc_energia_ano", {}),
            "energia_nome": st.session_state.get("arc_energia_nome", {}),
            "contexto": st.session_state.get("contexto_pessoa", "")
        }

    # ------------------------------------------------------------------
    # Botões
    # ------------------------------------------------------------------
    col_gen, col_clear = st.columns(2)

    with col_gen:
        if st.button("🚀 Gerar Análise com LLaMA 3 (Groq)", use_container_width=True):

            if not campos_ok():
                st.stop()

            if st.session_state.gpt_request_made:
                st.warning("⚠️ A análise já foi gerada. Clique em 'Limpar' para gerar outra.")
                st.stop()

            nome = st.session_state["nome"]
            contexto = st.session_state.get("contexto_pessoa", "")
            arcanos = montar_arcanos()

            from app.gera_insight_gpt import generate_analysis

            with st.spinner("⏳ Gerando análise com LLaMA 3..."):
                try:
                    analise = generate_analysis(
                        nome,
                        arcanos,
                        contexto,
                        groq_api_key,
                        use_cache=True
                    )
                except Exception as e:
                    st.error(f"Erro ao gerar análise: {e}")
                    st.stop()

                # Salva, mas NÃO imprime aqui
                st.session_state.gpt_request_made = True
                st.session_state.gpt_analysis = analise

                st.success("✅ Análise gerada com sucesso!")

    with col_clear:
        if st.button("🔄 Limpar", use_container_width=True):
            st.session_state.gpt_request_made = False
            st.session_state.pop("gpt_analysis", None)
            st.rerun()

 # ------------------------------------------------------------------
    # Renderização ÚNICA da análise
    # ------------------------------------------------------------------
    if st.session_state.gpt_request_made:
        st.divider()
        analise_text = st.session_state.get("gpt_analysis", "")
        st.markdown(analise_text)
        
        # Botão de exportar apenas para TXT (conteúdo gerado pela IA)
        nome_consult = st.session_state.get("nome", "analise")
        txt_bytes = analise_text.encode("utf-8", errors="replace")
        st.download_button(
            label="📥 Baixar análise (TXT)",
            data=txt_bytes,
            file_name=f"{nome_consult.replace(' ', '_')}_analise.txt",
            mime="text/plain"
        )