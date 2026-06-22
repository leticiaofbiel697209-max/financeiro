import streamlit as st
from dotenv import load_dotenv
from services.db import init_db, update_overdue_statuses
from modules import dashboard, lancamentos, contas_pagar, contas_receber, categorias, relatorios, manual, importar

load_dotenv()
st.set_page_config(page_title='Financeiro Novaprint', page_icon='💼', layout='wide', initial_sidebar_state='expanded')

CSS = """
<style>
:root { --bg:#F7F8FA; --card:#FFFFFF; --primary:#25324B; --muted:#6B7280; --line:#E5E7EB; }
.stApp { background: var(--bg); }
[data-testid="stSidebar"] { background: #111827; }
[data-testid="stSidebar"] * { color: #F9FAFB !important; }
.block-container { padding-top: 1.3rem; padding-bottom: 3rem; max-width: 1180px; }
h1,h2,h3 { color:#111827; letter-spacing:-.02em; }
.kpi-card { background: var(--card); border:1px solid var(--line); border-radius:20px; padding:18px; margin-bottom:14px; box-shadow:0 8px 24px rgba(15,23,42,.05); }
.kpi-label { color:var(--muted); font-size:.92rem; margin-bottom:8px; }
.kpi-value { color:#111827; font-size:1.65rem; font-weight:800; }
.kpi-help { color:#6B7280; font-size:.78rem; margin-top:7px; }
.stButton>button, .stDownloadButton>button { border-radius:14px; min-height:44px; font-weight:700; }
[data-testid="stDataFrame"] { border-radius:16px; overflow:hidden; }
@media(max-width: 768px){ .block-container { padding-left: .8rem; padding-right:.8rem; } .kpi-value{font-size:1.35rem;} }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

init_db()
update_overdue_statuses()

st.sidebar.title('💼 Financeiro')
st.sidebar.caption('Novaprint / Local SQLite')
page = st.sidebar.radio('Menu', [
    'Dashboard', 'Lançamentos', 'Contas a pagar', 'Contas a receber', 'Importar planilha', 'Categorias', 'Relatórios e backup', 'Manual'
])
st.sidebar.divider()
st.sidebar.info('Use no celular abrindo o endereço local do Streamlit no mesmo Wi‑Fi do PC.')

if page == 'Dashboard': dashboard.render()
elif page == 'Lançamentos': lancamentos.render()
elif page == 'Contas a pagar': contas_pagar.render()
elif page == 'Contas a receber': contas_receber.render()
elif page == 'Importar planilha': importar.render()
elif page == 'Categorias': categorias.render()
elif page == 'Relatórios e backup': relatorios.render()
elif page == 'Manual': manual.render()
