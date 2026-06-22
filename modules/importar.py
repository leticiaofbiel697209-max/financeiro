import streamlit as st
import plotly.express as px
from services.relatorios import indicadores, brl, fluxo_mensal, por_categoria


def card(label, value, help_text=''):
    st.markdown(f"""
    <div class='kpi-card'>
      <div class='kpi-label'>{label}</div>
      <div class='kpi-value'>{value}</div>
      <div class='kpi-help'>{help_text}</div>
    </div>
    """, unsafe_allow_html=True)


def render():
    st.title('📊 Dashboard financeiro')
    st.caption('Visão rápida do caixa, resultado do mês, vencidos e valores a receber.')
    ind = indicadores()
    c1,c2 = st.columns(2)
    with c1:
        card('Saldo atual', brl(ind['saldo']), 'Calculado pelos lançamentos. Não é editável.')
        card('Entradas do mês', brl(ind['entradas_mes']), 'Receitas pagas ou em aberto no mês.')
        card('Contas vencidas', brl(ind['pagar_vencido']), 'Contas a pagar atrasadas.')
    with c2:
        card('Resultado do mês', brl(ind['lucro_mes']), 'Entradas menos saídas.')
        card('Saídas do mês', brl(ind['saidas_mes']), 'Despesas pagas ou em aberto no mês.')
        card('Inadimplência', brl(ind['inadimplencia']), 'Valores a receber atrasados.')
    st.divider()
    fluxo = fluxo_mensal()
    if fluxo.empty:
        st.info('Ainda não há lançamentos. Comece cadastrando ou importando sua planilha.')
    else:
        fig = px.bar(fluxo, x='mes', y=['entradas','saidas','resultado'], barmode='group', title='Fluxo de caixa mensal')
        st.plotly_chart(fig, use_container_width=True)
        desp = por_categoria('Saída')
        if not desp.empty:
            fig2 = px.pie(desp, names='categoria', values='valor', title='Despesas por categoria')
            st.plotly_chart(fig2, use_container_width=True)
