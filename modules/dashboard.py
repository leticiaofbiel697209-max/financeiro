import streamlit as st
from services.db import fetch_df, execute

def render():
    st.title('📈 Contas a receber')
    st.caption('Controle clientes, vencimentos e inadimplência. Valores atrasados aparecem no Dashboard.')
    cats = fetch_df("SELECT nome FROM categorias WHERE tipo IN ('Entrada','Ambos') AND ativa=1 ORDER BY nome")['nome'].tolist()
    with st.form('receber'):
        c1,c2 = st.columns(2)
        venc = c1.date_input('Vencimento *')
        cliente = c2.text_input('Cliente *')
        desc = st.text_input('Descrição')
        c3,c4 = st.columns(2)
        cat = c3.selectbox('Categoria', cats or ['Outros'])
        valor = c4.number_input('Valor *', min_value=0.0, step=10.0, format='%.2f')
        status = st.selectbox('Status', ['Em aberto','Recebido','Atrasado','Cancelado'])
        obs = st.text_area('Observação')
        if st.form_submit_button('Salvar conta a receber', use_container_width=True):
            if not cliente or valor <= 0: st.error('Informe cliente e valor.')
            else:
                execute('INSERT INTO contas_receber(vencimento,cliente,descricao,categoria,valor,status,observacao) VALUES (?,?,?,?,?,?,?)', (venc.isoformat(),cliente,desc,cat,valor,status,obs))
                st.success('Conta salva.'); st.rerun()
    df = fetch_df('SELECT * FROM contas_receber ORDER BY vencimento ASC,id DESC')
    st.dataframe(df, use_container_width=True, hide_index=True)
