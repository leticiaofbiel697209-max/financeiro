import shutil
from datetime import datetime
import streamlit as st
import plotly.express as px
from services.relatorios import fluxo_mensal, por_categoria, get_pagar, get_receber, export_excel, brl
from services.db import DB_PATH

def render():
    st.title('📑 Relatórios e backup')
    fluxo = fluxo_mensal()
    st.subheader('Fluxo de caixa mensal')
    st.dataframe(fluxo, use_container_width=True, hide_index=True)
    if not fluxo.empty:
        st.plotly_chart(px.line(fluxo, x='mes', y='resultado', markers=True, title='Resultado por mês'), use_container_width=True)
    c1,c2 = st.columns(2)
    with c1:
        st.subheader('Despesas por categoria')
        st.dataframe(por_categoria('Saída'), use_container_width=True, hide_index=True)
    with c2:
        st.subheader('Receitas por categoria')
        st.dataframe(por_categoria('Entrada'), use_container_width=True, hide_index=True)
    st.subheader('Vencidos e a receber')
    st.dataframe(get_pagar().query("status == 'Atrasado'") if not get_pagar().empty else get_pagar(), use_container_width=True, hide_index=True)
    st.dataframe(get_receber().query("status in ['Em aberto','Atrasado']") if not get_receber().empty else get_receber(), use_container_width=True, hide_index=True)
    c3,c4 = st.columns(2)
    if c3.button('Gerar relatório Excel', use_container_width=True):
        path = export_excel()
        with open(path, 'rb') as f:
            st.download_button('Baixar relatório Excel', f, file_name='relatorio_financeiro.xlsx', use_container_width=True)
    if c4.button('Gerar backup do banco', use_container_width=True):
        backup = f"backups/financeiro_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        shutil.copy2(DB_PATH, backup)
        with open(backup, 'rb') as f:
            st.download_button('Baixar backup SQLite', f, file_name=backup.split('/')[-1], use_container_width=True)
