import time
import hashlib
import streamlit as st
from typing import Dict, Any

from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_analysis(
    nome: str,
    arcanos: Dict[str, Any],
    contexto: str,
    api_key: str,
    use_cache: bool = True
) -> str:
    """
    Gera análise usando LangChain + Groq LLaMA 3.
    - Sem fallback
    - Gratuito (Groq) e deployável no Streamlit Cloud
    - Cache opcional
    """

    logger.info(f"🔍 Iniciando análise para: {nome}")

    # -------------------------
    # Validar chave obrigatória
    # -------------------------
    if not api_key or api_key.strip() == "":
        raise ValueError("❌ Nenhuma API key informada. Não é possível gerar análise.")

    # -------------------------
    # Cache
    # -------------------------
    cache_key = hashlib.md5(f"{nome}{contexto}".encode()).hexdigest()

    if use_cache and "analysis_cache" in st.session_state:
        if cache_key in st.session_state.analysis_cache:
            logger.info("📦 Resultado carregado do cache")
            return st.session_state.analysis_cache[cache_key]

    # -------------------------
    # Modelo Groq LLaMA
    # -------------------------
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        groq_api_key=api_key,
        temperature=0.7,
        max_tokens=2000,
        timeout=60
    )

    # -------------------------
    # Template
    # -------------------------
    prompt_template = PromptTemplate(
        input_variables=[
            "nome", "contexto",
            "personalidade_arcano", "personalidade_numero",
            "alma_arcano", "alma_numero",
            "fator_arcano", "fator_numero",
            "energia_ano_arcano", "energia_ano_numero",
            "energia_nome", "energia_nome_numero"
        ],
        template="""
Você é um especialista em Numerologia e Tarô. Gere uma análise baseada nos dados abaixo. Tudo de forma descritiva, sem abordar a pessoa como "você":


Pessoa: {nome}
Contexto: {contexto}

Arcanos:
- Personalidade: {personalidade_arcano} (nº {personalidade_numero})
- Alma: {alma_arcano} (nº {alma_numero})
- Fator Oculto: {fator_arcano} (nº {fator_numero})
- Energia do Ano: {energia_ano_arcano} (nº {energia_ano_numero})
- Energia do Nome: {energia_nome} (nº {energia_nome_numero})

Estrutura da análise:
Trazer o Nome da pessoa e tambem todos os arcanos retirados.

1. **Interpretação Integrada dos Arcanos**
- Relação com o contexto atual

2. **Desafios e Oportunidades**
- Saúde
- Carreira
- Relacionamentos (Amorosos, Familiares, Sociais)
- Espiritualidade

3. **Recomendações Práticas**
- Saúde
- Carreira
- Relacionamentos (Amorosos, Familiares, Sociais)
- Espiritualidade

4. **Perspectivas Futuras**

5. **Resumo Final**
Tonalidade: profissional, acolhedora e construtiva.
"""
    )

    chain = prompt_template | llm | StrOutputParser()

    # -------------------------
    # Contador de requisições
    # -------------------------
    st.session_state.api_request_count = st.session_state.get("api_request_count", 0) + 1
    logger.info(f"📊 Total de requisições: {st.session_state.api_request_count}")

    # -------------------------
    # Execução
    # -------------------------
    try:
        analysis = chain.invoke({
            "nome": nome,
            "contexto": contexto,
            "personalidade_arcano": arcanos.get('personalidade', {}).get('arcano', 'N/A'),
            "personalidade_numero": arcanos.get('personalidade', {}).get('numero', 'N/A'),
            "alma_arcano": arcanos.get('alma', {}).get('arcano', 'N/A'),
            "alma_numero": arcanos.get('alma', {}).get('numero', 'N/A'),
            "fator_arcano": arcanos.get('fator_oculto', {}).get('arcano', 'N/A'),
            "fator_numero": arcanos.get('fator_oculto', {}).get('numero', 'N/A'),
            "energia_ano_arcano": arcanos.get('energia_ano', {}).get('arcano', 'N/A'),
            "energia_ano_numero": arcanos.get('energia_ano', {}).get('numero', 'N/A'),
            "energia_nome": arcanos.get('energia_nome', {}).get('nome_energia', 'N/A'),
            "energia_nome_numero": arcanos.get('energia_nome', {}).get('numero', 'N/A'),
        })

        logger.info("✅ Análise recebida com sucesso")

        # Salvar cache
        st.session_state.setdefault("analysis_cache", {})
        st.session_state.analysis_cache[cache_key] = analysis

        return analysis

    except Exception as e:
        logger.error(f"❌ Erro na API: {e}")
        raise RuntimeError(f"Erro ao gerar análise via Groq LLaMA: {e}")
