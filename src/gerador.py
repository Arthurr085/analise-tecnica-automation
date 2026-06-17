import pandas as pd

from config.colunas_saida import COLUNAS_SAIDA
from src.banco import buscar_dados_demanda


def gerar_analise_tecnica(df_entrada: pd.DataFrame) -> pd.DataFrame:
    """Gera o DataFrame da análise técnica a partir da planilha do cliente."""
    blocos = _agrupar_por_demanda(df_entrada)
    registros = [_mapear_bloco(bloco) for bloco in blocos]
    return pd.DataFrame(registros, columns=COLUNAS_SAIDA)


def _agrupar_por_demanda(df: pd.DataFrame) -> list:
    """Agrupa as linhas em blocos por demanda.

    A planilha de entrada usa células mescladas: uma demanda ocupa várias
    linhas, onde só Sistema/Versão variam e as demais colunas vêm vazias
    (preenchidas apenas na primeira linha do bloco).
    """
    blocos = []
    atual = None
    for _, row in df.iterrows():
        if row.get("Demanda", "").strip():
            atual = [row]
            blocos.append(atual)
        elif atual is not None:
            atual.append(row)
    return blocos


def _mapear_bloco(bloco: list) -> dict:
    primeira = bloco[0]
    demanda = primeira.get("Demanda", "").strip()
    dados_banco = buscar_dados_demanda(demanda)

    sistemas = []
    versoes = []
    for row in bloco:
        sistema = row.get("Sistema", "").strip()
        versao = row.get("Versão", "").strip()
        if sistema or versao:
            sistemas.append(sistema)
            versoes.append(versao)

    return {
        "Demanda": demanda,
        "Descrição": dados_banco["descricao"],
        "Analista/Programador": dados_banco["analista_programador"],
        "Demandas Pendentes": dados_banco["demandas_pendentes"],
        "Observação": primeira.get("Observação", "").strip(),
        "Objeto (Envolvimento na demanda)": dados_banco["objeto"],
        "Programa Alterado": ", ".join(sistemas),
        "Versão Pacote Atualização": ", ".join(versoes),
        "Data Envio Pacote": "",
    }
