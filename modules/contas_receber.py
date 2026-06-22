import streamlit as st
from services.db import fetch_df, execute

def render():
    st.title('📉 Contas a pagar')
    st.caption('Controle vencimentos de fornecedores, despesas fixas e parcelas. O atraso é calculado automaticamente ao abrir o sistema.')
    cats = fetch_df("SELECT nome FROM categorias WHERE tipo IN ('Saída','Ambos') AND ativa=1 ORDER BY nome")['nome'].tolist()
    with st.form('pagar'):
        c1,c2 = st.columns(2)
        venc = c1.date_input('Vencimento *')
        fornecedor = c2.text_input('Fornecedor *')
        desc = st.text_input('Descrição')
        c3,c4 = st.columns(2)
        cat = c3.selectbox('Categoria', cats or ['Outros'])
        valor = c4.number_input('Valor *', min_value=0.0, step=10.0, format='%.2f')
        status = st.selectbox('Status', ['Em aberto','Pago','Atrasado','Cancelado'])
        obs = st.text_area('Observação')
        if st.form_submit_button('Salvar conta a pagar', use_container_width=True):
            if not fornecedor or valor <= 0: st.error('Informe fornecedor e valor.')
            else:
                execute('INSERT INTO contas_pagar(vencimento,fornecedor,descricao,categoria,valor,status,observacao) VALUES (?,?,?,?,?,?,?)', (venc.isoformat(),fornecedor,desc,cat,valor,status,obs))
                st.success('Conta salva.'); st.rerun()
    df = fetch_df('SELECT * FROM contas_pagar ORDER BY vencimento ASC,id DESC')
    st.dataframe(df, use_container_width=True, hide_index=True)
