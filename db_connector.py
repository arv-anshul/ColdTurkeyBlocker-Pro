""" Connect with Cold Turkey Blocker database. """

import logging
import sqlite3
from pathlib import Path
from sqlite3 import Connection, Cursor, DatabaseError
from typing import Literal

MAC_DB_PATH = Path('/Library/Application Support/Cold Turkey/data-app.db')
WIN_DB_PATH = Path('C:\\ProgramData\\Cold Turkey\\data-app.db')


class ColdTurkeyDatabase:
    def __init__(self, system_type: str) -> None:
        self.db_path = MAC_DB_PATH if system_type.lower() == 'mac' else WIN_DB_PATH
        self.__check_db_path(system_type)

    def __check_db_path(self, system_type):
        if system_type == 'mac':
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            self.db_path.touch(exist_ok=True)
        if not self.db_path.exists():
            raise DatabaseError(
                f'Database does not exists. Create a file at {self.db_path!s}'
            )

    def make_connection(self) -> tuple[Connection, Cursor]:
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
        except sqlite3.Error:
            logging.info('Failed to Connect with Cold Turkey blocker.')
            raise
        else:
            return conn, c

    def close_connection(self, conn: Connection) -> None:
        conn.close()
