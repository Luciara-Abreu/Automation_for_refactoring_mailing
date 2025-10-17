# %%
import sys
sys.path.append('H:/Tecnologia/EQUIPE - DADOS/dev_env/000_base/database_functions/')
from database import Database
sys.path.append('H:/Tecnologia/EQUIPE - DADOS/dev_env/000_base/modules/')
from utils import Format_data
from datetime import datetime
import numpy as np
import pandas as pd

db = Database()
fd = Format_data()

# %%
## Valida se tem clientes vencidos com status Enviar (são os que acabou o dia e não deu tempo de ligar para eles)
## Valida se tem clientes vencidos com Status diferente de Enviar, Completou e Em Execucao (Ligações que não deram certo)
## Valida se tem base sem data de hoje para ligar.(Base sem dados para ligar hoje)

# BLOCO 1
from datetime import datetime
import pandas as pd

hoje = datetime.today().date()
mes_referencia = hoje.strftime('%m/%Y') 

tabelas_campanhas = ['CAMP_CARDIOLOGIA',  'CAMP_OFTALMOLOGIA','CAMP_PSICO_PSIQUI', 'CAMP_ODONTO',
'CAMP_CHECKUP_MULHER', 'CAMP_CHECKUP_SAUDE', 'CAMP_DERMATOLOGIA','CAMP_ODONTO_GERAL','CAMP_CHECKUP_HOMEM','CAMP_ORTODONTIA']

#tabelas_campanhas = [  'CAMP_DERMATOLOGIA'  ]


registros_para_redistribuir = {}

for tabela in tabelas_campanhas:
    print(f"\n🔍 Validando campanha: {tabela}")

    # 1. Vencidos com STATUS <> 'Completou'
    query_vencidos = f"""
        SELECT SEQ_CAMPANHA, COD_PACIENTE, NOME_PACIENTE, FONE, LIGAR_EM, STATUS, TEMPO_LIGACAO, CANAIS, CAMPANHA
        FROM {tabela}
        WHERE TO_CHAR(LIGAR_EM, 'MM/YYYY') = '{mes_referencia}'
          AND LIGAR_EM < TO_DATE('{hoje.strftime('%Y-%m-%d')}', 'YYYY-MM-DD')
          AND STATUS NOT IN ('Completou')
    """
    df_vencidos = pd.read_sql(query_vencidos, con=db.connection)

    # 2. Registros com STATUS = 'Enviar' ou 'Em Execucao' na data de hoje
    query_hoje = f"""
        SELECT SEQ_CAMPANHA, COD_PACIENTE, NOME_PACIENTE, FONE, LIGAR_EM, STATUS, TEMPO_LIGACAO, CANAIS, CAMPANHA
        FROM {tabela}
        WHERE TO_CHAR(LIGAR_EM, 'YYYY-MM-DD') = '{hoje.strftime('%Y-%m-%d')}'
          AND STATUS IN ('Enviar', 'Em Execucao')
    """
    df_hoje = pd.read_sql(query_hoje, con=db.connection)



    # 3. Acumula os registros que precisam ser redistribuídos
    df_acumulado = pd.DataFrame()

    if df_vencidos.shape[0] > 0:
        print(f"🔄 {len(df_vencidos)} registros vencidos serão redistribuídos.")
        df_acumulado = pd.concat([df_acumulado, df_vencidos])

    if df_acumulado.empty:
        print(f"✅ Nenhum registro com STATUS = 'Enviar' para redistribuir.")
    else:
        registros_para_redistribuir[tabela] = df_acumulado.copy()  

# %%
#BLOCO 2

from datetime import datetime
import pandas as pd

hoje = datetime.today().date()
mes_referencia = hoje.strftime('%m/%Y')

# 1. Carrega o calendário a partir de hoje
df_calendario = db.extract_data(f"""
    SELECT * FROM DADOS_CALENDARIO_BI
    WHERE DATA >= TO_DATE('{hoje.strftime('%Y-%m-%d')}', 'YYYY-MM-DD')
""")
df_calendario['DATA'] = pd.to_datetime(df_calendario['DATA'], errors='coerce')

# 2. Filtra dias úteis com peso
dias_uteis_validos = df_calendario[
    (df_calendario['FERIADO_FOLGA'] != 'S') &
    (df_calendario['DIAS_TT_MES'] > 0)
][['DATA', 'DIAS_TT_MES']].copy()

if dias_uteis_validos.empty:
    raise ValueError("⚠️ Nenhum dia útil disponível a partir de hoje no calendário.")



# %%
# BLOCO 3 — Redistribuição e Atualização
for tabela, df_base in registros_para_redistribuir.items():
    print(f"\n🔄 Iniciando redistribuição para campanha: {tabela}")
    print(f"🧪 Total de registros recebidos: {len(df_base)}")

    df_base = df_base.reset_index(drop=True)
    df_base = df_base.drop_duplicates(subset=['COD_PACIENTE', 'CAMPANHA'])

    if df_base.empty:
        print(f"⚠️ Nenhum registro válido para redistribuir em {tabela}.")
        continue

    # Redistribuição proporcional com garantia de hoje
    total = len(df_base)
    datas_expandidas = []

    for _, row in dias_uteis_validos.iterrows():
        peso = row['DIAS_TT_MES']
        rep = int(peso * 2)
        datas_expandidas.extend([row['DATA']] * rep)

    data_hoje = pd.to_datetime(hoje)
    if data_hoje not in datas_expandidas:
        datas_expandidas.insert(0, data_hoje)

    df_base['LIGAR_EM'] = [
        datas_expandidas[i % len(datas_expandidas)].strftime('%Y-%m-%d')
        for i in range(total)
    ]
    df_base['STATUS'] = 'Enviar'

    # Verifica se os campos essenciais existem e preenche se necessário
    campos_essenciais = ['COD_PACIENTE', 'FONE', 'CANAIS', 'CAMPANHA']
    for campo in campos_essenciais:
        if campo not in df_base.columns:
            print(f"⚠️ Campo ausente: {campo} — preenchendo com valor padrão.")
            df_base[campo] = 0

    # Preenche nulos com valores padrão
    df_base['FONE'] = df_base['FONE'].fillna(999999999)
    df_base['CANAIS'] = df_base['CANAIS'].fillna(1)

    # Converte para inteiro com tolerância
    for campo in ['COD_PACIENTE', 'FONE', 'CANAIS']:
        df_base[campo] = pd.to_numeric(df_base[campo], errors='coerce').fillna(0).astype(int)

    print(f"🧪 Registros prontos para atualização: {len(df_base)}")

    # Atualização no banco
    sql_update = f"""
        UPDATE AGE.{tabela}
        SET 
            STATUS = :1,
            LIGAR_EM = TO_DATE(:2, 'YYYY-MM-DD'),
            CANAIS = :3
        WHERE 
            COD_PACIENTE = :4
            AND CAMPANHA = :5
    """

    dados = []
    for _, row in df_base.iterrows():
        try:
            dados.append((
                'Enviar',
                row['LIGAR_EM'],
                row['CANAIS'],
                row['COD_PACIENTE'],
                str(row['CAMPANHA']).strip().upper().replace("'", "''")
            ))
        except Exception as e:
            print(f"⚠️ Erro ao preparar linha: {e}")
            continue

    if dados:
        try:
            db.cursor.executemany(sql_update, dados)
            db.connection.commit()
            print(f"✅ {len(dados)} registros atualizados para {tabela}.")
        except Exception as e:
            print(f"❌ Erro ao executar UPDATE: {e}")
    else:
        print(f"⚠️ Nenhum dado válido para atualizar em {tabela}.")



