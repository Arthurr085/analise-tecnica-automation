"""Query para buscar descrição da demanda."""

from config.banco import get_connection


def buscar_descricao(demanda: str) -> str:
    """Busca a descrição (título) de uma demanda no banco."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT DS_TITULO "
                    "   FROM SIDEMANDA "
                    "   WHERE NR_DEMCLI = :NR_DEMCLI",
                    {"NR_DEMCLI": demanda},
                )
                row = cursor.fetchone()
                return str(row[0]).strip() if row and row[0] is not None else ""
    except Exception as e:
        print(f"[AVISO] Erro ao buscar descrição da demanda {demanda}: {e}")
        return ""
