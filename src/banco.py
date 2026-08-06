from config.banco import get_connection


def buscar_dados_demanda(demanda: str) -> dict:
    """Retorna dados complementares de uma demanda consultando o Oracle."""
    return {
        "descricao": _buscar_descricao(demanda),
        "analista_programador": _buscar_analista_programador(demanda),
        "objeto": _buscar_objeto(demanda),
        "demandas_pendentes": _buscar_demandas_pendentes(demanda),
    }


def _buscar_descricao(demanda: str) -> str:
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


def _buscar_analista_programador(demanda: str) -> str:
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


def _buscar_objeto(demanda: str) -> str:
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


def _buscar_demandas_pendentes(demanda: str) -> str:
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
