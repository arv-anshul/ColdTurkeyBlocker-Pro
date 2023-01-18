''' For Mac Only '''

import json
import os
import sqlite3

DB_PATH = r"/Library/Application Support/Cold Turkey/data-app.db"


def activate():

    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        s = (c.execute("SELECT value FROM settings WHERE key = 'settings'")
             .fetchone()[0])
        data = json.loads(s)

        if data["additional"]["proStatus"] != "pro":
            print("Your version of Cold Turkey Blocker is not activated.")
            data["additional"]["proStatus"] = "pro"
            print("But now it is activated.\nJust check it.")
            c.execute("""UPDATE settings SET value = ? WHERE "key" = 'settings'""",
                      (json.dumps(data),))
            conn.commit()

        else:
            print("Looks like your copy of Cold Turkey Blocker is already activated.")
            print("Deactivating it now.")
            data["additional"]["proStatus"] = "free"
            c.execute("""UPDATE settings set value = ? WHERE "key" = 'settings'""",
                      (json.dumps(data),))
            conn.commit()

    except sqlite3.Error as e:
        print("Failed to activate", e)

    finally:
        if conn:
            conn.close()
        os.system(r'killall Cold Turkey Blocker')


def main():
    if os.path.exists(DB_PATH):
        print("Data file found.\nLet's activate your copy of Cold Turkey Blocker.")
        activate()

    else:
        print("Looks like Cold Turkey Blocker is not installed.\nIf it is installed then run it at least once.")


if __name__ == '__main__':
    main()
