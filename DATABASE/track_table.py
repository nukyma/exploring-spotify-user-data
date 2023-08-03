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


def insert_into_track(data):

    # Open database connection
    con = sqlite3.connect(settings.DB_ABSOLUTE_PATH)
    cur = con.cursor()

    for d in data:

        sql_update_track_ = '''UPDATE track
                               SET name = ?, 
                                   album_id = ?,
                                   album_name = ?,
                                   artists_id = ?,
                                   artists_names = ?,
                                   duration_ms = ?,
                                   explicit = ?,
                                   popularity = ?,
                                   type = ?,
                                   preview_url = ? 
                                WHERE id = ? '''

        par_update_track_ = (d['name'],
                             d['album_id'],
                             d['album_name'],
                             d['artists_id'],
                             d['artists_names'],
                             d['duration_ms'],
                             d['explicit'],
                             d['popularity'],
                             d['type'],
                             d['preview_url'],
                             d['id'])

        cur.execute(sql_update_track_, par_update_track_)

    con.commit()
    con.close()
