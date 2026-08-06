"""
Módulo principal src - Análise Técnica Automation.

Estrutura:
    - core/: Lógica de negócio (gerador de análise)
    - database/: Acesso a dados Oracle
    - io/: Entrada/Saída de arquivos (Excel, Google Sheets)
    - formatacao/: Formatação visual de planilhas
    - utils/: Utilitários diversos
"""

from src.core import gerar_analise_tecnica
from src.database import buscar_dados_demanda
from src.io import encontrar_arquivo_entrada, ler_planilha, exportar_para_sheets
from src.formatacao import formatar_planilha
from src.utils import garantir_pastas, gerar_nome_saida, exibir_log

__all__ = [
    # Core
    "gerar_analise_tecnica",
    # Database
    "buscar_dados_demanda",
    # IO
    "encontrar_arquivo_entrada",
    "ler_planilha",
    "exportar_para_sheets",
    # Formatação
    "formatar_planilha",
    # Utils
    "garantir_pastas",
    "gerar_nome_saida",
    "exibir_log",
]
