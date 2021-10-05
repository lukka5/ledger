import pytest


@pytest.fixture
def tmp_csv_factory(tmp_path):
    def _inner(*lines):
        csvfile = tmp_path / "test.csv"
        csvfile.write_text("\n".join(lines))
        return csvfile

    return _inner
