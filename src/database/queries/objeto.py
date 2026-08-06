"""Query para buscar objeto (tipo) da demanda."""

from config.banco import get_connection


def buscar_objeto(demanda: str) -> str:
    """Busca e classifica o tipo de objeto da demanda (Tela, Relatório, Script)."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT NR_DEMANDA, NR_ANODEM, "
                    "       PORTAL.FN_ARQ_USADOS_DEM(NR_DEMANDA, NR_ANODEM) AS ARQUIVOS "
                    "   FROM SIDEMANDA "
                    "   WHERE NR_DEMCLI = :NR_DEMCLI",
                    {"NR_DEMCLI": demanda},
                )
                row = cursor.fetchone()
                if not row:
                    return ""
                nr_demanda, nr_anodem = row[0], row[1]
                arquivos = str(row[2]).strip() if row[2] is not None else None
                return _classificar_objeto(arquivos, _tem_script(nr_demanda, nr_anodem))
    except Exception as e:
        print(f"[AVISO] Erro ao buscar objeto da demanda {demanda}: {e}")
        return ""


def _classificar_objeto(arquivos: str | None, tem_script: bool) -> str:
    """Classifica o objeto com base nos arquivos e presença de scripts."""
    partes = []

    if arquivos:
        lower = arquivos.lower()

        if "tela" in lower:
            partes.append("Tela")

        if "relatorio" in lower or "relatório" in lower:
            partes.append("Relatório")

    if tem_script:
        partes.append("Script")

    return ", ".join(partes) if partes else ""


def _tem_script(nr_demanda: int, nr_anodem: int) -> bool:
    """Verifica se a demanda possui scripts associados."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT CD_PROCLI FROM SISCRIPT "
                    "   WHERE NR_DEMANDA = :NR_DEMANDA "
                    "     AND NR_ANODEM = :NR_ANODEM",
                    {"NR_DEMANDA": nr_demanda, "NR_ANODEM": nr_anodem},
                )
                return cursor.fetchone() is not None
    except Exception as e:
        print(f"[AVISO] Erro ao verificar scripts da demanda {nr_demanda}/{nr_anodem}: {e}")
        return False
