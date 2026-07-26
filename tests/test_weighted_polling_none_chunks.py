"""pick_by_weighted_polling must tolerate sorted_chunks=None."""

import pytest

from lightrag.utils import pick_by_weighted_polling

pytestmark = pytest.mark.offline


def test_single_entity_none_sorted_chunks_returns_empty():
    assert pick_by_weighted_polling([{"sorted_chunks": None}], 3) == []


def test_multi_entity_none_sorted_chunks_skips_without_typeerror():
    selected = pick_by_weighted_polling(
        [
            {"sorted_chunks": None},
            {"sorted_chunks": ["c1", "c2"]},
        ],
        2,
        1,
    )
    assert selected == ["c1", "c2"]


def test_missing_sorted_chunks_still_defaults_to_empty():
    assert pick_by_weighted_polling([{}], 3) == []


def test_string_sorted_chunks_treated_as_empty():
    # A non-list value must not be sliced as if it were a chunk list.
    assert pick_by_weighted_polling([{"sorted_chunks": "abc"}], 2) == []
