# Olist Analytics — E-commerce Performance & Customer Experience

Projeto de portfólio em Análise de Dados e Business Intelligence sobre o desempenho do e-commerce brasileiro e a experiência de compra. A análise vai explorar vendas, comportamento do cliente, prazos de entrega e avaliações para responder perguntas como **onde os atrasos se concentram** e **como os prazos de entrega se relacionam com as avaliações dos clientes**.

A fonte é o [Brazilian E-Commerce Public Dataset by Olist, no Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce). A base reúne pedidos, itens, pagamentos, avaliações, clientes, vendedores, produtos, geolocalização e a tradução das categorias de produto.

## Tecnologias

| Ferramenta | Uso no projeto |
| --- | --- |
| Python 3.11+, Pandas, JupyterLab e Matplotlib | Leitura, exploração, visualizações e verificações de qualidade |
| DuckDB e SQL | Consultas analíticas locais |
| PyArrow e Parquet | Armazenamento local das saídas preparadas |
| Power BI Desktop e DAX | Modelo analítico, indicadores e dashboard |
| Figma | Identidade visual e protótipo do dashboard |
| Git e GitHub | Controle de versão e documentação do portfólio |

O processamento e o armazenamento serão locais.

## Etapas do projeto

1. **Estrutura e ambiente.** Organizar o projeto e conferir a presença e a leitura dos cabeçalhos dos nove CSVs originais.
2. **Exploração e qualidade.** Investigar a granularidade das tabelas, a cobertura temporal e a qualidade dos dados.
3. **Preparação e modelagem dimensional.** Preparar os dados com Python e SQL e materializar as saídas em Parquet.
4. **Dashboard e storytelling.** Desenhar o protótipo no Figma e desenvolver os indicadores DAX e a apresentação dos resultados no Power BI.

## Estrutura

```text
olist-analytics/
├── data/
│   ├── raw/
│   ├── interim/
│   └── processed/
├── notebooks/
│   └── 01_data_profiling.ipynb
├── src/
│   ├── ingestion/
│   │   └── read_raw_headers.py
│   ├── cleaning/
│   ├── modeling/
│   └── validation/
│       └── check_raw_files.py
├── sql/
├── tests/
│   ├── README.md
│   └── test_check_raw_files.py
├── docs/
│   ├── data_dictionary.md
│   ├── source_relationships.md
│   └── figma/
├── powerbi/
├── reports/
│   ├── data_quality_report.md
│   └── eda_findings.md
├── requirements.txt
├── .gitignore
└── README.md
```

## Configuração no Windows com PowerShell

Execute os comandos na raiz do projeto. Use o Python 3.11 ou superior, de preferência em 64 bits. O [instalador oficial do Python para Windows](https://www.python.org/downloads/windows/) disponibiliza o comando `py`. Se sua instalação disponibiliza apenas `python`, use esse comando no lugar de `py -3`.

```powershell
py -3 --version
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip check
```

Os comandos usam o executável de `.venv` diretamente, dispensando a ativação do ambiente no PowerShell.

Se esta cópia do projeto já tiver o Python local em `.tools/`, use o executável abaixo para recriar o ambiente virtual.

```powershell
.\.tools\python\tools\python.exe -m venv .venv
```

## Dados e verificação da Etapa 1

Baixe e extraia os nove arquivos CSV do [Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) em `data/raw/`, mantendo seus nomes originais. Os dados brutos e os arquivos das pastas `data/interim/` e `data/processed/` ficam fora do Git.

```powershell
.\.venv\Scripts\python.exe -m src.validation.check_raw_files
.\.venv\Scripts\python.exe -m src.ingestion.read_raw_headers
```

O primeiro comando lista os arquivos encontrados e ausentes. O segundo usa Pandas para ler somente os cabeçalhos e lista as colunas de cada CSV. Ambos retornam código 0 em caso de sucesso e 1 se a verificação falhar. No PowerShell, consulte `$LASTEXITCODE` logo após o comando para ver o código retornado.

Os comandos apenas leem os arquivos de origem. O [guia de testes](tests/README.md) explica como executar e ampliar os testes automatizados.

## Exploração e qualidade — Etapa 2

Para abrir e reexecutar o notebook no JupyterLab, instale as dependências atualizadas e execute na raiz do projeto.

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m jupyterlab
```

Abra `notebooks/01_data_profiling.ipynb` e execute todas as células com os CSVs em `data/raw/`. O notebook apresenta tabelas e gráficos agregados.

- [Notebook de exploração](notebooks/01_data_profiling.ipynb)
- [Dicionário de dados](docs/data_dictionary.md)
- [Relacionamentos e granularidade](docs/source_relationships.md)
- [Relatório de qualidade](reports/data_quality_report.md)
- [Descobertas e perguntas de negócio](reports/eda_findings.md)
