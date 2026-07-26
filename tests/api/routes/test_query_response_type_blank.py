"""QueryRequest response_type must stay non-empty after stripping."""

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


@pytest.mark.parametrize("response_type", ["  ", "\t\t", "\n"])
def test_response_type_rejects_whitespace_only(response_type):
    with pytest.raises(ValidationError):
        QueryRequest(query="hello world", response_type=response_type)


def test_response_type_strips_surrounding_whitespace():
    req = QueryRequest(query="hello world", response_type="  Bullet Points  ")
    assert req.response_type == "Bullet Points"
