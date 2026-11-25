"""Verifica como a checagem de presença sinaliza arquivos ausentes."""

from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

from src.validation.check_raw_files import EXPECTED_CSV_NAMES, main


class CheckRawFilesTest(TestCase):
    def test_reports_missing_csvs(self) -> None:
        output = StringIO()

        with patch.object(Path, "is_file", return_value=False), redirect_stdout(output):
            exit_code = main()

        self.assertEqual(exit_code, 1)
        for name in EXPECTED_CSV_NAMES:
            with self.subTest(csv=name):
                self.assertIn(f"[AUSENTE] {name}", output.getvalue())
