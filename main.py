import sys

from src.leitor import encontrar_arquivo_entrada, ler_planilha
from src.gerador import gerar_analise_tecnica
from src.formatador_excel import formatar_planilha
from src.google_sheets import exportar_para_sheets
from src.utils import gerar_nome_saida, garantir_pastas, exibir_log

PASTA_INPUT = "input"
PASTA_OUTPUT = "output"
PASTA_LOGS = "logs"


def main() -> None:
    garantir_pastas([PASTA_INPUT, PASTA_OUTPUT, PASTA_LOGS])

    print("Iniciando processamento da Análise Técnica...")

    try:
        caminho_entrada = encontrar_arquivo_entrada(PASTA_INPUT)
        print(f"Arquivo encontrado: {caminho_entrada}")

        df_entrada = ler_planilha(caminho_entrada)
        print(f"Planilha lida com sucesso. {len(df_entrada)} linha(s) encontrada(s).")

        df_saida = gerar_analise_tecnica(df_entrada)
        print(f"{len(df_saida)} demanda(s) processada(s).")

        caminho_saida = gerar_nome_saida(PASTA_OUTPUT)
        df_saida.to_excel(caminho_saida, index=False)

        print("Aplicando formatação Excel...")
        formatar_planilha(caminho_saida)

        # Exportar para Google Sheets (opcional - não interrompe se falhar)
        try:
            print("Exportando para Google Sheets...")
            sucesso, mensagem = exportar_para_sheets(df_saida)
            if sucesso:
                print(f"[OK] {mensagem}")
            else:
                print(f"[AVISO] Google Sheets: {mensagem}")
        except Exception as e:
            print(f"[AVISO] Erro ao exportar para Google Sheets: {e}")

        exibir_log(caminho_entrada, len(df_saida), caminho_saida)

    except FileNotFoundError as e:
        print(f"\n[ERRO] {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"\n[ERRO] Planilha inválida: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERRO] Falha inesperada: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
