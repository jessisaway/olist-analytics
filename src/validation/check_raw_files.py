"""Verifica a presença dos nove CSVs oficiais da Olist."""

from pathlib import Path

RAW_DIR = Path(__file__).resolve().parents[2] / "data" / "raw"

EXPECTED_CSV_NAMES = (
    "olist_customers_dataset.csv",
    "olist_geolocation_dataset.csv",
    "olist_order_items_dataset.csv",
    "olist_order_payments_dataset.csv",
    "olist_order_reviews_dataset.csv",
    "olist_orders_dataset.csv",
    "olist_products_dataset.csv",
    "olist_sellers_dataset.csv",
    "product_category_name_translation.csv",
)


def raw_csv_paths(raw_dir: Path = RAW_DIR) -> tuple[Path, ...]:
    """Retorna os caminhos esperados dos CSVs, mesmo quando estão ausentes."""
    return tuple(raw_dir / name for name in EXPECTED_CSV_NAMES)


def main() -> int:
    """Lista os arquivos encontrados e retorna 1 se algum estiver ausente."""
    paths = raw_csv_paths()
    found_count = 0

    for path in paths:
        if path.is_file():
            print(f"[OK] {path.name}")
            found_count += 1
        else:
            print(f"[AUSENTE] {path.name}")

    print(f"\n{found_count}/{len(paths)} arquivos encontrados em {RAW_DIR}.")
    if found_count < len(paths):
        print("Coloque os CSVs originais do Kaggle em data/raw/ e execute novamente.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
