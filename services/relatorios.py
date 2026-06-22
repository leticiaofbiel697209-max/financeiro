from datetime import datetime, timedelta
import pandas as pd
from services.db import fetch_df


def brl(v):
    try:
        return f"R$ {float(v):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    except Exception:
        return "R$ 0,00"


def get_lancamentos():
    return fetch_df("SELECT * FROM lancamentos ORDER BY data DESC, id DESC")


def get_pagar():
    return fetch_df("SELECT * FROM contas_pagar ORDER BY vencimento ASC, id DESC")


def get_receber():
    return fetch_df("SELECT * FROM contas_receber ORDER BY vencimento ASC, id DESC")


def indicadores():
    hoje = datetime.now().date()
    inicio_mes = hoje.replace(day=1).isoformat()
    fim_30 = (hoje + timedelta(days=30)).isoformat()
    lanc = get_lancamentos()
    pagar = get_pagar()
    receber = get_receber()
    if not lanc.empty:
        lanc['valor'] = pd.to_numeric(lanc['valor'], errors='coerce').fillna(0)
        lanc_mes = lanc[lanc['data'] >= inicio_mes]
        entradas_mes = lanc_mes[(lanc_mes['tipo']=='Entrada') & (lanc_mes['status'].isin(['Pago','Em aberto']))]['valor'].sum()
        saidas_mes = lanc_mes[(lanc_mes['tipo']=='Saída') & (lanc_mes['status'].isin(['Pago','Em aberto']))]['valor'].sum()
        saldo = lanc[(lanc['status'].isin(['Pago','Em aberto']))].apply(lambda r: r['valor'] if r['tipo']=='Entrada' else -r['valor'], axis=1).sum()
    else:
        entradas_mes = saidas_mes = saldo = 0
    lucro = entradas_mes - saidas_mes
    def total(df, status, datecol=None, future=False):
        if df.empty: return 0
        d = df.copy(); d['valor'] = pd.to_numeric(d['valor'], errors='coerce').fillna(0)
        if datecol and future:
            d = d[(d[datecol] >= hoje.isoformat()) & (d[datecol] <= fim_30)]
        return d[d['status'].isin(status)]['valor'].sum()
    return {
        'saldo': saldo,
        'entradas_mes': entradas_mes,
        'saidas_mes': saidas_mes,
        'lucro_mes': lucro,
        'pagar_vencido': total(pagar, ['Atrasado']),
        'pagar_30': total(pagar, ['Em aberto'], 'vencimento', True),
        'receber_aberto': total(receber, ['Em aberto','Atrasado']),
        'inadimplencia': total(receber, ['Atrasado']),
    }


def fluxo_mensal():
    df = get_lancamentos()
    if df.empty: return pd.DataFrame(columns=['mes','entradas','saidas','resultado'])
    df['data'] = pd.to_datetime(df['data'], errors='coerce')
    df['valor'] = pd.to_numeric(df['valor'], errors='coerce').fillna(0)
    df = df[df['status'].isin(['Pago','Em aberto'])]
    df['mes'] = df['data'].dt.strftime('%Y-%m')
    g = df.groupby(['mes','tipo'])['valor'].sum().unstack(fill_value=0).reset_index()
    g['entradas'] = g.get('Entrada', 0)
    g['saidas'] = g.get('Saída', 0)
    g['resultado'] = g['entradas'] - g['saidas']
    return g[['mes','entradas','saidas','resultado']].sort_values('mes')


def por_categoria(tipo):
    df = get_lancamentos()
    if df.empty: return pd.DataFrame(columns=['categoria','valor'])
    df['valor'] = pd.to_numeric(df['valor'], errors='coerce').fillna(0)
    df = df[(df['tipo']==tipo) & (df['status'].isin(['Pago','Em aberto']))]
    return df.groupby('categoria', dropna=False)['valor'].sum().reset_index().sort_values('valor', ascending=False)


def export_excel(path='exports/relatorio_financeiro.xlsx'):
    with pd.ExcelWriter(path, engine='openpyxl') as writer:
        get_lancamentos().to_excel(writer, 'Lançamentos', index=False)
        get_pagar().to_excel(writer, 'Contas a pagar', index=False)
        get_receber().to_excel(writer, 'Contas a receber', index=False)
        fluxo_mensal().to_excel(writer, 'Fluxo mensal', index=False)
        por_categoria('Saída').to_excel(writer, 'Despesas por categoria', index=False)
        por_categoria('Entrada').to_excel(writer, 'Receitas por categoria', index=False)
    return path
