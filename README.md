# Análise Técnica — Fase 1

Gera automaticamente a planilha de Análise Técnica a partir de uma planilha recebida do cliente.

## Requisitos

- Python 3.12+

## Instalação

```bash
pip install -r requirements.txt
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
projeto_analise_tecnica/
├── input/                      # Planilha do cliente (.xlsx)
├── output/                     # Planilha gerada
├── logs/                       # Reservado para logs futuros
├── config/
│   ├── mapeamento.py           # Colunas obrigatórias e mapeamento entrada→saída
│   ├── colunas_saida.py        # Colunas do arquivo final
│   └── banco.py                # Config Oracle (Fase 2)
├── src/
│   ├── leitor.py               # Leitura e validação da planilha do cliente
│   ├── banco.py                # Dados mockados (Fase 2: Oracle)
│   ├── gerador.py              # Montagem do DataFrame de saída
│   ├── formatador_excel.py     # Formatação visual (openpyxl)
│   └── utils.py                # Helpers gerais
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
| Descrição | Mock vazio (Fase 2: Oracle) |
| Analista/Programador | Mock vazio (Fase 2: Oracle) |
| Demandas Pendentes | Vazio |
| Observação | Planilha do cliente |
| Objeto (Envolvimento na demanda) | Vazio |
| Programa Alterado | Coluna "Sistema" do cliente |
| Versão Pacote Atualização | Coluna "Versão" do cliente |
| Data Envio Pacote | Vazio |

## Fase 2 — Integração Oracle

Para ativar a integração com Oracle:

1. Preencher `config/banco.py` com as credenciais
2. Substituir o corpo de `src/banco.buscar_dados_demanda()` pela consulta real
