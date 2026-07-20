"""GRAPH_FIELD_SEP must not survive sanitize_and_normalize_extracted_text.

Descriptions and entity names are later joined/split on GRAPH_FIELD_SEP.
If free-form extracted text still contains that delimiter, merge/reload
forges extra description fragments and relation chunk keys collide.
"""

import pytest

from lightrag.constants import GRAPH_FIELD_SEP
from lightrag.utils import (
    make_relation_chunk_key,
    sanitize_and_normalize_extracted_text,
)


@pytest.mark.offline
def test_sanitize_strips_graph_field_sep_from_description():
    raw = "Protocol uses the <SEP> token between fields"
    cleaned = sanitize_and_normalize_extracted_text(raw)

    assert GRAPH_FIELD_SEP not in cleaned
    fragments = [p for p in cleaned.split(GRAPH_FIELD_SEP) if p]
    assert fragments == [cleaned]


@pytest.mark.offline
def test_sanitize_prevents_relation_chunk_key_collision():
    left = sanitize_and_normalize_extracted_text("Alice<SEP>Corp")
    right_a = sanitize_and_normalize_extracted_text("Bob")
    mid = sanitize_and_normalize_extracted_text("Alice")
    right_b = sanitize_and_normalize_extracted_text("Corp<SEP>Bob")

    assert make_relation_chunk_key(left, right_a) != make_relation_chunk_key(
        mid, right_b
    )
