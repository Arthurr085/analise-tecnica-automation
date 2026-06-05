from config.banco import get_connection


def buscar_dados_demanda(demanda: str) -> dict:
    """Retorna dados complementares de uma demanda consultando o Oracle."""
    return {
        "descricao": _buscar_descricao(demanda),
        "analista_programador": "",  # Fase 3
    }


def _buscar_descricao(demanda: str) -> str:
    """
    SELECT ds_titulo FROM SIDEMANDA
    WHERE SIDEMANDA.nr_demcli = :nr_demcli
    """
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT ds_titulo " \
                    "   FROM SIDEMANDA " \
                "   WHERE nr_demcli = :nr_demcli",
                    {"nr_demcli": demanda},
                )
                row = cursor.fetchone()
                return str(row[0]).strip() if row and row[0] is not None else ""
    except Exception as e:
        print(f"[AVISO] Erro ao buscar descrição da demanda {demanda}: {e}")
        return ""
