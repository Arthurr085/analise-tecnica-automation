"""Leitor de planilhas Excel de entrada."""

import os
import re
import glob
from datetime import datetime

import pandas as pd

from config.mapeamento import COLUNAS_OBRIGATORIAS

# Padrão esperado: DD_MM_YYYY_vN.xlsx (ex: 03_06_2026_v1.xlsx)
_PADRAO_NOME = re.compile(r"^(\d{2}_\d{2}_\d{4})_v(\d+)\.xlsx$", re.IGNORECASE)


def encontrar_arquivo_entrada(pasta_input: str) -> str:
    """
    Retorna o arquivo mais recente de input/ com base na data e versão do nome.
    
    Args:
        pasta_input: Caminho da pasta de entrada
        
    Returns:
        Caminho completo do arquivo mais recente
        
    Raises:
        FileNotFoundError: Se nenhum arquivo válido for encontrado
    """
    todos = glob.glob(os.path.join(pasta_input, "*.xlsx"))

    if not todos:
        raise FileNotFoundError(
            f"Nenhum arquivo encontrado em '{pasta_input}'.\n"
            f"  Formato esperado: DD_MM_YYYY_v1.xlsx  (ex: 03_06_2026_v1.xlsx)"
        )

    candidatos = []
    for caminho in todos:
        match = _PADRAO_NOME.match(os.path.basename(caminho))
        if match:
            data = datetime.strptime(match.group(1), "%d_%m_%Y")
            versao = int(match.group(2))
            candidatos.append((data, versao, caminho))

    if not candidatos:
        raise FileNotFoundError(
            f"Nenhum arquivo no formato esperado encontrado em '{pasta_input}'.\n"
            f"  Formato esperado: DD_MM_YYYY_v1.xlsx  (ex: 03_06_2026_v1.xlsx)"
        )

    candidatos.sort(key=lambda x: (x[0], x[1]), reverse=True)
    return candidatos[0][2]


def ler_planilha(caminho: str) -> pd.DataFrame:
    """
    Lê a primeira aba da planilha e valida as colunas obrigatórias.
    
    Args:
        caminho: Caminho do arquivo Excel
        
    Returns:
        DataFrame com os dados da planilha
        
    Raises:
        ValueError: Se colunas obrigatórias estiverem ausentes
    """
    df = pd.read_excel(caminho, sheet_name=0, dtype=str, keep_default_na=False)
    df.columns = [col.strip() for col in df.columns]
    _validar_colunas(df)
    return df


def _validar_colunas(df: pd.DataFrame) -> None:
    """Valida se todas as colunas obrigatórias estão presentes."""
    colunas_presentes = set(df.columns)
    colunas_obrigatorias = set(COLUNAS_OBRIGATORIAS)

    ausentes = colunas_obrigatorias - colunas_presentes
    if ausentes:
        raise ValueError(f"Colunas obrigatórias ausentes: {', '.join(sorted(ausentes))}")

    extras = colunas_presentes - colunas_obrigatorias
    if extras:
        print(f"[AVISO] Colunas extras encontradas (serão ignoradas): {', '.join(sorted(extras))}")
