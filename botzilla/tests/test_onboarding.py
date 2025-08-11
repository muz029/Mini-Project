import pytest
from handlers.start import handle_consent
from storage.sqlite import SQLiteStorage

@pytest.fixture
def storage(tmp_path):
    return SQLiteStorage(str(tmp_path / "test.db"))

@pytest.mark.parametrize("agree,expected", [(True, "verified"), (False, "unverified")])
def test_handle_consent(storage, agree, expected):
    uid = 42
    storage.upsert_user(uid, "u", "f", "l", "", "2025-01-01T00:00:00Z")
    status = handle_consent(storage, uid, agree)
    assert status == expected

def test_upsert_idempotent(storage):
    uid = 99
    storage.upsert_user(uid, "u1", "f1", "l1", "", "2025-01-01T00:00:00Z")
    storage.upsert_user(uid, "u2", "f2", "l2", "", "2025-01-02T00:00:00Z")
    user = storage.get_user(uid)
    assert user["username"] == "u2"
