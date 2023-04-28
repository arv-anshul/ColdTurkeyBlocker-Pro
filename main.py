"""
Get Pro Subscription of Cold Turkey Blocker.

Author: Anshul Raj Verma
Github: https://github.com/arv-anshul

Check Also
----------
`ColdTurkeyBlocker-Disable`: Disable all blocker at once.
https://github.com/arv-anshul/ColdTurkeyBlocker-Disable
"""

import logging
from json import dumps, loads
from os import system
from sqlite3 import Cursor
from time import sleep

from db_connector import ColdTurkeyDatabase

CTB = 'Cold Turkey Blocker'


logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s -> %(message)s'
)


def make_pro(c: Cursor):
    get_data_sql = "SELECT value FROM settings WHERE key = 'settings'"
    s = c.execute(get_data_sql).fetchone()[0]
    data = loads(s)

    if data['additional']['proStatus'] != 'pro':
        logging.info('%s is not activated.', CTB)
        sleep(2.0)
        data['additional']['proStatus'] = 'pro'

        update_data_sql = "UPDATE settings SET value = ? WHERE 'key' = 'settings'"
        c.execute(update_data_sql, (dumps(data),))
        logging.info('%s is now activated.', CTB)
        return True
    else:
        logging.info('%s is already activated.', CTB)
        return False


def main():
    while True:
        system_type = input('Choose [Mac | Windows]: ').lower()
        if system_type.lower() in ['mac', 'windows']:
            break
    db = ColdTurkeyDatabase(system_type)
    conn, c = db.make_connection()

    pro = make_pro(c)
    if pro:
        logging.info('Committing the changed settings.')
        conn.commit()

    db.close_connection(conn)

    if pro:
        if system_type == 'mac':
            system("killall 'Cold Turkey Blocker'")
            logging.info('Open %s', CTB)
        else:
            logging.critical('"Reopen %s" OR "Restart the system"', CTB)


if __name__ == '__main__':
    main()
