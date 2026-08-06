"""Constantes de estilo para formatação de planilhas Excel."""

from openpyxl.styles import Border, Side

# Cor do cabeçalho (azul)
COR_CABECALHO = "8EAADB"

# Borda fina para células
BORDA_THIN = Border(
    left=Side(style="thin"),
    right=Side(style="thin"),
    top=Side(style="thin"),
    bottom=Side(style="thin"),
)

# Colunas que devem ser centralizadas
COLUNAS_CENTRO = {
    "Demanda",
    "Analista/Programador",
    "Objeto (Envolvimento na demanda)",
    "Programa Alterado",
    "Versão Pacote Atualização",
}

# Colunas que sempre recebem borda (mesmo vazias)
COLUNAS_BORDA_SEMPRE = {"Demandas Pendentes"}
