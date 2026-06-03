import os
import glob
import pandas as pd

from config.mapeamento import COLUNAS_OBRIGATORIAS


def encontrar_arquivo_entrada(pasta_input: str) -> str:
    """Retorna o .xlsx mais recente dentro da pasta input/."""
    arquivos = glob.glob(os.path.join(pasta_input, "*.xlsx"))
    if not arquivos:
        raise FileNotFoundError(f"Nenhum arquivo .xlsx encontrado em '{pasta_input}'")
    return max(arquivos, key=os.path.getmtime)


def ler_planilha(caminho: str) -> pd.DataFrame:
    """Lê a primeira aba da planilha e valida as colunas obrigatórias."""
    df = pd.read_excel(caminho, sheet_name=0, dtype=str, keep_default_na=False)
    df.columns = [col.strip() for col in df.columns]
    _validar_colunas(df)
    return df


def _validar_colunas(df: pd.DataFrame) -> None:
    colunas_presentes = set(df.columns)
    colunas_obrigatorias = set(COLUNAS_OBRIGATORIAS)

    ausentes = colunas_obrigatorias - colunas_presentes
    if ausentes:
        raise ValueError(f"Colunas obrigatórias ausentes: {', '.join(sorted(ausentes))}")

    extras = colunas_presentes - colunas_obrigatorias
    if extras:
        print(f"[AVISO] Colunas extras encontradas (serão ignoradas): {', '.join(sorted(extras))}")
