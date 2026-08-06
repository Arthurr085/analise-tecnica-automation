"""Service para orquestrar as queries de demanda."""

from src.database.queries.descricao import buscar_descricao
from src.database.queries.analista import buscar_analista_programador
from src.database.queries.objeto import buscar_objeto
from src.database.queries.pendentes import buscar_demandas_pendentes


def buscar_dados_demanda(demanda: str) -> dict:
    """
    Retorna dados complementares de uma demanda consultando o Oracle.
    
    Args:
        demanda: Número da demanda do cliente (NR_DEMCLI)
        
    Returns:
        Dicionário com: descricao, analista_programador, objeto, demandas_pendentes
    """
    return {
        "descricao": buscar_descricao(demanda),
        "analista_programador": buscar_analista_programador(demanda),
        "objeto": buscar_objeto(demanda),
        "demandas_pendentes": buscar_demandas_pendentes(demanda),
    }
