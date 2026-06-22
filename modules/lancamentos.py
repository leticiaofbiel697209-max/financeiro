import streamlit as st
from services.importador_planilha import read_file, guess_columns, import_lancamentos


def render():
    st.title('📥 Importar planilha')
    st.caption('Importe Excel ou CSV. O sistema tenta identificar colunas automaticamente, mas você pode corrigir antes de gravar.')
    file = st.file_uploader('Escolha a planilha', type=['xlsx','csv'])
    if not file:
        st.info('Sua planilha original tinha abas como DESPESAS, RECEITAS, DRE, Fluxo de caixa, Balanço, Classificações e Posição. Aqui você pode importar qualquer aba que tenha data, descrição e valor.')
        return
    sheets = read_file(file)
    sheet_name = st.selectbox('Aba para importar', list(sheets.keys()))
    df = sheets[sheet_name].dropna(how='all')
    st.dataframe(df.head(30), use_container_width=True)
    cols = [''] + list(df.columns)
    guesses = guess_columns(df.columns)
    st.subheader('Mapeamento das colunas')
    def idx(target):
        return cols.index(guesses[target]) if target in guesses and guesses[target] in cols else 0
    c1,c2 = st.columns(2)
    mapping = {}
    mapping['data'] = c1.selectbox('Coluna de data *', cols, index=idx('data'))
    mapping['descricao'] = c2.selectbox('Coluna de descrição *', cols, index=idx('descricao'))
    mapping['valor'] = c1.selectbox('Coluna de valor *', cols, index=idx('valor'))
    mapping['tipo'] = c2.selectbox('Coluna de tipo', cols, index=idx('tipo'))
    mapping['categoria'] = c1.selectbox('Coluna de categoria', cols, index=idx('categoria'))
    mapping['status'] = c2.selectbox('Coluna de status', cols, index=idx('status'))
    mapping['forma_pagamento'] = c1.selectbox('Coluna de forma de pagamento', cols, index=idx('forma_pagamento'))
    mapping = {k:v for k,v in mapping.items() if v}
    if st.button('Importar lançamentos', use_container_width=True):
        if not all(k in mapping for k in ['data','descricao','valor']):
            st.error('Data, descrição e valor são obrigatórios.')
        else:
            qtd = import_lancamentos(df, mapping, origem=f'{file.name} / {sheet_name}')
            st.success(f'{qtd} lançamentos importados.')
