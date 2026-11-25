"""Testa a leitura dos cabeçalhos dos CSVs originais com Pandas."""

import pandas as pd

from src.validation.check_raw_files import raw_csv_paths


def main() -> int:
    """Exibe as colunas lidas e retorna 1 se algum arquivo falhar."""
    paths = raw_csv_paths()
    read_count = 0

    for path in paths:
        try:
            columns = pd.read_csv(path, nrows=0, encoding="utf-8-sig").columns
        except (OSError, UnicodeError, pd.errors.ParserError, pd.errors.EmptyDataError) as error:
            print(f"[ERRO] {path.name} ({error})")
            continue

        print(f"[OK] {path.name} ({len(columns)} colunas) — {', '.join(columns)}")
        read_count += 1

    print(f"\n{read_count}/{len(paths)} cabeçalhos lidos.")
    return int(read_count != len(paths))


if __name__ == "__main__":
    raise SystemExit(main())
