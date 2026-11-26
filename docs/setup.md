# Configuração e execução no Windows

Use o PowerShell na raiz do projeto e uma instalação de Python a partir da versão 3.11. A execução desta etapa foi validada com Python 3.13.17 de 64 bits. As etapas abaixo usam o executável de `.venv` diretamente. [Downloads oficiais do Python para Windows](https://www.python.org/downloads/windows/)

## 1. Criar o ambiente virtual

Se o comando `py` estiver disponível, confira a versão e crie o ambiente. Para selecionar o Python 3.13 quando houver várias versões instaladas, use `py -3.13` nos dois comandos.

```powershell
py -3 --version
py -3 -m venv .venv
```

Se a instalação disponibilizar o comando `python`, use `python --version` e `python -m venv .venv`. Se esta cópia já tiver o interpretador local em `.tools/`, use o comando abaixo para criar o ambiente com ele.

```powershell
.\.tools\python\tools\python.exe -m venv .venv
```

Instale e confira as dependências.

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip check
```

## 2. Preparar e conferir os CSVs

Baixe o conjunto de dados e extraia os nove CSVs diretamente em `data/raw/`, com os nomes originais. Os ambientes locais e os arquivos de dados em `raw/`, `interim/` e `processed/` ficam fora do Git. [Dataset da Olist no Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

```powershell
.\.venv\Scripts\python.exe -m src.validation.check_raw_files
.\.venv\Scripts\python.exe -m src.ingestion.read_raw_headers
```

O primeiro comando confere a presença dos arquivos. O segundo lê os cabeçalhos com Pandas e exibe as colunas. Ambos retornam código 0 em caso de sucesso e 1 se a verificação falhar. Consulte `$LASTEXITCODE` logo após o comando. Os nomes dos nove arquivos e os campos esperados estão no [dicionário de dados](data_dictionary.md).

## 3. Reproduzir a análise exploratória

```powershell
.\.venv\Scripts\python.exe -m jupyterlab
```

No JupyterLab, abra o notebook e execute todas as células em ordem usando o ambiente do projeto. As saídas são tabelas e gráficos agregados. [Notebook de exploração](../notebooks/01_data_profiling.ipynb)

## 4. Executar os testes

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

O teste automatizado verifica como o script sinaliza a ausência dos CSVs. Os comandos da seção 2 verificam os arquivos reais da cópia local. [Guia de testes](../tests/README.md)
