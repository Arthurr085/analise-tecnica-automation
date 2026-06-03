import os
from datetime import date


def gerar_nome_saida(pasta_output: str) -> str:
    """Retorna o caminho completo do arquivo de saída com a data de hoje."""
    hoje = date.today().strftime("%Y-%m-%d")
    return os.path.join(pasta_output, f"analise_tecnica_{hoje}.xlsx")


def garantir_pastas(pastas: list[str]) -> None:
    """Cria as pastas necessárias caso não existam."""
    for pasta in pastas:
        os.makedirs(pasta, exist_ok=True)


def exibir_log(arquivo_entrada: str, total_demandas: int, arquivo_saida: str) -> None:
    print("\n====================================")
    print("ANÁLISE TÉCNICA")
    print("===============\n")
    print(f"Arquivo encontrado:\n{os.path.basename(arquivo_entrada)}\n")
    print(f"Total de demandas:\n{total_demandas}\n")
    print(f"Arquivo gerado:\n{arquivo_saida}")
    print("====================================\n")
