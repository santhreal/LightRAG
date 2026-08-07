"""Coverage for JsonKVStorage legacy cache structure migration.

WHY: _migrate_legacy_cache_structure must not silently drop keys whose value is
an empty dictionary (e.g. unpopulated cache namespace entries or non-legacy dicts),
which occurred because all([]) returned True on empty dictionary values.
"""

import pytest

from lightrag.kg.json_kv_impl import JsonKVStorage
from lightrag.kg.shared_storage import finalize_share_data, initialize_share_data

pytestmark = pytest.mark.offline


@pytest.fixture(autouse=True)
def setup_shared_data():
    initialize_share_data()
    yield
    finalize_share_data()


@pytest.mark.asyncio
async def test_migrate_legacy_cache_structure_preserves_empty_dict_values(tmp_path):
    storage = JsonKVStorage(
        namespace="llm_response_cache",
        global_config={"working_dir": str(tmp_path)},
        embedding_func=None,
        workspace="test",
    )

    data = {
        "empty_namespace_key": {},
        "legacy_mode": {
            "hash1": {"cache_type": "extract", "return": "result1"},
        },
        "non_dict_key": "scalar_value",
    }

    migrated = await storage._migrate_legacy_cache_structure(data)

    assert "empty_namespace_key" in migrated, (
        "_migrate_legacy_cache_structure must preserve keys with empty dict values"
    )
    assert migrated["empty_namespace_key"] == {}
    assert migrated["non_dict_key"] == "scalar_value"
    assert "legacy_mode:extract:hash1" in migrated
    assert migrated["legacy_mode:extract:hash1"] == {
        "cache_type": "extract",
        "return": "result1",
    }
