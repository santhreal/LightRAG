"""load_json should treat a directory path as missing, not raise."""

from pathlib import Path

import pytest

from lightrag.utils import load_json

pytestmark = pytest.mark.offline


def test_load_json_directory_returns_none(tmp_path: Path):
    d = tmp_path / "not_a_file"
    d.mkdir()
    assert load_json(str(d)) is None


def test_load_json_missing_still_none(tmp_path: Path):
    assert load_json(str(tmp_path / "missing.json")) is None


def test_load_json_valid_object(tmp_path: Path):
    p = tmp_path / "ok.json"
    p.write_text('{"a": 1}', encoding="utf-8")
    assert load_json(str(p)) == {"a": 1}
