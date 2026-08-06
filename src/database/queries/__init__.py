"""Queries individuais para buscar dados de demandas."""

from src.database.queries.descricao import buscar_descricao
from src.database.queries.analista import buscar_analista_programador
from src.database.queries.objeto import buscar_objeto
from src.database.queries.pendentes import buscar_demandas_pendentes

__all__ = [
    "buscar_descricao",
    "buscar_analista_programador",
    "buscar_objeto",
    "buscar_demandas_pendentes",
]
