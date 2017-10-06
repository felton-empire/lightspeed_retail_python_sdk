from .utils import config
import sqlite3


class Storage:
    """Creates a storage object containing the credentials of the supplied
    account ID. If refresh_token and access_token are provided, they will be
    updated or created.

    Args:
        account_id:
        refresh_token:
        access_token:

    Attributes:
        tokens:
    """
    def __init__(self, account_id=-1, access_token=False, refresh_token=False):
        storage_type = config["sdk"]["token_storage_method"]
        if not int(account_id) > -1:
            raise Exception("No lightspeed retail account ID supplied. Unable"
                            "to authenticate without it.")
        if storage_type == "file":
            Storage.connection = sqlite3.connect(config["sdk"]["db_file"],
                                                 isolation_level=None)
            Storage.cursor = Storage.connection.cursor()
            self.tokens = self.file(account_id, access_token, refresh_token)
            Storage.connection.commit()
            Storage.connection.close()
        else:
            raise Exception("SDK is configured with a token_storage_method "
                            "that does not exist.")
            exit()

    def file(self, account_id, access_token, refresh_token):
        """The default file storage method actually uses sqlite.

        Create the database and table if they don't exist.

        Then if no access token and refresh token are provided, return the
        account token record for the account_id supplied. Otherwise update
        the access_token and refresh_token as appropriate. Note that the access
        token is ALWAYS updated. The refresh token may or may not be updated
        """

        Storage.cursor.execute("SELECT count(*) FROM sqlite_master "
                       "WHERE type='table' AND "
                       "name='table_name';")
        table_exists = Storage.cursor.fetchone()[0]

        if not table_exists:
            Storage.cursor.execute("CREATE TABLE IF NOT EXISTS "
                                   "tokens(account_id INTEGER PRIMARY KEY,"
                                   " refresh_token, access_token, updated);")

        if not access_token and not refresh_token:
            account = self._file_select(account_id)
            if not account:
                raise Exception("The account with ID " + str(account_id) +
                                " was not located in available records")
            else:
                return account

        elif not access_token and refresh_token:
            raise Exception("Can't update refresh token without also having an "
                            "access token. Access token is always provided by"
                            "the lightspeed API when a new refresh token is"
                            "authorized.")
        else:
            return self._file_insert(account_id, access_token, refresh_token)

    def _file_select(self, account_id):
        Storage.cursor.execute("SELECT * FROM tokens WHERE account_id =" +
                       str(account_id) + ";")

        return Storage.cursor.fetchone()

    def _file_insert(self, account_id, access_token, refresh_token):
        if not refresh_token:
            fields = "(account_id, access_token, updated)"
            values = "('" + str(account_id) + "','" + access_token + "'," + \
                     "CURRENT_TIMESTAMP)"
        else:
            fields = "(account_id, access_token, refresh_token, updated)"
            values = "('" + str(account_id) + "','" + access_token + "','" + \
                     refresh_token + "',CURRENT_TIMESTAMP)"

        query = "REPLACE INTO tokens " + fields + " VALUES" + values + ";"
        Storage.cursor.execute(query)

        return self._file_select(account_id)
