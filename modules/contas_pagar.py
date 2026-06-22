import streamlit as st
from services.db import fetch_df, execute

def render():
    st.title('🏷️ Categorias e formas')
    st.caption('Cadastre categorias para padronizar relatórios. Evite criar nomes duplicados para a mesma coisa.')
    with st.form('cat'):
        c1,c2 = st.columns(2)
        nome = c1.text_input('Nova categoria')
        tipo = c2.selectbox('Tipo', ['Entrada','Saída','Ambos'])
        if st.form_submit_button('Adicionar categoria', use_container_width=True):
            if nome:
                try:
                    execute('INSERT INTO categorias(nome,tipo) VALUES (?,?)', (nome.strip(), tipo))
                    st.success('Categoria adicionada.'); st.rerun()
                except Exception as e: st.error('Essa categoria já existe ou está inválida.')
    with st.form('forma'):
        fp = st.text_input('Nova forma de pagamento')
        if st.form_submit_button('Adicionar forma de pagamento', use_container_width=True):
            if fp:
                try:
                    execute('INSERT INTO formas_pagamento(nome) VALUES (?)', (fp.strip(),))
                    st.success('Forma adicionada.'); st.rerun()
                except Exception: st.error('Essa forma já existe.')
    c1,c2 = st.columns(2)
    c1.dataframe(fetch_df('SELECT * FROM categorias ORDER BY tipo,nome'), use_container_width=True, hide_index=True)
    c2.dataframe(fetch_df('SELECT * FROM formas_pagamento ORDER BY nome'), use_container_width=True, hide_index=True)
