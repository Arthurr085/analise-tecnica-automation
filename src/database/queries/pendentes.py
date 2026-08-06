"""Query para buscar demandas pendentes relacionadas."""

from config.banco import get_connection


def buscar_demandas_pendentes(demanda: str) -> str:
    """Busca demandas pendentes que compartilham arquivos com a demanda atual."""
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
                    "SELECT SIDEMANDA.NR_DEMANDA, SIDEMANDA.NR_ANODEM, SIDEMANDA.NR_DEMCLI "
                    "   FROM SIDEMANDA "
                    "   WHERE (SELECT COUNT(MOSERDEM.NR_DEMANDA) FROM MOSERDEM "
                    "           WHERE MOSERDEM.NR_DEMANDA = SIDEMANDA.NR_DEMANDA "
                    "             AND MOSERDEM.NR_ANODEM = SIDEMANDA.NR_ANODEM "
                    "             AND (SELECT COUNT(MOSERDEM.NR_DEMANDA) FROM MOSERDEM A "
                    "                   WHERE A.CD_PROJETO = MOSERDEM.CD_PROJETO "
                    "                     AND A.DS_NOMEARQ = MOSERDEM.DS_NOMEARQ "
                    "                     AND A.NR_DEMANDA = :NR_DEMANDA "
                    "                     AND A.NR_ANODEM = :NR_ANODEM) > 0) > 0",
                    {"NR_DEMANDA": nr_demanda, "NR_ANODEM": nr_anodem},
                )
                resultados = []
                for row in cursor:
                    dem_nr, dem_ano, dem_cli = row[0], row[1], row[2]
                    if dem_nr == nr_demanda and dem_ano == nr_anodem:
                        continue
                    if dem_cli is not None:
                        resultados.append(str(dem_cli).strip())
                    else:
                        resultados.append(f"{dem_nr}_{dem_ano} (LOCAL)")
                return ", ".join(resultados)
    except Exception as e:
        print(f"[AVISO] Erro ao buscar demandas pendentes da demanda {demanda}: {e}")
        return ""
