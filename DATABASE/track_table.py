import sqlite3

import settings


def get_tracks_incomplete():
    """
    get the tracks id of the tracks that info is not complete
    :return list list_ids: a list of the tracks ids that are incomplete
    """
    # Open database connection
    con = sqlite3.connect(settings.DB_ABSOLUTE_PATH)
    cur = con.cursor()

    # Check if the pair (track_id and played_at) are already on the table play
    sql_select_ids_ = '''SELECT id
                         FROM track 
                         WHERE name IS NULL'''

    cur.execute(sql_select_ids_)
    list_ids = list()
    for i in cur.fetchall():
        list_ids.append(i[0])

    return list_ids
