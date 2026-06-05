import pandas as pd

from config.colunas_saida import COLUNAS_SAIDA
from src.banco import buscar_dados_demanda


def gerar_analise_tecnica(df_entrada: pd.DataFrame) -> pd.DataFrame:
    """Gera o DataFrame da análise técnica a partir da planilha do cliente."""
    registros = [_mapear_linha(row) for _, row in df_entrada.iterrows()]
    return pd.DataFrame(registros, columns=COLUNAS_SAIDA)


def _mapear_linha(row: pd.Series) -> dict:
    demanda = row.get("Demanda", "").strip()
    dados_banco = buscar_dados_demanda(demanda)

    return {
        "Demanda": demanda,
        "Descrição": dados_banco["descricao"],
        "Analista/Programador": dados_banco["analista_programador"],
        "Demandas Pendentes": dados_banco["demandas_pendentes"],
        "Observação": row.get("Observação", "").strip(),
        "Objeto (Envolvimento na demanda)": dados_banco["objeto"],
        "Programa Alterado": row.get("Sistema", "").strip(),
        "Versão Pacote Atualização": row.get("Versão", "").strip(),
        "Data Envio Pacote": "",
    }
