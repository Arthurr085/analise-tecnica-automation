"""Query para buscar analista/programador da demanda."""

from config.banco import get_connection


def buscar_analista_programador(demanda: str) -> str:
    """Busca o analista/programador que mais trabalhou na demanda."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT NR_DEMANDA, NR_ANODEM "
                    "   FROM SIDEMANDA "
                    "   WHERE NR_DEMCLI = :NR_DEMCLI",
                    {"NR_DEMCLI": demanda},
                )
                row = cursor.fetchone()
                if not row:
                    return ""
                nr_demanda, nr_anodem = row[0], row[1]

                cursor.execute(
                    "SELECT DS_LOGIN "
                    "   FROM ( "
                    "       SELECT SIUSUARI.DS_LOGIN, "
                    "              SUM(CAST(SIDEMAITEM.HR_FIM AS DATE) - CAST(SIDEMAITEM.HR_INICIO AS DATE)) AS TEMPO_TOTAL "
                    "           FROM SIDEMAITEM "
                    "           INNER JOIN SIUSUARI ON SIUSUARI.CD_USUARI = SIDEMAITEM.CD_USUDES "
                    "           WHERE SIDEMAITEM.NR_DEMANDA = :NR_DEMANDA "
                    "             AND SIDEMAITEM.NR_ANODEM = :NR_ANODEM "
                    "             AND SIDEMAITEM.HR_INICIO IS NOT NULL "
                    "             AND SIDEMAITEM.HR_FIM IS NOT NULL "
                    "           GROUP BY SIUSUARI.DS_LOGIN "
                    "           ORDER BY TEMPO_TOTAL DESC "
                    "   ) WHERE ROWNUM = 1",
                    {"NR_DEMANDA": nr_demanda, "NR_ANODEM": nr_anodem},
                )
                row = cursor.fetchone()
                return str(row[0]).strip() if row and row[0] is not None else ""
    except Exception as e:
        print(f"[AVISO] Erro ao buscar analista/programador da demanda {demanda}: {e}")
        return ""
