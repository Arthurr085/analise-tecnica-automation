"""Utilitários para logging e exibição de informações."""

import os


def exibir_log(arquivo_entrada: str, total_demandas: int, arquivo_saida: str) -> None:
    """
    Exibe um resumo do processamento no console.
    
    Args:
        arquivo_entrada: Caminho do arquivo de entrada processado
        total_demandas: Número de demandas processadas
        arquivo_saida: Caminho do arquivo de saída gerado
    """
    print("\n====================================")
    print("ANÁLISE TÉCNICA")
    print("===============\n")
    print(f"Arquivo encontrado:\n{os.path.basename(arquivo_entrada)}\n")
    print(f"Total de demandas:\n{total_demandas}\n")
    print(f"Arquivo gerado:\n{arquivo_saida}")
    print("====================================\n")
