"""
Módulo para exportação de dados para Google Sheets usando gspread.
"""

import os
from typing import Tuple

import pandas as pd
from dotenv import load_dotenv

load_dotenv()

GOOGLE_CREDENTIALS_JSON = os.getenv("GOOGLE_CREDENTIALS_JSON", "")
GOOGLE_SPREADSHEET_ID = os.getenv("GOOGLE_SPREADSHEET_ID", "")
GOOGLE_SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME", "Sheet1")


def _verificar_configuracao() -> Tuple[bool, str]:
    """
    Verifica se as variáveis de ambiente do Google Sheets estão configuradas.
    
    Returns:
        Tuple[bool, str]: (configurado, mensagem de erro se não configurado)
    """
    if not GOOGLE_CREDENTIALS_JSON:
        return False, "GOOGLE_CREDENTIALS_JSON não configurado no .env"
    
    if not os.path.exists(GOOGLE_CREDENTIALS_JSON):
        return False, f"Arquivo de credenciais não encontrado: {GOOGLE_CREDENTIALS_JSON}"
    
    if not GOOGLE_SPREADSHEET_ID:
        return False, "GOOGLE_SPREADSHEET_ID não configurado no .env"
    
    return True, ""


def exportar_para_sheets(df: pd.DataFrame) -> Tuple[bool, str]:
    """
    Exporta um DataFrame para uma planilha do Google Sheets.
    
    A função limpa todos os dados existentes na aba e insere os novos dados.
    
    Args:
        df: DataFrame pandas com os dados a serem exportados
        
    Returns:
        Tuple[bool, str]: (sucesso, mensagem)
            - Se sucesso: (True, mensagem de sucesso)
            - Se falha: (False, mensagem de erro)
    """
    # Verificar configuração antes de importar gspread
    configurado, erro = _verificar_configuracao()
    if not configurado:
        return False, erro
    
    try:
        import gspread
        from gspread.exceptions import GSpreadException
    except ImportError:
        return False, "Biblioteca gspread não instalada. Execute: pip install gspread"
    
    try:
        # Autenticar usando Service Account
        gc = gspread.service_account(filename=GOOGLE_CREDENTIALS_JSON)
        
        # Abrir planilha por ID
        spreadsheet = gc.open_by_key(GOOGLE_SPREADSHEET_ID)
        
        # Verificar se a aba já existe
        aba_existente = None
        try:
            aba_existente = spreadsheet.worksheet(GOOGLE_SHEET_NAME)
        except gspread.WorksheetNotFound:
            pass
        
        if aba_existente:
            # Se é a única aba, não podemos deletar - apenas limpar e redimensionar
            if len(spreadsheet.worksheets()) == 1:
                aba_existente.clear()
                aba_existente.resize(rows=len(df) + 1, cols=len(df.columns))
                # Limpar formatação usando batch_update
                aba_existente.clear_basic_filter()
                worksheet = aba_existente
            else:
                # Se há outras abas, criar nova com nome temporário, deletar antiga, renomear
                temp_name = f"_temp_{GOOGLE_SHEET_NAME}"
                worksheet = spreadsheet.add_worksheet(
                    title=temp_name, 
                    rows=len(df) + 1, 
                    cols=len(df.columns)
                )
                spreadsheet.del_worksheet(aba_existente)
                worksheet.update_title(GOOGLE_SHEET_NAME)
        else:
            # Aba não existe, criar nova
            worksheet = spreadsheet.add_worksheet(
                title=GOOGLE_SHEET_NAME, 
                rows=len(df) + 1, 
                cols=len(df.columns)
            )
        
        # Preparar dados: cabeçalho + linhas
        # Converter todos os valores para string para evitar problemas de serialização
        dados = [df.columns.tolist()]
        for _, row in df.iterrows():
            linha = [str(val) if pd.notna(val) else "" for val in row.tolist()]
            dados.append(linha)
        
        # Atualizar planilha com todos os dados de uma vez
        worksheet.update(dados, value_input_option="USER_ENTERED")
        
        return True, f"Dados exportados com sucesso para Google Sheets (aba: {GOOGLE_SHEET_NAME})"
        
    except GSpreadException as e:
        return False, f"Erro do Google Sheets: {e}"
    except FileNotFoundError:
        return False, f"Arquivo de credenciais não encontrado: {GOOGLE_CREDENTIALS_JSON}"
    except Exception as e:
        return False, f"Erro ao exportar para Google Sheets: {type(e).__name__}: {e}"
