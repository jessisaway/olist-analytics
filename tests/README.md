# Testes automatizados

## Teste implementado

`CheckRawFilesTest.test_reports_missing_csvs` verifica o comportamento da checagem de presença quando nenhum dos nove CSVs está disponível. O teste simula a ausência dos arquivos e usa apenas a biblioteca padrão do Python. [Código do teste](test_check_raw_files.py)

O resultado esperado é que a função `main()` da checagem retorne `1` e exiba `[AUSENTE]` para cada CSV esperado.

## Como executar

No PowerShell, a partir da raiz do projeto, execute a suíte com o ambiente virtual configurado. [Guia de configuração](../docs/setup.md)

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Quando a suíte passa, o `unittest` exibe `Ran 1 test` e `OK` e retorna código `0` ao PowerShell.

## Checagens com os arquivos reais

A verificação de presença e a leitura dos cabeçalhos são checagens executadas separadamente com os CSVs locais. Com a base disponível e legível, o resultado esperado é encontrar os nove arquivos e ler os nove cabeçalhos. [Comandos de checagem](../docs/setup.md#2-preparar-e-conferir-os-csvs)

## Testes futuros

As verificações abaixo são propostas para as próximas etapas.

- **Preparação.** Validar a leitura de tipos e datas, a cobertura de campos obrigatórios e a rastreabilidade das regras de tratamento.
- **Modelagem dimensional.** Verificar a unicidade das chaves no nível de detalhe definido para cada fato ou dimensão e a cobertura dos relacionamentos.
- **Conciliação.** Conferir se as junções preservam os totais de referência de itens, fretes e pagamentos para as populações definidas.

Adicione novos casos em arquivos `test_*.py` com `unittest.TestCase`.
