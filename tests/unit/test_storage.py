import pytest
import lightspeed_sdk.storage as storage
import lightspeed_sdk.utils as utils
import os
import sqlite3
import importlib
import time

utils.config["sdk"]["db_file"] = "test.db"


class TestStorageFreshDB:
    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        os.remove("test.db")

    def test_storage_file_new_and_lookup(self):
        account = [1, "test_access_token", "test_refresh_token"]
        storage.Storage(*account)
        record = storage.Storage(1)
        assert set(account).issubset(record.tokens)

    def test_storage_file_update(self):
        first_record = storage.Storage(41, "first_access_token", "first_refresh_token")
        first_timestamp = first_record.tokens[3]
        time.sleep(1)
        account = [41, "second_access_token", "second_refresh_token"]
        second_record = storage.Storage(*account)
        second_timestamp = second_record.tokens[3]
        connection = sqlite3.connect(utils.config["sdk"]["db_file"])
        cursor = connection.cursor()
        cursor.execute("SELECT count(*) FROM tokens")
        record_count = cursor.fetchone()[0]

        assert record_count == 1 and set(account).issubset(second_record.tokens) \
            and first_timestamp < second_timestamp

    def test_storage_no_tokens(self):
        with pytest.raises(Exception) as excinfo:
            storage.Storage("100")
        assert "100 was not located in available record" in str(excinfo.value)


def test_storage_no_specified_storage_type():
    storage_method = utils.config["sdk"]["token_storage_method"]
    utils.config["sdk"]["token_storage_method"] = "not_real"
    with pytest.raises(Exception) as excinfo:
        storage.Storage("100", "access", "refresh")
    utils.config["sdk"]["token_storage_method"] = storage_method
    assert "SDK is configured with a " \
           "token_storage_method that does not" in str(excinfo.value)


def test_no_id_supplied():
    with pytest.raises(Exception) as excinfo:
        storage.Storage()
    assert "No lightspeed retail account ID" in str(excinfo.value)

