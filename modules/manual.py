import streamlit as st
from services.db import fetch_df, execute
from services.relatorios import brl


def render():
    st.title('🧾 Lançamentos')
    st.caption('Preencha apenas os campos do formulário. Saldo, total de entradas e total de saídas são calculados automaticamente.')
    cats = fetch_df("SELECT nome FROM categorias WHERE ativa=1 ORDER BY nome")['nome'].tolist()
    formas = fetch_df("SELECT nome FROM formas_pagamento WHERE ativa=1 ORDER BY nome")['nome'].tolist()
    with st.form('form_lanc'):
        c1,c2 = st.columns(2)
        data = c1.date_input('Data *', help='Data da entrada ou saída.')
        tipo = c2.selectbox('Tipo *', ['Entrada','Saída'], help='Entrada aumenta o caixa. Saída reduz o caixa.')
        descricao = st.text_input('Descrição *', help='Exemplo: Venda cliente X, aluguel, fornecedor de toner.')
        c3,c4 = st.columns(2)
        categoria = c3.selectbox('Categoria', cats or ['Outros'])
        valor = c4.number_input('Valor *', min_value=0.0, step=10.0, format='%.2f')
        c5,c6 = st.columns(2)
        forma = c5.selectbox('Forma de pagamento', formas or ['Outro'])
        status = c6.selectbox('Status', ['Pago','Em aberto','Atrasado','Cancelado'])
        obs = st.text_area('Observação')
        if st.form_submit_button('Salvar lançamento', use_container_width=True):
            if not descricao or valor <= 0:
                st.error('Informe descrição e valor maior que zero.')
            else:
                execute("""INSERT INTO lancamentos(data, descricao, tipo, categoria, valor, forma_pagamento, status, observacao)
                         VALUES (?,?,?,?,?,?,?,?)""", (data.isoformat(), descricao, tipo, categoria, valor, forma, status, obs))
                st.success('Lançamento salvo.')
                st.rerun()
    st.subheader('Últimos lançamentos')
    df = fetch_df('SELECT id,data,descricao,tipo,categoria,valor,forma_pagamento,status,observacao FROM lancamentos ORDER BY data DESC,id DESC')
    if df.empty:
        st.info('Nenhum lançamento cadastrado.')
    else:
        st.dataframe(df, use_container_width=True, hide_index=True)
        with st.expander('Editar ou excluir lançamento'):
            ids = df['id'].tolist()
            sel = st.selectbox('Selecione o ID', ids)
            row = df[df['id']==sel].iloc[0]
            novo_status = st.selectbox('Novo status', ['Pago','Em aberto','Atrasado','Cancelado'], index=['Pago','Em aberto','Atrasado','Cancelado'].index(row['status']))
            nova_obs = st.text_area('Nova observação', value=row.get('observacao') or '')
            c1,c2 = st.columns(2)
            if c1.button('Atualizar', use_container_width=True):
                execute('UPDATE lancamentos SET status=?, observacao=?, atualizado_em=CURRENT_TIMESTAMP WHERE id=?', (novo_status,nova_obs,int(sel)))
                st.success('Atualizado.'); st.rerun()
            if c2.button('Excluir', use_container_width=True):
                execute('DELETE FROM lancamentos WHERE id=?', (int(sel),))
                st.warning('Excluído.'); st.rerun()
