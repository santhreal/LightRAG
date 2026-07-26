"""QueryRequest keyword lists must not keep blank entries."""

import importlib
import sys

import pytest
from pydantic import ValidationError

_original_argv = sys.argv[:]
sys.argv = [sys.argv[0]]
_qr = importlib.import_module("lightrag.api.routers.query_routes")
sys.argv = _original_argv

QueryRequest = _qr.QueryRequest

pytestmark = pytest.mark.offline


@pytest.mark.parametrize(
    "kwargs",
    [
        {"hl_keywords": ["  "]},
        {"hl_keywords": ["ok", ""]},
        {"ll_keywords": ["\t"]},
        {"ll_keywords": ["", "x"]},
    ],
)
def test_query_keywords_reject_blank_entries(kwargs):
    with pytest.raises(ValidationError):
        QueryRequest(query="hello world", **kwargs)


def test_query_keywords_strip_surrounding_whitespace():
    req = QueryRequest(query="hello world", hl_keywords=["  Tesla  "], ll_keywords=["  EV "])
    assert req.hl_keywords == ["Tesla"]
    assert req.ll_keywords == ["EV"]
