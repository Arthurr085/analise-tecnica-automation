import os
import re
from datetime import date


def gerar_nome_saida(pasta_output: str) -> str:
    """Gera o próximo nome de saída com versionamento automático.

    Formato: analise_tecnica_DD_MM_YYYY_vN.xlsx
    O N é incrementado automaticamente com base nos arquivos já existentes em output/.
    """
    hoje = date.today().strftime("%d_%m_%Y")
    padrao = re.compile(rf"^analise_tecnica_{hoje}_v(\d+)\.xlsx$", re.IGNORECASE)

    maior_versao = 0
    if os.path.isdir(pasta_output):
        for nome in os.listdir(pasta_output):
            match = padrao.match(nome)
            if match:
                maior_versao = max(maior_versao, int(match.group(1)))

    proxima_versao = maior_versao + 1
    nome_arquivo = f"analise_tecnica_{hoje}_v{proxima_versao}.xlsx"
    return os.path.join(pasta_output, nome_arquivo)


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
