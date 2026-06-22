# Sistema Financeiro Novaprint

App financeiro local em Python + Streamlit, responsivo para celular e com armazenamento em SQLite no próprio PC.

## Como instalar

```bash
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

Mac/Linux:
```bash
source .venv/bin/activate
```

Instale dependências:
```bash
pip install -r requirements.txt
```

Rode o sistema:
```bash
streamlit run app.py
```

## Como abrir no celular

1. Deixe o PC e o celular no mesmo Wi‑Fi.
2. Rode `streamlit run app.py` no PC.
3. No terminal aparecerá um endereço de rede, parecido com `http://192.168.0.10:8501`.
4. Abra esse endereço no navegador do celular.
5. No navegador, use “Adicionar à tela inicial”.

## O que preencher

Preencha somente formulários de lançamentos, contas a pagar, contas a receber, categorias e importação.

## O que fica automático/travado

Saldo, entradas, saídas, lucro, inadimplência, vencidos e relatórios são calculados automaticamente.

## Banco de dados

O banco fica em:

```text
database/financeiro.db
```

Não edite esse arquivo manualmente.

## Backup

No menu **Relatórios e backup**, clique em **Gerar backup do banco**.

## Restaurar backup

1. Feche o Streamlit.
2. Copie o backup `.db` para a pasta `database/`.
3. Renomeie para `financeiro.db`.
4. Abra o sistema novamente.

## Estrutura

- `app.py`: entrada principal
- `services/db.py`: SQLite
- `services/importador_planilha.py`: importador Excel/CSV
- `services/relatorios.py`: cálculos financeiros
- `modules/`: telas do sistema
- `database/`: banco local
- `exports/`: relatórios Excel
- `backups/`: backups SQLite
