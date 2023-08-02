import sqlite3

import settings


def insert_into_play(data):

    # Open database connection
    con = sqlite3.connect(settings.DB_ABSOLUTE_PATH)
    cur = con.cursor()

    for d in data:

        # Check if the pair (track_id and played_at) are already on the table play
        sql_select_ = ('''SELECT track_id, track_played_at 
                       FROM play 
                       WHERE track_id = ? AND track_played_at = ? ''')
        par_select_ = (d['track_id'], d['played_at'])

        cur.execute(sql_select_, par_select_)

        result = cur.fetchone()

        # If pair (track_id and played_at) ARE NOT in the DB, we should include them
        if not result:
            sql_insert_ = ('''INSERT INTO play (track_id, track_played_at, context) 
                           VALUES (?, ?, ?)''')
            par_insert_ = (d['track_id'], d['played_at'], d['context'])

            cur.execute(sql_insert_, par_insert_)
            print(cur.lastrowid)

    con.commit()
    con.close()

    return True
