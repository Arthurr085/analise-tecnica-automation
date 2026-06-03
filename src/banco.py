# Camada de dados — Fase 1: retorna dados mockados.
# Na Fase 2, substituir pela consulta Oracle real usando config/banco.py.


def buscar_dados_demanda(demanda: str) -> dict:
    """Retorna dados complementares de uma demanda.

    Fase 2: consultar Oracle e retornar descricao e analista_programador reais.
    """
    return {
        "descricao": "",
        "analista_programador": "",
    }
