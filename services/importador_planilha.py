import pandas as pd
from services.db import execute_many, execute

SUGESTOES = {
    'data': ['data','dt','emissão','emissao','vencimento','pagamento'],
    'descricao': ['descrição','descricao','histórico','historico','cliente','fornecedor','nome'],
    'valor': ['valor','total','r$','receita','despesa','pago'],
    'tipo': ['tipo','entrada','saída','saida','categoria'],
    'categoria': ['categoria','classificação','classificacao','grupo','conta'],
    'status': ['status','situação','situacao','pago','aberto'],
    'forma_pagamento': ['forma','pagamento','meio']
}


def read_file(file):
    name = file.name.lower()
    if name.endswith('.csv'):
        return {'CSV': pd.read_csv(file)}
    return pd.read_excel(file, sheet_name=None, engine='openpyxl')


def guess_columns(cols):
    result = {}
    normalized = {c: str(c).strip().lower() for c in cols}
    for target, keys in SUGESTOES.items():
        for col, low in normalized.items():
            if any(k in low for k in keys):
                result[target] = col
                break
    return result


def parse_money(v):
    if pd.isna(v): return 0.0
    if isinstance(v, (int,float)): return float(v)
    s = str(v).replace('R$','').replace(' ','').strip()
    if ',' in s:
        s = s.replace('.','').replace(',','.')
    try: return float(s)
    except Exception: return 0.0


def normalize_tipo(v, valor=0):
    s = str(v or '').lower()
    if 'entr' in s or 'rece' in s or 'venda' in s: return 'Entrada'
    if 'saí' in s or 'sai' in s or 'desp' in s or 'pagar' in s: return 'Saída'
    return 'Saída' if valor < 0 else 'Entrada'


def normalize_status(v):
    s = str(v or '').lower()
    if 'cancel' in s: return 'Cancelado'
    if 'atras' in s or 'venc' in s: return 'Atrasado'
    if 'pago' in s or 'receb' in s or 'quit' in s: return 'Pago'
    return 'Em aberto'


def import_lancamentos(df, mapping, origem='Importação'):
    rows = []
    for _, r in df.iterrows():
        valor = abs(parse_money(r.get(mapping.get('valor'))))
        if valor == 0: continue
        raw_data = r.get(mapping.get('data'))
        data = pd.to_datetime(raw_data, errors='coerce', dayfirst=True)
        if pd.isna(data): continue
        tipo = normalize_tipo(r.get(mapping.get('tipo')), valor)
        descricao = str(r.get(mapping.get('descricao'), '') or '').strip() or 'Lançamento importado'
        categoria = str(r.get(mapping.get('categoria'), 'Outros') or 'Outros').strip()
        status = normalize_status(r.get(mapping.get('status')))
        forma = str(r.get(mapping.get('forma_pagamento'), 'Outro') or 'Outro').strip()
        rows.append((data.date().isoformat(), descricao, tipo, categoria, valor, forma, status, '', origem))
    if rows:
        execute_many("""INSERT INTO lancamentos
        (data, descricao, tipo, categoria, valor, forma_pagamento, status, observacao, origem)
        VALUES (?,?,?,?,?,?,?,?,?)""", rows)
        execute("INSERT INTO importacoes(arquivo, linhas_importadas) VALUES (?,?)", (origem, len(rows)))
    return len(rows)
