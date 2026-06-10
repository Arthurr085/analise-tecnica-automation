# Análise Técnica

Gera automaticamente a planilha de Análise Técnica a partir de uma planilha recebida do cliente, consultando dados complementares no banco Oracle.

## Requisitos

- Python 3.12+
- Oracle Client instalado e configurado

## Instalação

```bash
pip install -r requirements.txt
```

## Configuração do banco

Copie o arquivo de exemplo e preencha com as credenciais do banco Oracle:

```bash
cp .env.example .env
```

Edite o `.env`:

```
DB_HOST=host_do_banco
DB_PORT=porta_do_banco
DB_SERVICE_NAME=nome_do_servico
DB_USER=usuario_do_banco
DB_PASSWORD=senha_do_banco
```

## Configuração do Google Sheets (opcional)

O sistema pode exportar automaticamente os dados gerados para uma planilha do Google Sheets. Esta funcionalidade é **opcional** — se não configurada, apenas o arquivo Excel será gerado.

### 1. Criar Service Account no Google Cloud

1. Acesse o [Google Cloud Console](https://console.cloud.google.com/)
2. Crie um novo projeto ou selecione um existente
3. Ative a **Google Sheets API** em "APIs & Services" > "Enable APIs"
4. Vá em "APIs & Services" > "Credentials" > "Create Credentials" > "Service Account"
5. Preencha os dados e clique em "Create"
6. Na aba "Keys", clique em "Add Key" > "Create new key" > "JSON"
7. Salve o arquivo JSON baixado em um local seguro

### 2. Criar e compartilhar a planilha

> **⚠️ Importante:** A planilha deve ser **nativa do Google Sheets**, não um arquivo Excel (.xlsx) hospedado no Google Drive. Se você fez upload de um Excel, converta-o: Arquivo → Salvar como Planilha Google.

1. Crie uma planilha em [sheets.google.com](https://sheets.google.com) ou use uma existente
2. Copie o ID da planilha (parte da URL: `https://docs.google.com/spreadsheets/d/{ID}/edit`)
3. Compartilhe a planilha com o email do Service Account (encontrado no JSON, campo `client_email`)
4. Dê permissão de **Editor**

### 3. Configurar variáveis de ambiente

Adicione ao seu `.env`:

```
GOOGLE_CREDENTIALS_JSON=caminho/para/credentials.json
GOOGLE_SPREADSHEET_ID=id_da_planilha_google
GOOGLE_SHEET_NAME=nome_da_aba
```

- `GOOGLE_CREDENTIALS_JSON`: Caminho para o arquivo JSON de credenciais
- `GOOGLE_SPREADSHEET_ID`: ID da planilha (copiado da URL)
- `GOOGLE_SHEET_NAME`: Nome da aba onde os dados serão inseridos (opcional, padrão: "Sheet1")

> **💡 Nota:** A Google Sheets API é **gratuita** para uso normal (limite de 300 requisições/minuto).

## Uso

1. Coloque o arquivo `.xlsx` do cliente na pasta `input/`
2. Execute:

```bash
python main.py
```

3. O arquivo gerado estará em `output/analise_tecnica_YYYY-MM-DD.xlsx`
4. Se configurado, os dados também serão exportados para o Google Sheets

> **Nota:** Se houver erro na exportação para Google Sheets, o sistema exibe um aviso mas continua funcionando normalmente — o arquivo Excel sempre será gerado.

## Estrutura

```
analise-tecnica-automation/
├── input/                      # Planilha do cliente (.xlsx)
├── output/                     # Planilha gerada
├── logs/                       # Reservado para logs futuros
├── config/
│   ├── mapeamento.py           # Colunas obrigatórias e mapeamento entrada→saída
│   ├── colunas_saida.py        # Colunas do arquivo final
│   └── banco.py                # Conexão Oracle (lê variáveis do .env)
├── src/
│   ├── leitor.py               # Leitura e validação da planilha do cliente
│   ├── banco.py                # Consultas Oracle
│   ├── gerador.py              # Montagem do DataFrame de saída
│   ├── formatador_excel.py     # Formatação visual (openpyxl)
│   ├── google_sheets.py        # Exportação para Google Sheets (gspread)
│   └── utils.py                # Helpers gerais
├── .env                        # Credenciais do banco (não versionado)
├── .env.example                # Modelo de configuração
└── main.py                     # Ponto de entrada
```

## Colunas esperadas na entrada

| Coluna                 | Obrigatória |
| ---------------------- | ----------- |
| Data Comitê            | Sim         |
| Demanda                | Sim         |
| Analista               | Sim         |
| Sistema                | Sim         |
| Situação               | Sim         |
| Versão                 | Sim         |
| Data Prevista Produção | Sim         |
| Observação             | Sim         |

## Colunas geradas na saída

| Coluna                           | Origem                                                   |
| -------------------------------- | -------------------------------------------------------- |
| Demanda                          | Planilha do cliente                                      |
| Descrição                        | Oracle — DS_TITULO da demanda                            |
| Analista/Programador             | Oracle — usuário com maior tempo em SIDEMAITEM           |
| Demandas Pendentes               | Oracle — demandas que compartilham arquivos via MOSERDEM |
| Observação                       | Planilha do cliente                                      |
| Objeto (Envolvimento na demanda) | Oracle — classificação via FN_ARQ_USADOS_DEM e SISCRIPT  |
| Programa Alterado                | Coluna "Sistema" do cliente                              |
| Versão Pacote Atualização        | Coluna "Versão" do cliente                               |
| Data Envio Pacote                | Preenchimento manual                                     |
