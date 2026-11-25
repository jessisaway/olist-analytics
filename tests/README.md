# Testes automatizados

Adicione os futuros testes em arquivos `test_*.py` e use `unittest.TestCase` da biblioteca padrão do Python. Execute a descoberta dos testes na raiz do projeto.

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests
```

O teste inicial verifica a saída do script quando os CSVs estão ausentes. A checagem de presença e o teste de leitura dos arquivos reais são executados pelos comandos do [README principal](../README.md).
