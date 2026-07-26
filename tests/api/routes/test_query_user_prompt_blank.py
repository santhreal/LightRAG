"""QueryRequest user_prompt must stay non-empty after stripping when set."""

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


@pytest.mark.parametrize("user_prompt", ["", "  ", "\t\n"])
def test_user_prompt_rejects_blank(user_prompt):
    with pytest.raises(ValidationError):
        QueryRequest(query="hello world", user_prompt=user_prompt)


def test_user_prompt_strips_surrounding_whitespace():
    req = QueryRequest(query="hello world", user_prompt="  use bullets  ")
    assert req.user_prompt == "use bullets"


def test_user_prompt_none_still_allowed():
    req = QueryRequest(query="hello world", user_prompt=None)
    assert req.user_prompt is None
