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

## Uso

1. Coloque o arquivo `.xlsx` do cliente na pasta `input/`
2. Execute:

```bash
python main.py
```

3. O arquivo gerado estará em `output/analise_tecnica_YYYY-MM-DD.xlsx`

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
│   └── utils.py                # Helpers gerais
├── .env                        # Credenciais do banco (não versionado)
├── .env.example                # Modelo de configuração
└── main.py                     # Ponto de entrada
```

## Colunas esperadas na entrada

| Coluna | Obrigatória |
|---|---|
| Data Comitê | Sim |
| Demanda | Sim |
| Analista | Sim |
| Sistema | Sim |
| Situação | Sim |
| Versão | Sim |
| Data Prevista Produção | Sim |
| Observação | Sim |

## Colunas geradas na saída

| Coluna | Origem |
|---|---|
| Demanda | Planilha do cliente |
| Descrição | Oracle — DS_TITULO da demanda |
| Analista/Programador | Oracle — usuário com maior tempo em SIDEMAITEM |
| Demandas Pendentes | Oracle — demandas que compartilham arquivos via MOSERDEM |
| Observação | Planilha do cliente |
| Objeto (Envolvimento na demanda) | Oracle — classificação via FN_ARQ_USADOS_DEM e SISCRIPT |
| Programa Alterado | Coluna "Sistema" do cliente |
| Versão Pacote Atualização | Coluna "Versão" do cliente |
| Data Envio Pacote | Preenchimento manual |
